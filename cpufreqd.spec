%define name cpufreqd
%define version 2.4.2
%define release %mkrel 6
%define lib_name %mklibname %name 

# (misc) about the rpmlint warning.
#
# file in /usr/lib are plugin, so they do not have a soname
# and they do not nned to be installable side by side with another
# version, so it is safe to ignore the error.

Name: %{name}
Summary: CPU frequency scaling daemon
Version: %{version}
Release: %{release}
Group: System/Kernel and hardware
Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1: %{name}.init.mdk.bz2
Source2: cpufreq_defaults.bz2
Patch0: %{name}.Makefile.patch
# (fc) 1.2.3-2mdk add more cpu intensive programs to full power mode
Patch1: cpufreqd-2.1.1-defaults.patch
# add patch from upstream to fix a buffer overflow with gcc-4.5
Patch2: cpufreqd-2.4.2-fix-segfault-when-calling-realpath.patch
Url: https://www.linux.it/~malattia/wiki/index.php/Cpufreqd
BuildRoot: %{_tmppath}/%{name}-buildroot
License: GPLv2+
Requires(preun,post): rpm-helper
BuildRequires: automake
BuildRequires: libcpufreq-devel
BuildRequires: sysfsutils-devel
Requires: %{lib_name} 

%description
cpufreqd is meant to be a replacement of the speedstep applet you
can find on some other OS, it monitors battery level, AC state and
running programs and adjusts the frequency of the processor according to
a set of rules specified in the config file (see cpufreqd.conf (5)).

It works only a kernel patched with the cpufreq patch, such as the 
standard Mandriva Linux kernel.
You also need a supported processor, often found in laptop computer.


%package -n %{lib_name}
Summary: Library for %{name}
Group: System/Kernel and hardware
%description -n %{lib_name}
This packages contains some library needed
by %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0
%patch1 -p1 -b .defaults
%patch2 -p1 -b .segfault
#(misc) Patch on the makefile, needed to recreate it.
#aclocal
#autoconf
#automake -a
autoreconf -fiv

%build
%configure2_5x 
%make

%install

%{__rm} -rf ${RPM_BUILD_ROOT}

%makeinstall

