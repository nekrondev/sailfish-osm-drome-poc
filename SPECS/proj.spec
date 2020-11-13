Summary: Standard UNIX filter function which converts geographic coordinates
Name: proj
Version: 4.9.3
Release: 1%{?dist}
License: MIT
Group: Libraries/Geo
URL: https://github.com/rinigus/pkg-proj

#Source: http://download.osgeo.org/proj/proj-4.9.3.tar.gz
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++ libtool

%description
proj.4 is a standard UNIX filter function which converts geographic longitude and latitude coordinates into cartesian coordinates (and vice versa), and it is a C API for software developers to include coordinate transformation in 
their own software.

%package devel
Summary: proj.4 development headers and static library
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
proj.4 is a standard UNIX filter function which converts geographic coordinates. Development package

%package tools
Summary: proj.4 tools
Group: Libraries/Databases
Requires: %{name} = %{version}

%description tools
proj.4 is a standard UNIX filter function which converts geographic coordinates. Tools package

%prep

#%setup -q -n %{name}-%{version}/proj.4
rm -rf cd %{name}-%{version}
git clone --recurse-submodules -j8 %{url}.git %{name}-%{version}
tar -czf %{_sourcedir}/%{name}-%{version}.tar.gz /dev/null
cd %{name}-%{version}/proj.4

%build
cd %{name}-%{version}/proj.4
%{__make} clean || true
./autogen.sh

CFLAGS="$CFLAGS -fPIC"
CXXFLAGS="$CXXFLAGS -fPIC"
%configure 

%{__make} %{?_smp_mflags}

%install
cd %{name}-%{version}/proj.4
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%pre

%post -n proj -p /sbin/ldconfig

%postun -n proj -p /sbin/ldconfig

%files
%files
%defattr(-, root, root, 0755)
%{_libdir}/libproj.so
%{_libdir}/libproj.so.12
%{_libdir}/libproj.so.12.0.0
%{_datarootdir}/proj

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/geodesic.h
%{_includedir}/org_proj4_PJ.h
%{_includedir}/org_proj4_Projections.h
%{_includedir}/proj_api.h
%{_includedir}/projects.h
%{_libdir}/libproj.a
%{_libdir}/libproj.la
%{_libdir}/pkgconfig/proj.pc

%files tools
%defattr(-, root, root, 0755)
%{_bindir}/cs2cs
%{_bindir}/geod
%{_bindir}/invgeod
%{_bindir}/invproj
%{_bindir}/nad2bin
%{_bindir}/proj
%{_mandir}/man1/cs2cs.1.gz
%{_mandir}/man1/geod.1.gz
%{_mandir}/man1/proj.1.gz
%{_mandir}/man3/geodesic.3.gz
%{_mandir}/man3/pj_init.3.gz

%changelog
* Thu Apr 10 2017 rinigus <rinigus.git@gmail.com> - 1.2.76
- initial packaging release for SFOS

