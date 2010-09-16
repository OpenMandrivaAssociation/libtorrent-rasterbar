%define shortname	torrent-rasterbar
%define major		6
%define libname		%mklibname %{shortname} %{major}
%define develname	%mklibname %{shortname} -d

Summary:	The Rasterbar BitTorrent library
Name:		libtorrent-rasterbar
Version:	0.15.3
Release:	%mkrel 1
License:	BSD
Group:		System/Libraries
URL:		http://www.rasterbar.com/products/libtorrent/
Source0:	http://libtorrent.googlecode.com/files/%{name}-%{version}.tar.gz
# http://bugs.archlinux.org/task/19072?cat=&dev=&sev=4&status=
Patch0:		disable-valloc.dpatch
BuildRequires:	boost-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	python-devel
BuildRequires:	libgeoip-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
libtorrent-rasterbar is a C++ library that aims to be a good
alternative to all the other bittorrent implementations around. It is
a library and not a full featured client. It is not the same as the
other libtorrent, as used by the 'rtorrent' application, that is in
the 'libtorrent' package. The two are completely different and
incompatible.

%package -n %{libname}
Group:		System/Libraries
Summary:	The Rasterbar BitTorrent library
Obsoletes:	%{mklibname %{shortname} 1}

%description -n %{libname}
libtorrent-rasterbar is a C++ library that aims to be a good
alternative to all the other bittorrent implementations around. It is
a library and not a full featured client. It is not the same as the
other libtorrent, as used by the 'rtorrent' application, that is in
the 'libtorrent' package. The two are completely different and
incompatible.

%package -n python-%{name}
Group:		System/Libraries
Summary:	The Rasterbar BitTorrent library's Python bindings
%{py_requires}
Requires:	%{libname} = %{version}-%{release}

%description -n python-%{name}
libtorrent-rasterbar is a C++ library that aims to be a good
alternative to all the other bittorrent implementations around. It is
a library and not a full featured client. It is not the same as the
other libtorrent, as used by the 'rtorrent' application, that is in
the 'libtorrent' package. The two are completely different and
incompatible. This package contains Python bindings.

%package -n %{develname}
Group:		Development/C
Summary:	The Rasterbar BitTorrent library's development headers
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
libtorrent-rasterbar is a C++ library that aims to be a good
alternative to all the other bittorrent implementations around. It is
a library and not a full featured client. It is not the same as the
other libtorrent, as used by the 'rtorrent' application, that is in
the 'libtorrent' package. The two are completely different and
incompatible. This package contains development libraries and headers.

%prep
%setup -q
%patch0 -p1

%build
# (tpg) a workaround for libtool crap
#sed -i 's/AC_CONFIG_MACRO_DIR(\[m4\])/dnl AC_CONFIG_MACRO_DIR(\[m4\])/' configure.in
#autoreconf -fi
%configure2_5x --disable-static \
	--enable-python-binding \
	--with-zlib=system \
	--with-libgeoip=system \
	--enable-encryption \
	--enable-dht \
	--with-boost-libdir=%{_libdir} \
	--with-boost-system=boost_system-mt \
	--with-boost-filesystem=boost_filesystem-mt \
	--with-boost-thread=boost_thread-mt \
	--with-boost-python=boost_python-mt
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{name} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.*a
%{_includedir}/libtorrent
%{_libdir}/pkgconfig/%{name}.pc

%files -n python-%{name}
%defattr(-,root,root)
%{py_platsitedir}/*.so
%{py_platsitedir}/*.egg-info


