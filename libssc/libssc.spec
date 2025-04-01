Name:           libssc
Version:        0.2.2
Release:        %autorelease
Summary:        Library to expose Qualcomm Sensor Core sensors

License:        GPL-3.0-or-later
URL:            https://codeberg.org/DylanVanAssche/libssc
Source:         %{url}/archive/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  systemd
BuildRequires:  pkgconfig(libprotobuf-c)
BuildRequires:  pkgconfig(glib)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(qmi-glib)
BuildRequires:  pkgconfig(qrtr)
BuildRequires:  pkgconfig(udev)

%description
%{summary}.

%package devel
Summary:	Development headers for libssc
Requires:	%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%package -n python3-ssc
Summary:    Python bindings for libssc
Requires:   %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-ssc
%{summary}.

%prep
%autosetup -p1 -n %{name}

%build
%meson
%meson_build

%install
%meson_install

%files
%{_bindir}/ssc-server
%{_bindir}/ssc-server-tests
%{_bindir}/ssccli
%{_libdir}/%{name}.so.0

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files -n python3-ssc
%pycached %{python3_sitelib}/qmi.py
%pycached %{python3_sitelib}/ssc.py

%changelog
%autochangelog
