Summary: Mapnik is an open source toolkit for developing mapping applications
Name: mapnik
Version: 3.0.21
Release: 1%{?dist}
License: LGPL
Group: Libraries/Geosciences
URL: https://github.com/rinigus/pkg-mapnik

Source: %{name}-%{version}.tar.gz
#Patch0:     mapnik.issue3384.patch
#Patch1:     mapnik.twkb.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++ harfbuzz-devel sqlite-devel
BuildRequires: pkgconfig(icu-uc)
BuildRequires: boost-devel freetype-devel
BuildRequires: libxml2-devel libjpeg-turbo-devel libpng-devel libtiff-devel cairo-devel
BuildRequires: proj-devel
Requires: proj

%description
Mapnik is basically a collection of geographic objects
like maps, layers, datasources, features, and geometries. The library
does not rely on any OS specific "windowing systems" and it can be
deployed to any server environment. It is intended to play fair in a
multi-threaded environment and is aimed primarily, but not
exclusively, at web-based development.


%package devel
Summary: Mapnik development headers
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: pkgconfig(icu-uc)
Requires: harfbuzz-devel sqlite-devel
Requires: boost-devel freetype-devel
Requires: libxml2-devel libjpeg-turbo-devel libpng-devel libtiff-devel cairo-devel
Requires: proj-devel

%description devel
This package provides headers for development


%package tools
Summary: Mapnik tools
Group: Libraries/Geosciences
Requires: %{name} = %{version}

%description tools
The package provides command line tools to test basic operations of mapnik

%prep
#%setup -q -n %{name}-%{version}/mapnik
rm -rf %{name}-%{version}
git clone --branch master --recurse-submodules -j8 %{url} %{name}-%{version}
tar -czf %{_sourcedir}/%{name}-%{version}.tar.gz %{name}-%{version}
cd %{name}-%{version}/mapnik
patch -p1 < ../rpm/mapnik.issue3384.patch
patch -p1 < ../rpm/mapnik.twkb.patch
sed -i 's/scons.py/scons.py CC=gcc/g' Makefile
sed -i 's/scons.py/scons.py CC=gcc/g' configure
#%patch0 -p1
#%patch1 -p1

%build
cd %{name}-%{version}/mapnik
JOBS=16 %{__make} clean || true
JOBS=16 %{__make} reset

%configure INPUT_PLUGINS="sqlite,shape" DESTDIR=%{buildroot} PREFIX="/usr" CUSTOM_CXXFLAGS="$CXXFLAGS -fPIC -g0" CUSTOM_CFLAGS="$CFLAGS -fPIC -g0" CUSTOM_LDFLAGS="$LDFLAGS" LINKING=shared OPTIMIZATION=2 CPP_TESTS=no CAIRO=no PLUGIN_LINKING=static MEMORY_MAPPED_FILE=no DEMO=no MAPNIK_INDEX=no MAPNIK_RENDER=no #ENABLE_STATS=True ENABLE_LOG=True 

#JOBS=16 %{__make} %{?_smp_mflags}

%install
cd %{name}-%{version}/mapnik
%{__rm} -rf %{buildroot}
JOBS=16 %{__make} install DESTDIR=%{buildroot}
cp -r deps/mapbox/variant/include/mapbox %{buildroot}/usr/include

%clean
%{__rm} -rf %{buildroot}

%pre

%post -n mapnik -p /sbin/ldconfig

%postun -n mapnik -p /sbin/ldconfig

%files
%files
%defattr(-, root, root, 0755)
%{_libdir}/libmapnik.so*
%{_libdir}/mapnik/fonts
%{_libdir}/mapnik/input

%files devel
%defattr(-, root, root, 0755)
%{_bindir}/mapnik-config
%{_includedir}/mapnik
%{_includedir}/mapbox
%{_libdir}/libmapnik-json.a
%{_libdir}/libmapnik-wkt.a
#%{_libdir}/libmapnik.a

%files tools
%defattr(-, root, root, 0755)
%{_bindir}/shapeindex

%changelog
* Mon Apr 3 2017 rinigus <rinigus.git@gmail.com> - 3.0.13-1
- initial packaging release for SFOS

