%define name		apmd
%define libname_orig	libapm
%define major		1
%define libname		%mklibname apm %{major}
%define develname	%mklibname apm -d

Summary:	Advanced Power Management (APM) BIOS utilities for laptops
Name:		apmd
Version:	3.2.2
Release:	28
License:	GPLv2+
Group:		System/Servers
Source:		ftp://ftp.debian.org/debian/pool/main/a/apmd/%{name}_%{version}.orig.tar.bz2
Source1:	apmd.init
Source3:	apmd_proxy
Patch0:		apmd-3.2.2.orig-lib64.patch
Patch1:		apmd-3.2.2.orig-graphicswitch.patch
Patch2:		apmd-3.2.2.orig-optimization.patch
Patch5:		apmd-3.2.2.orig-security.patch
Patch9:		apmd-3.2.2.orig-proxy-timeout.patch
Patch10:	apmd-3.2.2-libtool.patch
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xt)
BuildRequires:	libtool

Requires(post):		rpm-helper
Requires(preun):	rpm-helper

Requires:	initscripts

%description
APMD is a set of programs for controlling the Advanced Power 
Management daemon and utilities found in most modern laptop 
computers. APMD can watch your notebook's battery and warn 
users when the battery is low. APMD is also capable of shutting 
down the PCMCIA sockets before a suspend.

Install the apmd package if you need to control the APM system 
on your laptop.

%package -n %{libname}
Summary:	Main library for %{libname_orig}
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{libname_orig}.

%package -n %{develname}
Summary:	Development library for %{libname_orig}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains the developmeent library needed to compile
programs that use %{libname_orig}.

%prep
%setup -q -n apmd-%{version}.orig
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch5 -p1
%patch9 -p1
%patch10 -p1
echo "LIB = %{_lib}" > config.make

%build
%serverbuild
make CFLAGS="%{optflags}" LDFLAGS="%{ldflags} -s" PROXY_DIR=%{_sbindir}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/apm-scripts

%makeinstall_std PREFIX=%{_prefix} MANDIR=%{_mandir}

for i in apm.1 apmsleep.1;do install -m644 $i -D %{buildroot}/%{_mandir}/man1/$i;done
install -m644 apmd.8 -D %{buildroot}/%{_mandir}/man8/apmd.8

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/apmd
install -m755 %{SOURCE3} -D %{buildroot}%{_sbindir}/apmd_proxy
rm -f %{buildroot}%{_bindir}/on_ac_power

%post
%_post_service apmd

%preun
%_preun_service apmd

%triggerpostun -- apmd <= 3.0final-6
/sbin/chkconfig --add apmd

%files
%doc AUTHORS ChangeLog README apmsleep.README
%{_mandir}/man?/*
%{_bindir}/*
%{_sbindir}/*
%config(noreplace) %{_initrddir}/apmd

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{develname}
%{_libdir}/*so
%{_includedir}/*

%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 3.2.2-27mdv2011.0
+ Revision: 662784
- mass rebuild

* Wed Feb 02 2011 Funda Wang <fwang@mandriva.org> 3.2.2-26
+ Revision: 634995
- rebuild
- tighten BR

