%define   filever 2.9.11-20080817
%define   relver 2.9.11
%define   datetag 20080817

Summary:         Userspace application for smartLink softmodems
Name:            slmodem
Version:         %{relver}
Release:         7.%{datetag}%{?dist}
Group:           System Environment/Daemons
License:         BSD w/binary object
# Outdated
# URL:           http://www.smlink.com/content.aspx?id=132
URL:             http://linmodems.technion.ac.il/packages/smartlink/
Source0:         http://linmodems.technion.ac.il/packages/smartlink/slmodem-%{filever}.tar.gz
Source1:         slmodem.init
Source2:         slmodem.sysconfig
Source3:         README.fedora
Patch0:          slmodem-2.9.11-daemon.patch
Patch1:          slmodem-2.9.11-create.patch
BuildRoot:       %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:   alsa-lib-devel
%if 0%{?fedora} >= 11
ExclusiveArch:   i586
%else
ExclusiveArch:   i386
%endif
Provides:        slmodem-alsa = %{version}, slmodem-kmod-common = %{version}
Requires(post):  /sbin/chkconfig
Requires(post):  /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service


%description
This package contains the userspace application to control several
SmartLink based modems.

More information about installation and configuration of the slmodem
package can be found at %{_docdir}/%{name}-%{version}/README.fedora
after installation.


%prep
%setup -q -n slmodem-%{filever}
%patch0 -p1 -b .daemon
%patch1 -p1 -b .create


%build
pushd modem
make %{?_smp_mflags} SUPPORT_ALSA=1 EXTRA_CFLAGS="$RPM_OPT_FLAGS" 
popd


%install
rm -rf %{buildroot}
install -D -m 755 modem/slmodemd %{buildroot}%{_sbindir}/slmodemd
install -d -m 755 %{buildroot}%{_localstatedir}/lib/slmodem

install -D -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/slmodem
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/slmodem

cp %{SOURCE3} .


%post
/sbin/chkconfig --add slmodem


%preun
if [ $1 = 0 ]; then
        /sbin/service slmodem stop >/dev/null 2>&1
        /sbin/chkconfig --del slmodem
fi


%postun
if [ "$1" -ge "1" ]; then
        /sbin/service slmodem condrestart >/dev/null 2>&1
fi


%clean
rm -rf %{buildroot}


%files
%defattr (-,root,root)
%doc README.fedora README Changes COPYING Documentation/Smartlink.txt
%{_sbindir}/slmodemd
%{_sysconfdir}/init.d/slmodem
%config(noreplace) %{_sysconfdir}/sysconfig/slmodem
%{_localstatedir}/lib/slmodem/


%changelog
* Sun Mar 29 2009 Julian Sikorski <belegdol@fedoraproject.org> - 2.9.11-7.20080817
- Fedora 11 is i586, not i386

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-6.20080817
- rebuild for new F11 features

* Sat Sep 08 2007 Andreas Thienemann <andreas@bawue.net> 2.9.11-4.20070813
- Updated to recent slmodem package

* Wed Feb 07 2007 Andreas Thienemann <andreas@bawue.net> 2.9.11-3.20070204
- Updated to recent slmodem package
- Added README.fedora, explaining some configuration and hardware support details

* Fri Apr 28 2006 Andreas Thienemann <andreas@bawue.net> 2.9.11-2
- Modified .spec to coexist with slmodem and kmod-slmodem.
- Updated description
- Changed name of initscripts

* Wed Mar 29 2006 Andreas Thienemann <andreas@bawue.net> 2.9.11-1
- Updated to 2.9.11 snapshot.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field
- drop Epoch

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Tue Jul 10 2005 Andreas Thienemann <andreas@bawue.net> 2.9.9d-0.lvn.2
- Only builds on x86

* Tue Jun 28 2005 Andreas Thienemann <andreas@bawue.net> 2.9.9d-0.lvn.1
- Repackaged for rpm.livna.org
- Added daemonize patch, cleaned up init file
- Added %%pre and %%post scriptlets

* Tue Jun 28 2005 Andreas Thienemann <andreas@bawue.net> 2.9.9d-1
- Initial package

