%define shortname torrent-rasterbar
%define major 10
%define libname %mklibname %{shortname} %{major}
%define develname %mklibname %{shortname} -d
# Temporary workaroud for fix build for rasterbar 1.1.7/1.9. (penguin)
%define _disable_ld_no_undefined 1
#define _disable_lto 1

Summary:	The Rasterbar BitTorrent library
Name:		libtorrent-rasterbar
Version:	1.2.2
Release:	1
License:	BSD
Group:		System/Libraries
URL:		http://www.rasterbar.com/products/libtorrent/
Source0:	https://github.com/arvidn/libtorrent/releases/download/libtorrent-%(echo %{version}|sed -e 's,\.,_,g;s,_0$,,')/libtorrent-rasterbar-%{version}.tar.gz

BuildRequires:	boost-devel
BuildRequires:	boost-core-devel
BuildRequires:	boost-align-devel
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(geoip)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(zlib)

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

%description -n %{libname}
libtorrent-rasterbar is a C++ library that aims to be a good
alternative to all the other bittorrent implementations around. It is
a library and not a full featured client. It is not the same as the
other libtorrent, as used by the 'rtorrent' application, that is in
the 'libtorrent' package. The two are completely different and
incompatible.

%package -n python2-%{name}
Group:		System/Libraries
Summary:	The Rasterbar BitTorrent library's Python bindings
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	python-%{name} < 1.0.4-2
Provides:	python-%{name} = 1.0.4-2

%description -n python2-%{name}
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
Provides:	rb_libtorrent-devel = %{version}-%{release}
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
%apply_patches

%build

# LX3 build segfaults with clang 5.0 on i586 and x86_64
# Cooker/LX4 clang 7 failed for i686, just for it revert to gcc. Other arch stay with clang. (penguin)

%ifarch %{ix86}
export CC=gcc
export CXX=g++
%endif

# (tpg) a workaround for libtool crap
#sed -i 's/AC_CONFIG_MACRO_DIR(\[m4\])/dnl AC_CONFIG_MACRO_DIR(\[m4\])/' configure.in
#autoreconf -fi
export PYTHON=%{__python2}
export CXXFLAGS="%{optflags} -std=c++14"
%configure \
	--disable-static \
	--enable-python-binding \
	--with-zlib=system \
	--with-libgeoip=system \
	--enable-encryption \
	--enable-dht \
	--with-boost-libdir=%{_libdir}
#sed -i -e 's,$,-fno-lto,' bindings/python/compile_flags
%make_build

%install
%make_install

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_libdir}/*.so
%{_includedir}/libtorrent
%{_libdir}/pkgconfig/%{name}.pc

%files -n python2-%{name}
%{py2_platsitedir}/*.so
%{py2_platsitedir}/*.egg-info
