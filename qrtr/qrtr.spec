Name:           qrtr
Version:        1.1
Release:        %autorelease
Summary:        Service listing daemon for Qualcomm IPC Router

# src/map.c is BSD-2-Clause, the rest is BSD-3-Clause
License:        BSD-3-Clause AND BSD-2-Clause
URL:            https://github.com/linux-msm/qrtr
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch1:         qrtr-restore-soname.patch

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  systemd

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
This package provides the userspace component for the Qualcomm IPC Router
protocol, which maintains a service listing and allows peforming lookups.

%package        libs
Summary:        Shared libraries for %{name}

%description    libs
This packages provides shared libraries for %{name}.

%package        devel
Summary:        Development headers and libraries for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
This packages provides development headers and libraries for %{name}.

%prep
%autosetup -p1

%build
%meson -Dsystemd-unit-prefix=%{_unitdir} -Dqrtr-ns=disabled
%meson_build

%install
%meson_install

%files
%{_bindir}/qrtr-cfg
%{_bindir}/qrtr-lookup

%files devel
%{_includedir}/libqrtr.h
%{_libdir}/libqrtr.so
%{_libdir}/pkgconfig/qrtr.pc

%files libs
%license LICENSE
%{_libdir}/libqrtr.so.1*

%changelog
%autochangelog
