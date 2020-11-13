
Name: libosmscout-qt

Summary: libosmscout qt libraries
Version: 0.0.git.20170521
Release: 1
Group: Qt/Qt
License: LGPL
URL: https://github.com/rinigus/libosmscout
Source0:    %{name}-%{version}.tar.bz2

#Requires: protobuf
Requires: libmarisa
#Requires: cairo
#Requires: pango

BuildRequires: cmake
BuildRequires: pkgconfig(Qt5Core) pkgconfig(Qt5Gui) pkgconfig(Qt5Widgets) pkgconfig(Qt5Quick)
#BuildRequires: protobuf-devel
BuildRequires: libxml2-devel
BuildRequires: libmarisa-devel
#BuildRequires: cairo-devel
#BuildRequires: pango-devel

%description
libosmscout qt libraries

%package devel
Summary: libosmscout qt development header files
Group: Development/Libraries
#Requires: %{name} = %{version}

%description devel
libosmscout qt libraries - development files


%prep
#%setup -q -n %{name}-%{version}
rm -rf %{name}-%{version}
git clone --recurse-submodules -j8 %{url} %{name}-%{version}
tar -czf %{_sourcedir}/%{name}-%{version}.tar.gz %{name}-%{version}
cd %{name}-%{version}

%build
cd %{name}-%{version}
mkdir build-rpm
cd build-rpm
%cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILD_SHARED_LIBS=false -DBUILD_WITH_OPENMP=OFF -DOSMSCOUT_BUILD_MAP_OPENGL=OFF -DOSMSCOUT_BUILD_IMPORT=OFF -DOSMSCOUT_BUILD_MAP_AGG=OFF -DOSMSCOUT_BUILD_MAP_CAIRO=OFF -DOSMSCOUT_BUILD_MAP_SVG=OFF -DOSMSCOUT_BUILD_MAP_IOSX=OFF -DOSMSCOUT_BUILD_TESTS=OFF -DOSMSCOUT_BUILD_DEMOS=OFF -DOSMSCOUT_BUILD_BINDING_JAVA=OFF -DOSMSCOUT_BUILD_BINDING_CSHARP=OFF -DOSMSCOUT_BUILD_DOC_API=OFF -DOSMSCOUT_BUILD_CLIENT_QT=ON -DOSMSCOUT_BUILD_TOOL_OSMSCOUT2=OFF -DOSMSCOUT_BUILD_TOOL_STYLEEDITOR=OFF -DGPERFTOOLS_USAGE=OFF -DOSMSCOUT_BUILD_TOOL_IMPORT=OFF -DOSMSCOUT_BUILD_TOOL_DUMPDATA=OFF ..
make %{?_smp_mflags}
cd ..

%install
cd %{name}-%{version}/build-rpm
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot}
cd ..

%check
ctest -V %{?_smp_mflags}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
# %{_libdir}/libosmscout.so
# #%{_libdir}/libosmscout_import.so
# %{_libdir}/libosmscout_map.so
# %{_libdir}/libosmscout_map_qt.so
# %{_libdir}/libosmscout_client_qt.so
# #%{_libdir}/libosmscout_map_cairo.so
%{_datadir}/stylesheets

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/osmscout
%{_libdir}/libosmscout.a
#%{_libdir}/libosmscout_import.a
%{_libdir}/libosmscout_map.a
%{_libdir}/libosmscout_map_qt.a
%{_libdir}/libosmscout_client_qt.a
#%{_libdir}/libosmscout_map_cairo.a

