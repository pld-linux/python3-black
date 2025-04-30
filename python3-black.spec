#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	The uncompromising code formatter
Summary(pl.UTF-8):	Bezkompromisowe narzędzie do formatowania kodu
Name:		python3-black
Version:	25.1.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/black/
Source0:	https://files.pythonhosted.org/packages/source/b/black/black-%{version}.tar.gz
# Source0-md5:	2a33335756996e5948e8063677068f24
URL:		https://pypi.org/project/black/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
%if %{with tests}
BuildRequires:	python3-aiohttp >= 3.10
BuildRequires:	python3-appdirs
BuildRequires:	python3-click >= 8.1.7
BuildRequires:	python3-hatchling
BuildRequires:	python3-hatch-fancy-pypi-readme
BuildRequires:	python3-hatch-vcs
BuildRequires:	python3-mypy_extensions >= 0.4.3
BuildRequires:	python3-pathspec >= 0.9.0
BuildRequires:	python3-pathspec < 1
BuildRequires:	python3-pytest >= 6.1.1
#BuildRequires:	python3-pytest-cases >= 2.3.0
#BuildRequires:	python3-pytest-cov >= 2.11.1
BuildRequires:	python3-pytest-mock >= 3.3.1
#BuildRequires:	python3-pytest-xdist >= 2.2.1
BuildRequires:	python3-regex >= 2020.1.8
BuildRequires:	python3-toml >= 0.10.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-myst_parser >= 0.14.0
BuildRequires:	python3-sphinx_copybutton >= 0.3.1
BuildRequires:	python3-sphinxcontrib-programoutput >= 0.17
BuildRequires:	sphinx-pdg-3 >= 3.5.4
%endif
Requires:	python3-modules >= 1:3.8
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

%if %{with tests}
# 3 tests require "black" binary in path, prepare stub
install -d test-bin
cat >test-bin/black <<EOF
#!%{__python3}
from black import patched_main
patched_main()
EOF
chmod 755 test-bin/black
PATH="$(pwd)/test-bin:$PATH" \
PYTHONPATH=$(pwd)/src \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
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
%doc CHANGES.md LICENSE README.md
%attr(755,root,root) %{_bindir}/black
%attr(755,root,root) %{_bindir}/blackd
%{py3_sitescriptdir}/black
%{py3_sitescriptdir}/blackd
%{py3_sitescriptdir}/blib2to3
%{py3_sitescriptdir}/_black_version.py
%{py3_sitescriptdir}/__pycache__/_black_version.cpython-*.py[co]
%{py3_sitescriptdir}/black-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,contributing,guides,integrations,the_black_code_style,usage_and_configuration,*.html,*.js}
%endif
