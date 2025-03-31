Name:       hexagonrpc
Version:    0.3.2
Release:    0.1%{?dist}
Summary:    FastRPC ioctl wrapper and a reverse tunnel

License:    GPLv3+
URL:        https://github.com/linux-msm/hexagonrpc/
Source0:    https://github.com/linux-msm/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Source of those sources: https://gitlab.postmarketos.org/postmarketOS/pmaports/-/tree/master/extra-repos/systemd/systemd-services
Source1:    hexagonrpcd-adsp-rootpd.service
Source2:    hexagonrpcd-adsp-sensorspd.service
Source3:    hexagonrpcd-sdsp.service

Source4:    sysusers.conf

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  systemd-rpm-macros
BuildRequires:  systemd-rpm-macros
Requires(post): systemd

%{?sysusers_requires_compat}

%description
FastRPC ioctl wrapper and a reverse tunnel

FastRPC is used to communicate with the Context Hub Runtime Environment,
a program on the DSP that manages sensors, and to serve files to remote
processors.

%package devel
Summary: Libraries and header files for %{name} development 
	
Requires: %{name} = %{version}-%{release}

%description devel
	
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build
%meson
%meson_build

%install
%meson_install

# Install header files, so they can be taken by the devel package
mkdir -p %{buildroot}%{_includedir}
cp -a include/libhexagonrpc %{buildroot}%{_includedir}

# Install systemd units
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/hexagonrpcd-adsp-rootpd.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/hexagonrpcd-adsp-sensorspd.service
install -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/hexagonrpcd-sdsp.service
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysusersdir}/fastrpc.conf

%pre
%sysusers_create_compat %{SOURCE3}

%post
%systemd_post hexagonrpcd-adsp-rootpd.service
%systemd_post hexagonrpcd-adsp-sensorspd.service
%systemd_post hexagonrpcd-sdsp.service

%preun
%systemd_preun hexagonrpcd-adsp-rootpd.service
%systemd_preun hexagonrpcd-adsp-sensorspd.service
%systemd_preun hexagonrpcd-sdsp.service

%postun
%systemd_postun_with_restart hexagonrpcd-adsp-rootpd.service
%systemd_postun_with_restart hexagonrpcd-adsp-sensorspd.service
%systemd_postun_with_restart hexagonrpcd-sdsp.service

%files
%doc README.md
%license COPYING
%{_unitdir}/*.service
%{_bindir}/hexagonrpcd
%{_libdir}/libhexagonrpc.so
%{_libexecdir}/hexagonrpc
%{_sysusersdir}/fastrpc.conf

%files devel
%{_includedir}/libhexagonrpc

%changelog
* Mon May 13 2024 marcin - 0.3.2-0.1
- Initial packaging
