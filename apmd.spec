%define major	1
%define libname	%mklibname apm %{major}
%define devname	%mklibname apm -d

Summary:	Advanced Power Management (APM) BIOS utilities for laptops
Name:		apmd
Version:	3.2.2
Release:	38
License:	GPLv2+
Group:		System/Servers
Url:		ftp://ftp.debian.org/debian/pool/main/a/apmd
Source0:	ftp://ftp.debian.org/debian/pool/main/a/apmd/%{name}_%{version}.orig.tar.gz
Source1:	apmd.init
Source3:	apmd_proxy
Patch0:		apmd-3.2.2.orig-lib64.patch
Patch1:		apmd-3.2.2.orig-graphicswitch.patch
Patch2:		apmd-3.2.2.orig-optimization.patch
Patch5:		apmd-3.2.2.orig-security.patch
Patch9:		apmd-3.2.2.orig-proxy-timeout.patch
Patch10:	apmd-3.2.2-libtool.patch

BuildRequires:	libtool
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xt)
Requires(post,preun):	rpm-helper
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
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{devname}
Summary:	Development library for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the developmeent library needed to compile
programs that use %{name}.

%prep
%setup -qn apmd-%{version}.orig
%apply_patches

echo "LIB = %{_lib}" > config.make

%build
%serverbuild
make CFLAGS="%{optflags}" LDFLAGS="%{ldflags} -s" PROXY_DIR=%{_sbindir}

%install
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/apm-scripts

%makeinstall_std PREFIX=%{_prefix} MANDIR=%{_mandir}

for i in apm.1 apmsleep.1;
	do install -m644 $i -D %{buildroot}/%{_mandir}/man1/$i;
done
install -m644 apmd.8 -D %{buildroot}/%{_mandir}/man8/apmd.8

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/apmd
install -m755 %{SOURCE3} -D %{buildroot}%{_sbindir}/apmd_proxy
rm -f %{buildroot}%{_bindir}/on_ac_power

%post
%_post_service apmd

%preun
%_preun_service apmd

%files
%doc AUTHORS ChangeLog README apmsleep.README
%config(noreplace) %{_initrddir}/apmd
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man?/*

%files -n %{libname}
%{_libdir}/libapm.so.%{major}*

%files -n %{devname}
%{_libdir}/*so
%{_includedir}/*

