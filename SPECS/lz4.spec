Summary: Extremely Fast Compression algorithm
Name: lz4
Version: 1.8.1.2
Release: 1%{?dist}
License: BSD-type license
Group: Libraries/Databases
URL: https://github.com/rinigus/pkg-lz4

Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++
#Requires: pango

%description
LZ4 is lossless compression algorithm

%package devel
Summary: lz4 development headers and static library
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
LZ4 is lossless compression algorithm. This
package provides libraries and headers for development

%package tools
Summary: lz4 tools
Group: Development/Libraries
Requires: %{name} = %{version}

%description tools
LZ4 is lossless compression algorithm. This
package provides tools

%prep
#%setup -q -n %{name}-%{version}/lz4
rm -rf %{name}-%{version}
git clone --recurse-submodules -j8  %{url}.git %{name}-%{version}
tar -czf %{_sourcedir}/%{name}-%{version}.tar.gz /dev/null
cd %{name}-%{version}/lz4


%build
cd %{name}-%{version}/lz4
#make %{?_smp_mflags}
%{__make} clean || true

CFLAGS="$CFLAGS -fPIC"
CXXFLAGS="$CXXFLAGS -fPIC"

%{__make} prefix=/usr %{?_smp_mflags} CC=gcc

%install
cd %{name}-%{version}/lz4
%{__rm} -rf %{buildroot}
%{__make} install prefix=/usr DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%pre

%post -n lz4 -p /sbin/ldconfig

%postun -n lz4 -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
# %exclude %{_defaultdocdir}/snappy
%{_libdir}/liblz4.so.*
%exclude %{_mandir}/man1/*lz4*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/lz4*.h
%{_libdir}/liblz4.a
%{_libdir}/liblz4.so
%{_libdir}/pkgconfig/liblz4.pc
# %exclude %{_libdir}/libsnappy.la

%files tools
%defattr(-, root, root, 0755)
%{_bindir}/lz4*
%{_bindir}/unlz4

%changelog
* Thu Mar 29 2018 rinigus <rinigus.git@gmail.com> - 1.8.1.2
- initial packaging release for SFOS

