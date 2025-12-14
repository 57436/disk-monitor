#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/statvfs.h>
#include <string.h>
#include <syslog.h>

#define THRESHOLD_PERCENTAGE 15 // порог в процентах

void log_message(const char *message)
{
    openlog("disk-monitor", LOG_PID | LOG_CONS, LOG_USER);
    syslog(LOG_INFO, "%s", message);
    closelog();
}

double calculate_free_space_percentage(const char* path)
{
    struct statvfs buf;
    if(statvfs(path, &buf) != 0){
        perror("statvfs");
        return -1;
    }

    double total = buf.f_blocks * buf.f_frsize;
    double free = buf.f_bfree * buf.f_frsize;
    return ((total-free)/total)*100;
}

int main(int argc, char **argv)
{
    while(1){
        double percentage = calculate_free_space_percentage("/");

        if(percentage > 0 && percentage <= THRESHOLD_PERCENTAGE){
            char msg[256];
            snprintf(msg, sizeof(msg),"WARNING: Free disk space is below %f%%",THRESHOLD_PERCENTAGE);
            log_message(msg);
        } else {
            log_message("Disk space OK.");
        }

        sleep(20); // проверка каждые 20 секунд
    }
    return 0;
}
