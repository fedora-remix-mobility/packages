Name:		mobility-tweaks
Version:	0%{?commit:^%{date}git%{shortcommit}}
Release:	%autorelease
Summary:	A bunch of tweaks for mobile devices
License:	MIT

URL:		https://github.com/fedora-remix-mobility/packages/
Source1:	60-sensor-mobility.hwdb
Source2:	60-sensor-mobility.rules

BuildArch:      noarch	

BuildRequires:	systemd-rpm-macros
Requires:       systemd-udev

%description
A bunch of tweaks aimed at making mobile devices supported by the
Fedora Mobility efforts work. Those tweaks ideally should end up
upstream.

%install
install -D -m 644 %{SOURCE1} %{buildroot}%{_udevhwdbdir}/60-sensor-mobility.hwdb
install -D -m 644 %{SOURCE2} %{buildroot}%{_udevrulesdir}/60-sensor-mobility.rules

%files
%{_udevhwdbdir}/60-sensor-mobility.hwdb
%{_udevrulesdir}/60-sensor-mobility.rules

%changelog
%autochangelog
