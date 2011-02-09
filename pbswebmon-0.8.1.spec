
Summary: A generic startup mechanism for different MPI installation in a cluster/grid.
Name: pbswebmon
Version: 0.8.1
Release: 1
License: other
Group: Application
Source: pbswebmon-0.8.1.tar.gz
URL: dsds
Packager: childss@cs.tcd.ie
BuildRoot: %{_tmppath}/%{name}-%{version}-rootA
BuildArch:  noarch
Requires: pbs_python

%description
A web-based PBS/Torque monitor.

%prep
%setup -q

%build
cd $RPM_BUILD_DIR/pbswebmon-0.8.1
#make

%install
cd $RPM_BUILD_DIR/pbswebmon-0.8.1
%{__make} DESTDIR=$RPM_BUILD_ROOT  install

%clean
rm -rf $RPM_BUILD_ROOT/*

%files
%defattr(-,root,root,-)
/var/www/
%config(noreplace) /etc/pbswebmon.conf
%doc /usr/share/doc/pbswebmon/README
