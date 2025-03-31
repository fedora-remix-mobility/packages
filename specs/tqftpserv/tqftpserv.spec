Name:           tqftpserv
Version:        1.1
Release:        %autorelease
Summary:        Trivial File Transfer Protocol server over AF_QIPCRTR

License:        BSD-3-Clause
URL:            https://github.com/linux-msm/tqftpserv
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  systemd
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(qrtr)

%description
%{summary}.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%changelog
%autochangelog