%{__install} -d %{buildroot}{%{_sysconfdir}/sysconfig,%{_initrddir}}
%{__bzip2} -dc %{SOURCE1} > %{buildroot}/%{_initrddir}/%{name}
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__bzip2} -dc %{SOURCE2} > %{buildroot}%{_datadir}/%{name}/cpufreq_defaults
%clean
%{__rm} -rf ${RPM_BUILD_ROOT}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root,0755)
%doc AUTHORS README TODO NEWS ChangeLog
%attr(755,root,root) %{_sbindir}/cpufreqd
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/cpufreqd.conf
%config(noreplace) %attr(755,root,root) %{_initrddir}/%{name}
%dir %{_sysconfdir}/%{name}/
%attr(644,root,root) %{_datadir}/%{name}/cpufreq_defaults
%dir %{_datadir}/%{name}/
%attr(644,root,root) %{_mandir}/*/*
%{_bindir}/*
%files -n %{lib_name}
%defattr(-,root,root,0755)
%{_libdir}/cpufreqd*




%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.2-4mdv2011.0
+ Revision: 663418
- mass rebuild

* Tue Dec 07 2010 Ahmad Samir <ahmadsamir@mandriva.org> 2.4.2-3mdv2011.0
+ Revision: 614462
- add patch from upstream to fix a buffer overflow with gcc-4.5

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4.2-2mdv2011.0
+ Revision: 603854
- rebuild

* Mon Apr 26 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4.2-1mdv2010.1
+ Revision: 539180
- update to new version 2.4.2

* Mon Mar 29 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4.1-1mdv2010.1
+ Revision: 528658
- update to new version 2.4.1

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.4-3mdv2010.1
+ Revision: 520044
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.4-2mdv2010.0
+ Revision: 413271
- rebuild

* Sat Mar 21 2009 Frederik Himpe <fhimpe@mandriva.org> 2.3.4-1mdv2009.1
+ Revision: 360065
- Update to new version 2.3.4

* Sun Mar 08 2009 Emmanuel Andry <eandry@mandriva.org> 2.3.3-2mdv2009.1
+ Revision: 352712
- use autoreconf
- fix URL

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Sat Aug 23 2008 Frederik Himpe <fhimpe@mandriva.org> 2.3.3-1mdv2009.0
+ Revision: 275402
- Adapt BuildRequires
- Don't package COPYING file but some more interesting doc files
- Update to version 2.3.3
- Fix license

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 2.2.1-3mdv2009.0
+ Revision: 220513
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 2.2.1-2mdv2008.1
+ Revision: 149133
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Jul 19 2007 Funda Wang <fwang@mandriva.org> 2.2.1-1mdv2008.0
+ Revision: 53553
- do not use versioned autotools
- New version


* Mon Dec 18 2006 Olivier Blin <oblin@mandriva.com> 2.1.1-4mdv2007.0
+ Revision: 98675
- do not require cpufreq, frequency scaling modules are now configured by DrakX/harddrake
- Import cpufreqd

* Thu Aug 31 2006 Olivier Blin <blino@mandriva.com> 2.1.1-3mdv2007.0
- add lindvd in cpu intensive programs list

* Wed Aug 30 2006 Olivier Blin <blino@mandriva.com> 2.1.1-2mdv2007.0
- add LSB tags in initscript
- return correct exit code on service status (#21197)

* Sat Jul 22 2006 Emmanuel Andry <eandry@mandriva.org> 2.1.1-1mdv2007.0
- New release 2.1.1
- rediff patch 0 and 1

* Fri Jan 13 2006 Michael Scherer <misc@mandriva.org> 2.0.0-1mdk
- New release 2.0.0
- use mkrel
- update patch1
- do not include debug information in tarball

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.2.3-3mdk
- Rebuild

* Fri Aug 12 2005 Frederic Crozat <fcrozat@mandriva.com> 1.2.3-2mdk 
- Patch1: add more programs to full power mode

* Tue Jun 21 2005 Michael Scherer <misc@mandriva.org> 1.2.3-1mdk
- New release 1.2.3
- fix rpmlint warning

* Sat Jan 29 2005 Michael Scherer <misc@mandrake.org> 1.2.2-2mdk 
- change priority of cpufreqd ( thanks to the reporter of #13304 )

* Wed Oct 27 2004 Michael Scherer <misc@mandrake.org> 1.2.2-1mdk
- New release 1.2.2

* Tue Oct 26 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.2.1-1mdk
- 1.2.1

* Wed Aug 25 2004 Michael Scherer <misc@mandrake.org> 1.2.0-2mdk 
- Requires cpufreq

* Tue Aug 24 2004 Michael Scherer <misc@mandrake.org> 1.2.0-1mdk
- New release 1.2.0

* Sat May 29 2004 Michael Scherer <misc@mandrake.org> 1.1.2-2mdk 
- [DIRM]
- fix building problem

* Tue Mar 16 2004 Michael Scherer <misc@mandrake.org> 1.1.2-1mdk
- 1.1.2
- patch #1 merged upstream
- moved cpufreq_defaults to /usr/share

* Tue Feb 24 2004 Danny Tholen <obiwan@mailmij.org> 1.1.1-3mdk
- fix bug with pmu (patch1)
- require autmake 1.4 not 1.7
- script for adjusting config at startup (source2)

* Mon Feb 09 2004 Michael Scherer <misc@mandrake.org> 1.1.1-2mdk
- 2.6 support in the init file, upstream addition

* Sun Feb 08 2004 Michael Scherer <misc@mandrake.org> 1.1.1-1mdk
- 1.1.1

* Mon Jan 05 2004 Michael Scherer <misc@mandrake.org> 1.1-1mdk 
- 1.1
- patch1 merged upstream
- some adjustement to init file.

* Fri Dec 19 2003 Michael Scherer <misc@mandrake.org> 1.1-0.rc1.2mdk 
- add patch to not have /var/run/cpufreqd.pid world writable ( thanks msec )

