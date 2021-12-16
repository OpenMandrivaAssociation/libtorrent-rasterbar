%define shortname torrent-rasterbar
%define major 2
%define libname %mklibname %{shortname} %{major}
%define develname %mklibname %{shortname} -d
# Temporary workaroud for fix build for rasterbar 1.1.7/1.9. (penguin)
%define _disable_ld_no_undefined 1

Summary:	The Rasterbar BitTorrent library
Name:		libtorrent-rasterbar
Version:	2.0.5
Release:	3
License:	BSD
Group:		System/Libraries
URL:		http://www.rasterbar.com/products/libtorrent/
Source0:	https://github.com/arvidn/libtorrent/releases/download/libtorrent-%(echo %{version}|sed -e 's,\.,_,g;s,_0$,,')/libtorrent-rasterbar-%{version}.tar.gz

# Upstream patch to fix build with boost 1.78
Patch0: https://patch-diff.githubusercontent.com/raw/arvidn/libtorrent/pull/6597.patch

BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	boost-core-devel
BuildRequires:	boost-align-devel
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(geoip)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  pkgconfig(python)
BuildRequires:	python3dist(setuptools)

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
Group:		System/Libraries

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
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	python-%{name} < 1.0.4-2
Provides:	python-%{name} = %{EVRD}

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
%autosetup -p1

mkdir -p build-aux
touch build-aux/config.rpath

%build
export PYTHON=%{__python}
export CXXFLAGS="%{optflags} -std=c++14"
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="/usr" \
    -Dpython-bindings=ON \
    -Dboost-python-module-name="python" \
	-Dpython-egg-info=ON \
	-Dpython-install-system-dir=ON

%make_build

%install
%make_install -C build

#Fix for python
sed -i 's/^Version:.*/Version: %{version}/' %{buildroot}%{python_sitearch}/libtorrent.egg-info/PKG-INFO

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_libdir}/*.so
%{_libdir}/cmake/LibtorrentRasterbar/LibtorrentRasterbar*
%{_includedir}/libtorrent
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/cmake/Modules/FindLibtorrentRasterbar.cmake

%files -n python-%{name}
%{python_sitearch}/libtorrent.cpython-*.so
%{python_sitearch}/libtorrent.egg-info
