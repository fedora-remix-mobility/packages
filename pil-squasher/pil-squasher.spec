%global srcname pil-squasher
%global date 20240611
%global commit 3c9f8b8756ba6e4dbf9958570fd4c9aea7a70cf4
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}

Name:		pil-squasher
Version:	0%{?commit:^%{date}git%{shortcommit}}
Release:	%autorelease
Summary:	MTD to MBN firmware converter tool
License:	BSD-3-Clause

URL:		https://github.com/linux-msm/pil-squasher
Source:		%{url}/archive/%{commit}/%{commit}.tar.gz#/%{srcname}-%{commit}.tar.gz

BuildRequires:	gcc

%description	
pil-squasher takes a split firmware image (mdt + bXX files) and squash them into a single mbn
firmware image, preserving signature et al.

%prep
%autosetup -n %{srcname}-%{commit}

%build
make CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"
	
%install
make prefix="%{_prefix}" DESTDIR="%{buildroot}" install
	
%files
%doc README.md LICENSE
%{_bindir}/pil-splitter
%{_bindir}/pil-squasher
	
%changelog
%autochangelog
