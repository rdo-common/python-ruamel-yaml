%global pypi_name ruamel.yaml
%global pname ruamel-yaml
%global commit f29921d2048e

%global with_python3 1

Name:           python-%{pname}
Version:        0.13.14
Release:        1%{?dist}
Summary:        YAML 1.2 loader/dumper package for Python 

License:        MIT
URL:            https://bitbucket.org/ruamel/yaml
#Source0:        https://files.pythonhosted.org/packages/source/r/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Use bitbucket sources so we can run the tests
Source0:        https://bitbucket.org/ruamel/yaml/get/%{version}.tar.gz#/%{pname}-%{version}.tar.gz
# Works with pytest 2.7
Patch0:         python-ruamel-yaml-pytest27.patch
 
BuildRequires:  libyaml-devel

%description
ruamel.yaml is a YAML 1.2 loader/dumper package for Python.
It is a derivative of Kirill Simonov’s PyYAML 3.11

%package -n     python2-%{pname}
Summary:        YAML 1.2 loader/dumper package for Python 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
# For tests
BuildRequires:  pytest
BuildRequires:  python2-ruamel-ordereddict
BuildRequires:  python2-typing >= 3.5.2.2-2
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python2-ruamel-ordereddict
Requires:       python2-typing >= 3.5.2.2-2
Requires:       python-setuptools

%description -n python2-%{pname}
ruamel.yaml is a YAML 1.2 loader/dumper package for Python.
It is a derivative of Kirill Simonov’s PyYAML 3.11

%if 0%{?with_python3}
%package -n     python%{python3_pkgversion}-%{pname}
Summary:        YAML 1.2 loader/dumper package for Python 
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# For tests
BuildRequires:  python%{python3_pkgversion}-pytest
# typing was added in Python 3.5
%if %{python3_pkgversion} == 34
BuildRequires:  python%{python3_pkgversion}-typing
%endif
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

Requires:       python%{python3_pkgversion}-setuptools
%if %{python3_pkgversion} == 34
Requires:       python%{python3_pkgversion}-typing
%endif

%description -n python%{python3_pkgversion}-%{pname}
ruamel.yaml is a YAML 1.2 loader/dumper package for Python.
It is a derivative of Kirill Simonov’s PyYAML 3.11
%endif

%prep
%autosetup -n %{pname}-%{commit} -p1
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%{__python3} setup.py install --single-version-externally-managed --skip-build --root $RPM_BUILD_ROOT
%endif

%{__python2} setup.py install --single-version-externally-managed --skip-build --root $RPM_BUILD_ROOT

%check
%ifarch aarch64
# Appears to fail in pytest on aarch64 for some reason
PYTHONPATH=$(echo build/lib.*%{python2_version}) py.test-%{python2_version} _test/test_*.py || :
%else
PYTHONPATH=$(echo build/lib.*%{python2_version}) py.test-%{python2_version} _test/test_*.py
%endif
%if 0%{?with_python3}
PYTHONPATH=$(echo build/lib.*%{python3_version}) py.test-%{python3_version} _test/test_*.py
%endif

%files -n python2-%{pname}
%license LICENSE
%doc README.rst
%{python2_sitearch}/ruamel
%{python2_sitearch}/_ruamel_yaml.so
%{python2_sitearch}/%{pypi_name}-%{version}-py?.?-*.pth
%{python2_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{pname}
%license LICENSE
%doc README.rst
%{python3_sitearch}/ruamel
%{python3_sitearch}/_ruamel_yaml.cpython-*
%{python3_sitearch}/%{pypi_name}-%{version}-py?.?-*.pth
%{python3_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Wed Aug 9 2017 Orion Poplawski <orion@nwra.com> - 0.13.14-1
- Update to 0.13.14

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 13 2017 Jan Chaloupka <jchaloup@redhat.com> - 0.13.13-3
- The ruamel.yaml needs at least typing >= 3.5.2.2
  related: #1386563

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 0.13.13-1
- Update to 0.13.13

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 0.12.14-7
- Add patch to support pytest 2.7 in EPEL7

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.12.14-6
- Rebuild for Python 3.6

* Wed Oct 26 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.14-5
- Require python34-typing on EPEL
- Ignore python2 test failure due to old pytest on EPEL7

* Wed Oct 26 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.14-4
- Build python3 package
- Run tests

* Tue Oct 25 2016 Chandan Kumar <chkumar@redhat.com> - 0.12.14-3
- Disabling python3 as python3-ruamel-ordereddict not available

* Mon Oct 24 2016 Chandan Kumar <chkumar@redhat.com> - 0.12.14-2
- Fixed python2-typing runtime dependency issue

* Fri Oct 14 2016 Chandan Kumar <chkumar@redhat.com> - 0.12.14-1
- Initial package.
