%define shortname	torrent-rasterbar
%define major		1
%define libname		%mklibname %{shortname} %{major}
%define develname	%mklibname %{shortname} -d

Summary:	The Rasterbar BitTorrent library
Name:		libtorrent-rasterbar
Version:	0.14.1
Release:	%mkrel 4
License:	BSD
Group:		System/Libraries
Source0:	http://downloads.sourceforge.net/libtorrent/%{name}-%{version}.tar.gz
Patch0:		libtorrent-rasterbar-0.14.1-underlink.patch
URL:		http://www.rasterbar.com/products/libtorrent/
Buildroot:	%{_tmppath}/%{name}-root
BuildRequires:	boost-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	python-devel

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

%package -n python-%{name}
Group:		System/Libraries
Summary:	The Rasterbar BitTorrent library's Python bindings
%{py_requires}

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
%patch0 -p1 -b .underlink

%build
autoreconf -fiv
%configure2_5x --enable-python-binding \
	--with-asio=system \
	--with-boost-libdir=%{_libdir} \
	--with-boost-system=boost_system-mt \
	--with-boost-filesystem=boost_filesystem-mt \
	--with-boost-thread=boost_thread-mt \
	--with-boost-regex=boost_regex-mt \
	BOOST_PYTHON_LIB='boost_python-mt'
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
