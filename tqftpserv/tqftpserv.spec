Name:           tqftpserv
Version:        1.1
Release:        %autorelease
Summary:        Trivial File Transfer Protocol server over AF_QIPCRTR

License:        BSD-3-Clause
URL:            https://github.com/linux-msm/tqftpserv
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# tqftpserv.service.in: remove dependency on qrtr-ns.service
Patch:          https://github.com/linux-msm/tqftpserv/pull/24.patch

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(qrtr)
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros

%description
%{summary}.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%changelog
%autochangelog
