%global gvc_commit 5f9768a2eac29c1ed56f1fbb449a77a3523683b6
%global libcall_ui_version 0.1.4

Name:		phosh
Version:	0.45.0
Release:	%autorelease
Summary:	Graphical shell for mobile devices
License:	GPL-3.0-or-later
URL:		https://gitlab.gnome.org/World/Phosh/phosh
Source:	https://gitlab.gnome.org/World/Phosh/phosh/-/archive/v%{version}/%{name}-v%{version}.tar.gz
# This library doesn't compile into a DSO nor has any tagged releases.
# Other projects such as gnome-shell use it this way.
Source:	https://gitlab.gnome.org/GNOME/libgnome-volume-control/-/archive/%{gvc_commit}/libgnome-volume-control-%{gvc_commit}.tar.gz
# Similar situation as gvc
Source:	https://gitlab.gnome.org/World/Phosh/libcall-ui/-/archive/v%{libcall_ui_version}/libcall-ui-v%{libcall_ui_version}.tar.gz
Source:	phosh

ExcludeArch:	i686

BuildRequires:	gcc
BuildRequires:	meson
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(libecal-2.0) >= 3.33.1
BuildRequires:	pkgconfig(libedataserver-1.2) >= 3.33.1
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(gcr-3) >= 3.7.5
BuildRequires:	pkgconfig(glib-2.0) >= 2.76
BuildRequires:	pkgconfig(gio-2.0) >= 2.76
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.76
BuildRequires:	pkgconfig(gmobile) >= 0.1.0
BuildRequires:	pkgconfig(gnome-bluetooth-3.0) >= 46.0
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.26
BuildRequires:	pkgconfig(gobject-2.0) >= 2.76
BuildRequires:	pkgconfig(gsettings-desktop-schemas) >= 47
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.24.36
BuildRequires:	pkgconfig(gtk+-wayland-3.0) >= 3.22
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libfeedback-0.0) >= 0.4.0
BuildRequires:	pkgconfig(libhandy-1) >= 1.8.0
BuildRequires:	pkgconfig(libnm) >= 1.14
BuildRequires:	pkgconfig(polkit-agent-1) >= 0.122
BuildRequires:	pkgconfig(libsoup-3.0) >= 3.6
BuildRequires:	pkgconfig(libsystemd) >= 241
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(upower-glib) >= 0.99.1
BuildRequires:	pkgconfig(wayland-client) >= 1.14
BuildRequires:	pkgconfig(wayland-protocols) >= 1.12
BuildRequires:	pkgconfig(gtk4) >= 4.12
BuildRequires:	pkgconfig(libadwaita-1) >= 1.6
BuildRequires:	pkgconfig(evince-document-3.0)
BuildRequires:	pkgconfig(evince-view-3.0)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libpulse) >= 12.99.3
BuildRequires:	pkgconfig(libpulse-mainloop-glib)
BuildRequires:	pkgconfig(libcallaudio-0.1)
BuildRequires:	pkgconfig(mm-glib)
BuildRequires:	/usr/bin/xvfb-run
BuildRequires:	/usr/bin/xauth
BuildRequires:	dbus-daemon
BuildRequires:	desktop-file-utils
BuildRequires:	systemd-rpm-macros

Requires:	phoc >= 0.45.0
Requires:	iio-sensor-proxy
Requires:	gnome-session
Requires:	gnome-shell
Requires:	lato-fonts
Requires:	hicolor-icon-theme
Requires:	phosh-osk

Recommends:	squeekboard >= 1.21.0
Recommends:	phosh-mobile-settings

%description
Phosh is a simple shell for Wayland compositors speaking the layer-surface
protocol. It currently supports

* a lockscreen
* brightness control and nightlight
* the GCR system-prompter interface
* acting as a polkit auth agent
* enough of org.gnome.Mutter.DisplayConfig to make gnome-settings-daemon happy
* a homebutton that toggles a simple favorites menu
* status icons for battery, wwan and wifi

%package devel
Summary:	Development headers for Phosh
Requires:	%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
Development headers for Phosh.

%package -n libphosh
Summary:    Experimental library of Phosh components and functionality.
Requires:   %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n libphosh
Experimental shared library of Phosh components and functionality, allowing
other projects to embed Phosh.

%package -n libphosh-devel
Summary:    Development headers for libphosh.
Requires:   lib%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n libphosh-devel
Development headers for libphosh.

%prep
%setup -a1 -a2 -q -n %{name}-v%{version}

mv libgnome-volume-control-%{gvc_commit} subprojects/gvc
mv libcall-ui-v%{libcall_ui_version} subprojects/libcall-ui

%build
%meson -Dphoc_tests=disabled -Dbindings-lib=true
%meson_build

%install
install -d %{buildroot}%{_sysconfdir}/pam.d/
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/

install -d %{buildroot}%{_datadir}/applications
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE4}

%meson_install
%find_lang %{name}

%{__install} -Dpm 0644 data/phosh.service %{buildroot}%{_unitdir}/phosh.service
rm %{buildroot}%{_libdir}/libphosh-0.45.a

