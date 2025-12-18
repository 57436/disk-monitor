Name:           disk-monitor
Version:        0.11
Release:        1%{?dist}
Summary:        Disk Space Monitoring Utility
License:        GPLv3+
URL:            github.com
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  gcc make
BuildRequires:  systemd

%description
A simple utility to monitor the available disk space on a Linux system.

%build
# ИСПРАВЛЕНИЕ: Переходим в директорию, куда RPM распаковал исходники
cd %{_builddir}/%{name}-%{version}
make

%install
# ИСПРАВЛЕНИЕ: Также нужно перейти в директорию перед копированием файлов оттуда
cd %{_builddir}/%{name}-%{version}

# Создаем целевые директории
mkdir -p %{buildroot}/usr/local/bin/
mkdir -p %{buildroot}/etc/systemd/system/

# Копируем скомпилированный бинарник и файл службы
cp disk-monitor %{buildroot}/usr/local/bin/
cp disk-monitor.service %{buildroot}/etc/systemd/system/

%files
/usr/local/bin/disk-monitor
/etc/systemd/system/disk-monitor.service

%post
systemctl daemon-reload
systemctl enable disk-monitor.service || :
systemctl start disk-monitor.service || :

%preun
if [ "$1" = "0" ]; then
    systemctl stop disk-monitor.service || :
    systemctl disable disk-monitor.service || :
    systemctl daemon-reload
fi

%changelog
* Sun Dec 14 2025 Vasiliy Petrov <petrovbsilevs@gmail.com> - 1.0-1
- Initial package creation
