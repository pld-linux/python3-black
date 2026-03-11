#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	The uncompromising code formatter
Summary(pl.UTF-8):	Bezkompromisowe narzędzie do formatowania kodu
Name:		python3-black
Version:	26.3.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/black/
Source0:	https://files.pythonhosted.org/packages/source/b/black/black-%{version}.tar.gz
# Source0-md5:	c01dce43efd71a7754ffd9cc3234fe89
URL:		https://pypi.org/project/black/
BuildRequires:	python3-build
BuildRequires:	python3-hatch-fancy-pypi-readme
BuildRequires:	python3-hatch-vcs >= 0.3.0
BuildRequires:	python3-hatchling >= 1.27.0
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-wheel >= 0.45.1
%if %{with tests}
BuildRequires:	python3-aiohttp >= 3.10
BuildRequires:	python3-click >= 8.1.7
BuildRequires:	python3-mypy_extensions >= 0.4.3
BuildRequires:	python3-packaging >= 22.0
BuildRequires:	python3-pathspec >= 1.0.0
BuildRequires:	python3-platformdirs >= 2
BuildRequires:	python3-pytest >= 7
#BuildRequires:	python3-pytest-cov >= 4.1.0
#BuildRequires:	python3-pytest-xdist >= 3.0.2
BuildRequires:	python3-pytokens >= 0.4.0
BuildRequires:	python3-pytokens < 0.5
%if "%{py3_ver}" == "3.10"
BuildRequires:	python3-tomli >= 1.1.0
BuildRequires:	python3-typing_extensions >= 4.0.1
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-docutils >= 0.21.2
BuildRequires:	python3-furo >= 2025.12.19
BuildRequires:	python3-myst_parser >= 4.0.1
BuildRequires:	python3-sphinx_copybutton >= 0.5.2
BuildRequires:	python3-sphinxcontrib-programoutput >= 0.19
BuildRequires:	sphinx-pdg-3 >= 8.2.3
%endif
Requires:	python3-modules >= 1:3.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Black is the uncompromising Python code formatter. By using it, you
agree to cede control over minutiae of hand-formatting. In return,
Black gives you speed, determinism, and freedom from pycodestyle
nagging about formatting. You will save time and mental energy for
more important matters.

%description -l pl.UTF-8
Black to bezkompromisowe narzędzie do formatowania kodu w Pythonie.
Używając go, zgadzamy się na scedowanie kontroli nad szczegółami
ręcznego formatowania. W zamian Black daje szybkość, determinizm i
wolność od narzekania pycodestyle na temat formatowania. Oszczędza
czas i siły mentalne na ważniejsze kwestie.

%package apidocs
Summary:	API documentation for Black module
Summary(pl.UTF-8):	Dokumentacja API modułu Black
Group:		Documentation

%description apidocs
API documentation for Black module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Black.

%prep
%setup -q -n black-%{version}

%build
%py3_build_pyproject

%if %{with tests} || %{with doc}
# metadata required for test_schema and sphinx
%{__python3} -m zipfile -e build-3/*.whl build-3-test
%endif

%if %{with tests}
# 3 tests require "black" binary in path, prepare stub
install -d test-bin
cat >test-bin/black <<EOF
#!%{__python3}
from black import patched_main
patched_main()
EOF
chmod 755 test-bin/black
# test_target_version_exceeds_runtime_warning: CliRunner doens't catch warning from black.main, don't know why
PATH="$(pwd)/test-bin:$PATH" \
PYTHONPATH=$(pwd)/build-3-test \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests -k 'not test_target_version_exceeds_runtime_warning'
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3-test \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGES.md LICENSE README.md SECURITY.md
%attr(755,root,root) %{_bindir}/black
%attr(755,root,root) %{_bindir}/blackd
%{py3_sitescriptdir}/black
%{py3_sitescriptdir}/blackd
%{py3_sitescriptdir}/blib2to3
%{py3_sitescriptdir}/_black_version.py
%{py3_sitescriptdir}/_black_version.pyi
%{py3_sitescriptdir}/__pycache__/_black_version.cpython-*.py[co]
%{py3_sitescriptdir}/black-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,contributing,guides,integrations,the_black_code_style,usage_and_configuration,*.html,*.js}
%endif
