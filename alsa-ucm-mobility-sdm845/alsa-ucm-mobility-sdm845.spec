%global srcname alsa-ucm-conf
%global date 20240408
%global commit de81252f28465fb76e2aa58eb9733b88de2076ea
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}

Name:		alsa-ucm-mobility-sdm845
Version:	0%{?commit:^%{date}git%{shortcommit}}
Release:	%autorelease
Summary:	ALSA Use Case Manager configuration (and topologies) for SDM845 mobile phones
License:	BSD-3-Clause

URL:		https://gitlab.com/sdm845-mainline/alsa-ucm-conf
Source:		%{url}/-/archive/%{commit}/%{srcname}-%{commit}.tar.gz

# This list is generated using the following command. The commit referenced is the last commit
# in this tree that is not related to SDM845 phones:
#
#    git diff 23adf5a368abe9009f44547b91d60a244f735d81.. |
#      grep '+++' |
#      cut -d/ -f2- |
#      grep -v ucm2/Qualcomm/sdm845/HiFi-MM1.conf
Source2:	alsa-ucm-mobility-sdm845.files

BuildArch:      noarch	
	
Requires:       alsa-ucm >= 1.2.7.2 
	
%description	
The ALSA Use Case Manager configuration (and topologies) for SDM845 mobile phones 

%prep
%autosetup -n %{srcname}-%{commit}
	
%install
cat %{SOURCE2} | while read FILE; do
  mkdir -p "%{buildroot}%{_datadir}/alsa/$(dirname "$FILE")"
  cp -a "$FILE" "%{buildroot}%{_datadir}/alsa/$FILE"
done
	
%files
%{_datadir}/alsa/ucm2/Google/*
%{_datadir}/alsa/ucm2/OnePlus/*
%{_datadir}/alsa/ucm2/SHIFT/*
%{_datadir}/alsa/ucm2/Samsung/*
%{_datadir}/alsa/ucm2/Xiaomi/*
%{_datadir}/alsa/ucm2/conf.d/sdm845/*
	
%changelog
%autochangelog
