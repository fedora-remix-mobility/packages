Name:           pd-mapper
Version:        1.0
Release:        %autorelease
Summary:        Service listing daemon for Qualcomm IPC Router

License:        BSD-3-Clause
URL:            https://github.com/andersson/pd-mapper
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# Makefile: allow $(CFLAGS), $(LDFLAGS) override
Patch:          %{url}/commit/a500e63481425013cb4023a67181c4434a18c56e.patch
# correct SIGSEGV when firmware is not present
Patch:          %{url}/commit/b4c1e362f16c8426f32778fadb4d578bb2ef0f2f.patch
# ANDROID: pd-mapper: Use /vendor/firmware path for AOSP
Patch:          %{url}/commit/352a39cd0c265ca522d9e2889f84246195355ac1.patch
# pd-mapper: Add ability to decompress .xz json files
Patch:          %{url}/commit/10997ba7c43a3787a40b6b1b161408033e716374.patch
# pd-mapper.service: don't start if /sys/class/remoteproc is empty
# https://github.com/linux-msm/pd-mapper/pull/15
# Patch:          0001-pd-mapper.service-don-t-start-if-sys-class-remotepro.patch

Patch:          https://patch-diff.githubusercontent.com/raw/linux-msm/pd-mapper/pull/14.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  systemd-rpm-macros

BuildRequires:  qrtr-devel
BuildRequires:  xz-devel
Requires:       qrtr

%description
This package provides the userspace component for the Qualcomm IPC Router
protocol, which maintains a service listing and allows peforming lookups.

%prep
%autosetup -p1

%build
%make_build prefix="%{_prefix}"

%install
%make_install prefix="%{_prefix}"

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