%check
desktop-file-validate \
%{buildroot}%{_datadir}/applications/mobi.phosh.Shell.desktop
LC_ALL=C.UTF-8 xvfb-run sh <<'SH'
%meson_test
SH

%files -f %{name}.lang
%{_bindir}/phosh-session
%{_libexecdir}/phosh
%{_libexecdir}/phosh-calendar-server
%{_datadir}/applications/mobi.phosh.Shell.desktop
%{_datadir}/glib-2.0/schemas/mobi.phosh.shell.gschema.xml
%{_datadir}/glib-2.0/schemas/mobi.phosh.shell.enums.xml
%{_datadir}/glib-2.0/schemas/00_mobi.Phosh.gschema.override
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.plugins.ticket-box.gschema.xml
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.plugins.launcher-box.gschema.xml
%{_datadir}/glib-2.0/schemas/sm.puri.phosh.plugins.upcoming-events.gschema.xml
%{_datadir}/glib-2.0/schemas/mobi.phosh.plugins.pomodoro.gschema.xml
%{_datadir}/gnome-session/sessions/phosh.session
%{_datadir}/wayland-sessions/phosh.desktop
%{_datadir}/phosh
%{_sysconfdir}/pam.d/phosh
%{_unitdir}/phosh.service
%{_userunitdir}/gnome-session@phosh.target.d/session.conf
%{_userunitdir}/mobi.phosh.Shell.service
%{_userunitdir}/mobi.phosh.Shell.target
%{_datadir}/xdg-desktop-portal/portals/phosh-shell.portal
%{_datadir}/xdg-desktop-portal/phosh-portals.conf
%{_datadir}/icons/hicolor/symbolic/apps/mobi.phosh.Shell-symbolic.svg
%{_datadir}/dbus-1/services/mobi.phosh.Shell.CalendarServer.service
%{_libdir}/phosh/plugins/caffeine-quick-setting.plugin
%{_libdir}/phosh/plugins/calendar.plugin
%{_libdir}/phosh/plugins/dark-mode-quick-setting.plugin
%{_libdir}/phosh/plugins/emergency-info.plugin
%{_libdir}/phosh/plugins/launcher-box.plugin
%{_libdir}/phosh/plugins/mobile-data-quick-setting.plugin
%{_libdir}/phosh/plugins/night-light-quick-setting.plugin
%{_libdir}/phosh/plugins/simple-custom-quick-setting.plugin
%{_libdir}/phosh/plugins/ticket-box.plugin
%{_libdir}/phosh/plugins/upcoming-events.plugin
%{_libdir}/phosh/plugins/wifi-hotspot-quick-setting.plugin
%{_libdir}/phosh/plugins/pomodoro-quick-setting.plugin
%{_libdir}/phosh/plugins/scaling-quick-setting.plugin
%{_libdir}/phosh/plugins/libphosh-plugin-caffeine-quick-setting.so
%{_libdir}/phosh/plugins/libphosh-plugin-calendar.so
%{_libdir}/phosh/plugins/libphosh-plugin-dark-mode-quick-setting.so
%{_libdir}/phosh/plugins/libphosh-plugin-emergency-info.so
%{_libdir}/phosh/plugins/libphosh-plugin-launcher-box.so
%{_libdir}/phosh/plugins/libphosh-plugin-mobile-data-quick-setting.so
%{_libdir}/phosh/plugins/libphosh-plugin-night-light-quick-setting.so
%{_libdir}/phosh/plugins/libphosh-plugin-simple-custom-quick-setting.so
%{_libdir}/phosh/plugins/libphosh-plugin-ticket-box.so
%{_libdir}/phosh/plugins/libphosh-plugin-upcoming-events.so
%{_libdir}/phosh/plugins/libphosh-plugin-wifi-hotspot-quick-setting.so
%{_libdir}/phosh/plugins/libphosh-plugin-pomodoro-quick-setting.so
%{_libdir}/phosh/plugins/libphosh-plugin-scaling-quick-setting.so
%{_libdir}/phosh/plugins/prefs/libphosh-plugin-prefs-emergency-info.so
%{_libdir}/phosh/plugins/prefs/libphosh-plugin-prefs-ticket-box.so
%{_libdir}/phosh/plugins/prefs/libphosh-plugin-prefs-upcoming-events.so
%{_libdir}/phosh/plugins/prefs/libphosh-plugin-prefs-pomodoro-quick-setting.so

%doc README.md
%license COPYING

%files devel
%{_datadir}/gir-1.0/Phosh-0.gir
%{_includedir}/phosh
%{_libdir}/pkgconfig/phosh-plugins.pc
%{_libdir}/pkgconfig/phosh-settings.pc

%files -n libphosh
%{_libdir}/girepository-1.0/Phosh-0.typelib
%{_libdir}/libphosh-0.45.so.0

%files -n libphosh-devel
%{_includedir}/libphosh-0.45
%{_libdir}/libphosh-0.45.so
%{_libdir}/pkgconfig/libphosh-0.45.pc

%changelog
%autochangelog
