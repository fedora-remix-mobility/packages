Name:           qbootctl
Version:        0.2.2
Release:        %autorelease
Summary:        CLI tool for manipulating A/B slots on Android devices

License:        GPL-3.0-or-later
URL:            https://github.com/linux-msm/qbootctl
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Source:         qbootctl.service

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  systemd-rpm-macros

%description
%{summary}. It is a port of the original Android bootctrl HAL developed by
Qualcomm, modified to build on Linux and provide a friendly CLI interface.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
install -Dm644 %{SOURCE1} -t %{buildroot}%{_unitdir}/

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%changelog
%autochangelog
