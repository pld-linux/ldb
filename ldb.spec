#
# Conditional build:
%bcond_without	lmdb	# LMDB module (64-bit only)
%bcond_without	python2	# CPython 2.x interface
#
%ifnarch %{x8664} aarch64 alpha mips64 ppc64 s390x sparc64
# lmdb support requires 64-bit size_t
%undefine	with_lmdb
%endif
%define		talloc_version	2:2.1.14
%define		tdb_version	2:1.3.16
%define		tevent_version	0.9.37
Summary:	LDAP-like embedded database
Summary(pl.UTF-8):	Wbudowana baza danych podobna do LDAP
Name:		ldb
Version:	1.5.4
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	https://www.samba.org/ftp/ldb/%{name}-%{version}.tar.gz
# Source0-md5:	24d9f18b085ba27f96d4dec643abea39
URL:		https://ldb.samba.org/
BuildRequires:	cmocka-devel >= 1.1.3
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt-progs
%{?with_lmdb:BuildRequires:	lmdb-devel >= 0.9.16}
BuildRequires:	openldap-devel
BuildRequires:	popt-devel >= 1.6
%if %{with python2}
BuildRequires:	python-devel >= 1:2.4.2
BuildRequires:	python-talloc-devel >= %{talloc_version}
BuildRequires:	python-tdb >= %{tdb_version}
BuildRequires:	python-tevent >= %{tevent_version}
%endif
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-talloc-devel >= %{talloc_version}
BuildRequires:	python3-tdb >= %{tdb_version}
BuildRequires:	python3-tevent >= %{tevent_version}
BuildRequires:	rpmbuild(macros) >= 1.507
BuildRequires:	talloc-devel >= %{talloc_version}
BuildRequires:	tdb-devel >= %{tdb_version}
BuildRequires:	tevent-devel >= %{tevent_version}
%{?with_lmdb:Requires:	lmdb >= 0.9.16}
Requires:	talloc >= %{talloc_version}
Requires:	tdb >= %{tdb_version}
Requires:	tevent >= %{tevent_version}
Requires:	popt >= 1.6
Provides:	libldb = %{version}-%{release}
Obsoletes:	libldb < 1.1.0-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# %{_includedir}/pyldb.h shared between python*-ldb-devel
%define		_duplicate_files_terminate_build	0

%description
An extensible library that implements an LDAP like API to access
remote LDAP servers, or use local tdb databases.

%description -l pl.UTF-8
Rozszerzalna biblioteka implementująca API podobne do LDAP pozwalające
na dostęp do zdalnych serwerów LDAP lub wykorzystanie lokalnych baz
danych tdb.

%package tools
Summary:	Tools to manage LDB files
Summary(pl.UTF-8):	Narzędzia do zarządzania plikami LDB
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}

%description tools
Tools to manage LDB files.

%description tools -l pl.UTF-8
Narzędzia do zarządzania plikami LDB.

%package devel
Summary:	Header files for the LDB library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LDB
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	talloc-devel >= %{talloc_version}
Requires:	tdb-devel >= %{tdb_version}
Requires:	tevent-devel >= %{tevent_version}
Provides:	libldb-devel = %{version}-%{release}
Obsoletes:	libldb-devel < 1.1.0-3

%description devel
Header files needed to develop programs that link against the LDB
library.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do tworzenia programów wykorzystujących
bibliotekę LDB.

%package -n python-ldb
Summary:	Python 2 bindings for the LDB library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki LDB
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs >= 1:2.4.2
Requires:	python-tdb >= %{tdb_version}
Obsoletes:	pyldb

%description -n python-ldb
Python 2 bindings for the LDB library.

%description -n python-ldb -l pl.UTF-8
Wiązania Pythona 2 do biblioteki LDB.

%package -n python-ldb-devel
Summary:	Development files for the Python 2 bindings for the LDB library
Summary(pl.UTF-8):	Pliki programistyczne wiązań Pythona 2 do biblioteki LDB
Group:		Development/Libraries
Requires:	python-ldb = %{version}-%{release}

