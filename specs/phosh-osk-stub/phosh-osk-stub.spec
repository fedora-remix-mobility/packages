%global _schemaid sm.puri.phosh.osk
%global _desktopid mobi.phosh.OskStub

Name:    phosh-osk-stub
Version: 0.45.0
Release: 1%{?dist}
Summary: An alternative OSK for Phosh

License: GPL-3.0-or-later
URL:     https://gitlab.gnome.org/guidog/phosh-osk-stub
Source:  %{url}/-/archive/v%{version_no_tilde _}/%{name}-v%{version_no_tilde _}.tar.gz

ExcludeArch: %{ix86}

BuildRequires: /usr/bin/xvfb-run
BuildRequires: /usr/bin/rst2man
BuildRequires: desktop-file-utils
BuildRequires: meson
BuildRequires: gcc

BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gmobile)
BuildRequires: pkgconfig(gnome-desktop-3.0)
BuildRequires: pkgconfig(gsettings-desktop-schemas) >= 47
BuildRequires: pkgconfig(gtk+-3.0) > 3.24.35
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(libfeedback-0.0)
BuildRequires: pkgconfig(libhandy-1) >= 1.1.90
BuildRequires: pkgconfig(wayland-protocols)

Provides: phosh-osk
Provides: %{_datadir}/applications/sm.puri.OSK0.desktop

Requires: gsettings-desktop-schemas >= 47
Requires(post): %{_sbindir}/alternatives
Requires(postun): %{_sbindir}/alternatives

%description
%{summary}. It can replace the default OSK squeekboard.

%prep
%setup -q -n %{name}-v%{version_no_tilde _}

%build
%meson -Ddefault_osk=false -Dman=true
%meson_build

%install
%meson_install
%find_lang %{name}

# desktop-file-validate doesn't recognize Phosh as a valid session
# So just yeet the OnlyShowIn= line, for now
# TODO: remove when desktop-file-utils is updated to 0.28 and carries a
# patch for adding Phosh as a valid registered OnlyShowIn= environment
# https://gitlab.freedesktop.org/xdg/desktop-file-utils/-/merge_requests/24
sed -i -e '/^OnlyShowIn=/d' %{buildroot}%{_datadir}/applications/%{_desktopid}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{_desktopid}.desktop
xvfb-run sh <<HERE
%meson_test
HERE

%post
alternatives --install \
    %{_datadir}/applications/sm.puri.OSK0.desktop \
    phosh-osk \
    %{_datadir}/applications/%{_desktopid}.desktop \
    1

%preun
if [ $1 -eq 0 ] ; then
  alternatives --remove \
    phosh-osk \
    %{_datadir}/applications/%{_desktopid}.desktop
fi

%files -f %{name}.lang
%ghost %{_datadir}/applications/sm.puri.OSK0.desktop
%{_bindir}/phosh-osk-stub
%{_datadir}/%{name}/completers/hunspell.completer
%{_datadir}/%{name}/layouts.json
%{_datadir}/applications/%{_desktopid}.desktop
%{_datadir}/glib-2.0/schemas/%{_schemaid}.gschema.xml
%{_datadir}/glib-2.0/schemas/%{_schemaid}.enums.xml
%{_datadir}/metainfo/%{_desktopid}.metainfo.xml
%{_mandir}/man1/phosh-osk-stub.1.gz

%changelog
%autochangelog
