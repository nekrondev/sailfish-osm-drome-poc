Summary: MARISA: Matching Algorithm with Recursively Implemented StorAge
Name: libmarisa
Version: 0.2.4
Release: 1%{?dist}
License: LGPL and BSD 2-clause license
Group: Libraries/Databases
URL: https://github.com/rinigus/pkg-marisa

#Source: https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/marisa-trie/marisa-0.2.4.tar.gz
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++
#Requires: pango

%description
Matching Algorithm with Recursively Implemented StorAge (MARISA) is a
space-efficient trie data structure. libmarisa is a C++ library for an
implementation of MARISA. Users can build dictionaries and search keys
from the dictionaries. The package also provides command line tools to
test basic operations of libmarisa, and the tools are useful to test
the performance.


%package devel
Summary: MARISA development headers and static library
Group: Development/Libraries
#Requires: %{name} = %{version}

%description devel
Matching Algorithm with Recursively Implemented StorAge (MARISA) is a
space-efficient trie data structure. This package provides libraries
and headers for development

%package tools
Summary: MARISA tools
Group: Libraries/Databases
Requires: %{name} = %{version}

%description tools
Matching Algorithm with Recursively Implemented StorAge (MARISA) is a
space-efficient trie data structure. The package provides command line
tools to test basic operations of libmarisa, and the tools that are
useful to test the performance.

%prep

#%setup -q -n %{name}-%{version}/marisa-trie
git clone --recurse-submodules -j8 %{url}.git %{name}-%{version}
tar -czf %{_sourcedir}/%{name}-%{version}.tar.gz /dev/null
cd %{name}-%{version}/marisa-trie

%build
cd %{name}-%{version}/marisa-trie
%{__make} clean || true

CFLAGS="$CFLAGS -fPIC"
CXXFLAGS="$CXXFLAGS -fPIC"
%configure 

%{__make} %{?_smp_mflags}

%install
cd %{name}-%{version}/marisa-trie
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%pre

%post -n libmarisa -p /sbin/ldconfig

%postun -n libmarisa -p /sbin/ldconfig

%files
%files
%defattr(-, root, root, 0755)
%{_libdir}/libmarisa.so
%{_libdir}/libmarisa.so.0
%{_libdir}/libmarisa.so.0.0.0

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/marisa
%{_includedir}/marisa.h
%{_libdir}/libmarisa.a
%{_libdir}/libmarisa.la
%{_libdir}/pkgconfig/marisa.pc

%files tools
%defattr(-, root, root, 0755)
%{_bindir}/marisa-*

%changelog
* Sat Oct 1 2016 rinigus <rinigus.git@gmail.com> - 0.2.4-1
- initial packaging release for SFOS
