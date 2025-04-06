Name:           buffyboard
Version:        3.2.0
Release:        %autorelease
Summary:        Touch-enabled on-screen keyboard for virtual terminals

License:        GPL-3.0-or-later
URL:            https://gitlab.postmarketos.org/postmarketOS/buffybox
Source:         https://gitlab.com/-/project/52322952/uploads/88ff83972a3c19d16d9d2560bfae8a7e/buffybox-3.2.0.tar.gz

# This can be dropped once a newer release is published
Source:         buffyboard.service

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  systemd-rpm-macros

%description
Buffyboard is a touch-enabled on-screen keyboard running on the Linux
framebuffer. It uses LVGL for input processing and rendering.

%prep
%autosetup -n buffybox-%{version}/buffyboard
cp ../COPYING ./

%build
# Once a newer release is published: -Dman=true -Dwith-drm=true
#   -Dsystemd-buffyboard-service=true -Dsystemd-password-agent=true
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
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%changelog
%autochangelog
