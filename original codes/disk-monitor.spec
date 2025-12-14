Name:           disk-monitor
Version:        0.1
Release:        1%{1}
Summary:        Disk Space Monitoring Utility
License:        GPLv3+
URL:            https://github.com/user-12-42/disk-monitor
Source0:        %{disk_monitor}-%{v01}.tar.gz
BuildRequires:  gcc make

%description
A simple utility to monitor the available disk space on a Linux system.

%install
mkdir -p %{buildroot}/usr/local/bin/
cp disk-monitor %{buildroot}/usr/local/bin/

%files
/usr/local/bin/disk-monitor

%post
systemctl daemon-reload
systemctl enable disk-monitor.service || :
systemctl start disk-monitor.service || :

%preun
if [ "$1" = "0" ]; then
    systemctl stop disk-monitor.service || :
    systemctl disable disk-monitor.service || :
fi

%changelog
* Thu Jan 01 2025 Vasiliy Petrov <petrovbsilevs@gmail.com> - 1.0-1
- Initial package creation