%description -n python-ldb-devel
Development files for the Python 2 bindings for the LDB library.

%description -n python-ldb-devel -l pl.UTF-8
Pliki programistyczne wiązań Pythona 2 do biblioteki LDB.

%package -n python3-ldb
Summary:	Python 3 bindings for the LDB library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki LDB
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-tdb >= %{tdb_version}
Obsoletes:	pyldb

%description -n python3-ldb
Python 3 bindings for the LDB library.

%description -n python3-ldb -l pl.UTF-8
Wiązania Pythona 3 do biblioteki LDB.

%package -n python3-ldb-devel
Summary:	Development files for the Python 3 bindings for the LDB library
Summary(pl.UTF-8):	Pliki programistyczne wiązań Pythona 3 do biblioteki LDB
Group:		Development/Libraries
Requires:	python3-ldb = %{version}-%{release}

%description -n python3-ldb-devel
Development files for the Python 3 bindings for the LDB library.

%description -n python3-ldb-devel -l pl.UTF-8
Pliki programistyczne wiązań Pythona 3 do biblioteki LDB.

%prep
%setup -q

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--with-modulesdir=%{_libdir}/ldb/modules \
	--with-privatelibdir=%{_libdir}/ldb \
	--bundled-libraries=NONE \
	--disable-rpath \
	--disable-rpath-install \
	%{?with_python2:--extra-python=%{__python}}

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python2}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n python-ldb -p /sbin/ldconfig
%postun	-n python-ldb -p /sbin/ldconfig

%post	-n python3-ldb -p /sbin/ldconfig
%postun	-n python3-ldb -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libldb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libldb.so.1
%dir %{_libdir}/ldb
%attr(755,root,root) %{_libdir}/ldb/libldb-key-value.so
%attr(755,root,root) %{_libdir}/ldb/libldb-tdb-err-map.so
%attr(755,root,root) %{_libdir}/ldb/libldb-tdb-int.so
%{?with_lmdb:%attr(755,root,root) %{_libdir}/ldb/libldb-mdb-int.so}
%dir %{_libdir}/ldb/modules
%dir %{_libdir}/ldb/modules/ldb
%attr(755,root,root) %{_libdir}/ldb/modules/ldb/*.so

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ldbadd
%attr(755,root,root) %{_bindir}/ldbdel
%attr(755,root,root) %{_bindir}/ldbedit
%attr(755,root,root) %{_bindir}/ldbmodify
%attr(755,root,root) %{_bindir}/ldbrename
%attr(755,root,root) %{_bindir}/ldbsearch
%attr(755,root,root) %{_libdir}/ldb/libldb-cmdline.so
%{_mandir}/man1/ldbadd.1*
%{_mandir}/man1/ldbdel.1*
%{_mandir}/man1/ldbedit.1*
%{_mandir}/man1/ldbmodify.1*
%{_mandir}/man1/ldbrename.1*
%{_mandir}/man1/ldbsearch.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libldb.so
%{_includedir}/ldb_module.h
%{_includedir}/ldb_handlers.h
%{_includedir}/ldb_errors.h
%{_includedir}/ldb_version.h
%{_includedir}/ldb.h
%{_pkgconfigdir}/ldb.pc
%{_mandir}/man3/ldb.3*

%if %{with python2}
%files -n python-ldb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyldb-util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpyldb-util.so.1
%attr(755,root,root) %{py_sitedir}/ldb.so
%{py_sitedir}/_ldb_text.py[co]

%files -n python-ldb-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyldb-util.so
%{_includedir}/pyldb.h
%{_pkgconfigdir}/pyldb-util.pc
%endif

%files -n python3-ldb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyldb-util.cpython-3*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpyldb-util.cpython-3*.so.1
%attr(755,root,root) %{py3_sitedir}/ldb.cpython-*.so
%{py3_sitedir}/_ldb_text.py
%{py3_sitedir}/__pycache__/_ldb_text.cpython-*.py[co]

%files -n python3-ldb-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyldb-util.cpython-3*.so
%{_includedir}/pyldb.h
%{_pkgconfigdir}/pyldb-util.cpython-3*.pc
