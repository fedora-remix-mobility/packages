Name:           bootmac
Version:        0.6.0
Release:        1%{?dist}
Summary:        Configures the MAC addresses of WLAN and Bluetooth interfaces at boot

License:        GPL-3.0-or-later
URL:            https://gitlab.postmarketos.org/postmarketOS/bootmac/
Source:         https://gitlab.postmarketos.org/postmarketOS/bootmac/-/archive/v%{version}/bootmac-v%{version}.tar.gz

%description
%{summary}.

%global debug_package %{nil}
%prep
%autosetup -n bootmac-v%{version}

%install
install -Dm755 bootmac -t %{buildroot}%{_bindir}/
install -Dm644 bootmac-bluetooth.service -t %{buildroot}%{_unitdir}/
install -Dm644 bootmac-wifi.rules -T %{buildroot}%{_udevrulesdir}/70-bootmac-wifi.rules

%files
%license LICENSE
%{_bindir}/bootmac
%{_unitdir}/bootmac-bluetooth.service
%{_udevrulesdir}/70-bootmac-wifi.rules

%changelog
%autochangelog
