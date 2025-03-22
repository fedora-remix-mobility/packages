Name:		squeekboard
Version:	1.43.1
Release:	%autorelease
Summary:	a Wayland virtual keyboard

# The entire source is GPL-3.0-or-later, except:
#
# GPL-2.0-or-later:
#   - eek/*, except eek/layersurface.{c,h} which are still GPL-3.0-or-later
# HPND-sell-variant:
#   - protocols/text-input-unstable-v3.xml
#   - protocols/wlr-layer-shell-unstable-v1.xml
# LGPL-2.0-or-later:
#   - src/style.rs
# MIT:
#   - protocols/input-method-unstable-v2.xml
#   - protocols/virtual-keyboard-unstable-v1.xml
# MIT OR Apache-2.0:
#   - src/assert_matches.rs
#   - src/float_ord.rs
SourceLicense:	%{shrink:
                GPL-3.0-or-later AND
                HPND-sell-variant AND
                LGPL-2.0-or-later AND
                MIT AND
                (MIT OR Apache-2.0)
                }
# This includes everything from SourceLicense, plus the licenses of Rust
# libraries statically linked into the executable. To obtain the following
# list of licenses, build the package and note the output of
# %%{cargo_license_summary}. A full breakdown is in LICENSES.dependencies.
#
# Apache-2.0 OR BSL-1.0
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-2-Clause OR Apache-2.0 OR MIT
# MIT
# MIT OR Apache-2.0
# MIT OR Apache-2.0 OR Zlib
# Unlicense OR MIT
License:	%{shrink:
                GPL-3.0-or-later AND
                HPND-sell-variant AND
                LGPL-2.0-or-later AND
                MIT AND
                (Apache-2.0 OR BSL-1.0) AND
                (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
                (BSD-2-Clause OR Apache-2.0 OR MIT) AND
                (MIT OR Apache-2.0) AND
                (MIT OR Apache-2.0 OR Zlib) AND
                (Unlicense OR MIT)
                }
URL:		https://gitlab.gnome.org/World/Phosh/squeekboard
Source0:	https://gitlab.gnome.org/World/Phosh/squeekboard/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
Source1:	squeekboard.desktop
# treewide: Upgrade zbus to 4.x
# https://gitlab.gnome.org/World/Phosh/squeekboard/-/merge_requests/709
Patch:		%{url}/-/merge_requests/709.patch

BuildRequires:	gcc
BuildRequires:	meson
BuildRequires:	rust-packaging
BuildRequires:	pkgconfig(gio-2.0) >= 2.26
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0
BuildRequires:	pkgconfig(wayland-client) >= 1.14
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(wayland-protocols) >= 1.12
BuildRequires:	pkgconfig(libfeedback-0.0)
BuildRequires:	pkgconfig(libbsd)
BuildRequires:	desktop-file-utils

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

%description
Squeekboard is a virtual keyboard supporting Wayland, built primarily
for the Librem 5 phone. It squeaks because some Rust got inside.

%package phosh-osk-provider
Summary:  Use squeekboard as Phosh's default OSK
BuildArch: noarch
Requires: %{name}
Provides: phosh-osk = 1.0

%description phosh-osk-provider
%{summary}.

%prep
%autosetup -p1 -n %{name}-v%{version}
%cargo_prep

rm -f Cargo.lock
%generate_buildrequires
%cargo_generate_buildrequires -a

%build
# ensure standard Rust compiler flags are set
export RUSTFLAGS="%build_rustflags"
%meson
%meson_build

%cargo_license_summary
%{cargo_license} > LICENSE.dependencies

%install
%meson_install
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart/
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/autostart/
chmod +x %{buildroot}%{_bindir}/squeekboard-entry

cp tools/squeekboard-restyled %{buildroot}%{_bindir}
chmod +x %{buildroot}%{_bindir}/squeekboard-restyled

# TODO: remove when desktop-file-utils is updated with this MR:
# https://src.fedoraproject.org/rpms/desktop-file-utils/pull-request/4
sed -i 's/Phosh/X-Phosh/g' %{buildroot}%{_datadir}/applications/sm.puri.Squeekboard.desktop
sed -i 's/X-X-Phosh/X-Phosh/g' %{buildroot}%{_datadir}/applications/sm.puri.Squeekboard.desktop

ln -s sm.puri.Squeekboard.desktop \
      %{buildroot}%{_datadir}/applications/sm.puri.OSK0.desktop

%find_lang %{name}

%check
# ensure standard Rust compiler flags are set
export RUSTFLAGS="%build_rustflags"
%meson_test
desktop-file-validate %{buildroot}/%{_datadir}/applications/sm.puri.Squeekboard.desktop

%files -f %{name}.lang
%{_bindir}/squeekboard
%{_bindir}/squeekboard-entry
%{_bindir}/squeekboard-test-layout
%{_bindir}/squeekboard-restyled
%{_datadir}/applications/sm.puri.Squeekboard.desktop
%{_datadir}/glib-2.0/schemas/sm.puri.Squeekboard.gschema.xml
%{_sysconfdir}/xdg/autostart/squeekboard.desktop
%doc README.md
%license COPYING LICENSE.dependencies

%files phosh-osk-provider
%{_datadir}/applications/sm.puri.OSK0.desktop

%changelog
%autochangelog
