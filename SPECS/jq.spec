Summary: lightweight and flexible command-line JSON processor
Name: jq
Version:    1.5
Release: 1%{?dist}
License: MIT
Group: System/Utilities
URL: https://github.com/rinigus/pkg-jq

Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc flex bison libtool autoconf

%description
jq is a lightweight and flexible command-line JSON processor.

%package devel
Summary: JQ development headers
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
This package provides headers for development

%prep
#%setup -q -n %{name}-%{version}/jq
rm -rf %{name}-%{version}
git clone --recurse-submodules -j8 %{url}.git %{name}-%{version}
tar -czf %{_sourcedir}/%{name}-%{version}.tar.gz %{name}-%{version}
cd %{name}-%{version}

%build
%{__make} clean || true
cd %{name}-%{version}/jq
autoreconf -fi

CFLAGS="$CFLAGS -fPIC"
CXXFLAGS="$CXXFLAGS -fPIC"
%configure --disable-static

%{__make} %{?_smp_mflags}

%install
cd %{name}-%{version}/jq
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%pre

%post -n jq -p /sbin/ldconfig

%postun -n jq -p /sbin/ldconfig


%files
%files
%defattr(-, root, root, 0755)
%{_bindir}/jq
%{_libdir}/libjq.so*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/jq.h
%{_includedir}/jv.h
%{_libdir}/libjq.la
%{_mandir}/man1/*
%{_datadir}/doc/jq

%changelog
* Thu May 18 2017 rinigus <rinigus.git@gmail.com> - 1.5-1
- initial packaging release for SFOS

