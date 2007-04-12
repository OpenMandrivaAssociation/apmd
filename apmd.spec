%define name apmd
%define lib_name_orig libapm
%define lib_major 1
%define lib_name %mklibname apm %{lib_major}

%define release %mkrel 12
%define version 3.2.2
%define url http://www.worldvisions.ca/~apenwarr/apmd/

Summary: Advanced Power Management (APM) BIOS utilities for laptops
Name: %{name}
Version: %{version}
Release: %{release}
Source: ftp://ftp.debian.org/debian/pool/main/a/apmd/%{name}_%{version}.orig.tar.bz2
Source1: apmd.init
Source3: apmd_proxy
Patch0: apmd-3.2.2.orig-lib64.patch
Patch1: apmd-3.2.2.orig-graphicswitch.patch
Patch2: apmd-3.1.0.orig-optimization.patch
Patch5: apmd-3.2.2.orig-security.patch
Patch9: apmd-3.2.2.orig-proxy-timeout.patch
License: GPL
Group: System/Servers
BuildRequires:	X11-devel libxaw-devel
BuildRequires:	libtool
BuildRoot: %{_tmppath}/%{name}-root
Requires: common-licenses
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires: initscripts >= 5.5
ExclusiveArch: %{ix86} x86_64 ppc
Url: %{url}

%description
APMD is a set of programs for controlling the Advanced Power 
Management daemon and utilities found in most modern laptop 
computers. APMD can watch your notebook's battery and warn 
users when the battery is low. APMD is also capable of shutting 
down the PCMCIA sockets before a suspend.

Install the apmd package if you need to control the APM system 
on your laptop.

%package -n %{lib_name}
Summary: Main library for %{lib_name_orig}
Group: System/Libraries
Provides: %{lib_name_orig} = %{version}-%{release}

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with %{lib_name_orig}.

%package -n %{lib_name}-devel
Summary: Development library for %{lib_name_orig}
Group: Development/C
Requires: %{lib_name} = %{version}
Provides: %{lib_name_orig}-devel = %{version}-%{release}
Obsoletes: %{name}-devel
Provides: %{name}-devel

%description -n %{lib_name}-devel
This package contains the developmeent library needed to compile
programs that use %{lib_name_orig}.

%prep
%setup -q -n apmd-%{version}.orig
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch5 -p1
%patch9 -p1
echo "LIB = %_lib" > config.make

%build
%serverbuild
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s PROXY_DIR=%{_sbindir}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/apm-scripts

%makeinstall_std PREFIX=%{_prefix} MANDIR=%{_mandir}

for i in apm.1 apmsleep.1;do install -m644 $i -D $RPM_BUILD_ROOT/%{_mandir}/man1/$i;done
install -m644 apmd.8 -D $RPM_BUILD_ROOT/%{_mandir}/man8/apmd.8

install -m755 %{SOURCE1} -D $RPM_BUILD_ROOT%{_initrddir}/apmd
install -m755 %{SOURCE3} -D $RPM_BUILD_ROOT%{_sbindir}/apmd_proxy
rm -f $RPM_BUILD_ROOT%{_bindir}/on_ac_power

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%post 
%_post_service apmd

%preun
%_preun_service apmd

%triggerpostun -- apmd <= 3.0final-6
/sbin/chkconfig --add apmd

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README apmsleep.README
%{_mandir}/man?/*
%{_bindir}/*
%{_sbindir}/*
%config(noreplace) %{_initrddir}/apmd

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%{_libdir}/*so
%{_libdir}/*a
%{_includedir}/*


