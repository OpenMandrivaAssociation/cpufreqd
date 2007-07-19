%define name cpufreqd
%define version 2.2.1
%define release %mkrel 1
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
Source: %{name}-%{version}.tar.bz2
Source1: %{name}.init.mdk.bz2
Source2: cpufreq_defaults.bz2
Patch0: %{name}.Makefile.patch
# (fc) 1.2.3-2mdk add more cpu intensive programs to full power mode
Patch1: cpufreqd-2.1.1-defaults.patch
Url: http://cpufreqd.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-buildroot
License: GPL
Requires(preun,post): rpm-helper
Buildrequires: automake1.8 libcpufreq-devel
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
#(misc) Patch on the makefile, needed to recreate it.
aclocal-1.8
autoconf-2.5x
automake-1.8 -a

%build
%configure2_5x 
%make

%install

%{__rm} -rf ${RPM_BUILD_ROOT}

%makeinstall

%{__install} -d $RPM_BUILD_ROOT{%{_sysconfdir}/sysconfig,%{_initrddir}}
%{__bzip2} -dc %{SOURCE1} > $RPM_BUILD_ROOT/%{_initrddir}/%{name}
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
%{__install} -d $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__bzip2} -dc %{SOURCE2} > $RPM_BUILD_ROOT%{_datadir}/%{name}/cpufreq_defaults
%clean
%{__rm} -rf ${RPM_BUILD_ROOT}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root,0755)
%doc AUTHORS COPYING INSTALL README TODO 
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


