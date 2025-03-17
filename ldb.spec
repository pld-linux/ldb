# NOTE: since samba 4.21.0 (ldb 2.10.0) ldb is built as a part of samba.spec
#
# Conditional build:
%bcond_without	lmdb	# LMDB module (64-bit only)
#
%ifnarch %{x8664} aarch64 alpha mips64 ppc64 s390x sparc64
# lmdb support requires 64-bit size_t
%undefine	with_lmdb
%endif
%define		talloc_version	2:2.4.2
%define		tdb_version	2:1.4.10
%define		tevent_version	0.16.1
Summary:	LDAP-like embedded database
Summary(pl.UTF-8):	Wbudowana baza danych podobna do LDAP
Name:		ldb
Version:	2.9.2
Release:	2
License:	LGPL v3+
Group:		Libraries
Source0:	https://download.samba.org/pub/ldb/%{name}-%{version}.tar.gz
# Source0-md5:	843644a43c0fc8342ff704230edd00c7
URL:		https://ldb.samba.org/
BuildRequires:	cmocka-devel >= 1.1.3
BuildRequires:	docbook-style-xsl
BuildRequires:	docbook-style-xsl-nons
BuildRequires:	libbsd-devel
BuildRequires:	libxslt-progs
%{?with_lmdb:BuildRequires:	lmdb-devel >= 0.9.16}
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.6
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-talloc-devel >= %{talloc_version}
BuildRequires:	python3-tdb >= %{tdb_version}
BuildRequires:	python3-tevent >= %{tevent_version}
BuildRequires:	rpmbuild(macros) >= 1.704
BuildRequires:	talloc-devel >= %{talloc_version}
BuildRequires:	tdb-devel >= %{tdb_version}
BuildRequires:	tevent-devel >= %{tevent_version}
%{?with_lmdb:Requires:	lmdb-libs >= 0.9.16}
Requires:	talloc >= %{talloc_version}
Requires:	tdb >= %{tdb_version}
Requires:	tevent >= %{tevent_version}
Requires:	popt >= 1.6
Provides:	libldb = %{version}-%{release}
Obsoletes:	libldb < 1.1.0-3
# ldb 1.6+ dropped python2 support
Obsoletes:	python-ldb < 1.6
Obsoletes:	python-ldb-devel < 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package -n python3-ldb
Summary:	Python 3 bindings for the LDB library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki LDB
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-tdb >= %{tdb_version}
Obsoletes:	pyldb < 1.1.0-1

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
	--disable-rpath-install

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n python3-ldb -p /sbin/ldconfig
%postun	-n python3-ldb -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libldb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libldb.so.2
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

%files -n python3-ldb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyldb-util.cpython-3*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpyldb-util.cpython-3*.so.2
%attr(755,root,root) %{py3_sitedir}/ldb.cpython-*.so
%{py3_sitedir}/_ldb_text.py
%{py3_sitedir}/__pycache__/_ldb_text.cpython-*.py[co]

%files -n python3-ldb-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyldb-util.cpython-3*.so
%{_includedir}/pyldb.h
%{_pkgconfigdir}/pyldb-util.cpython-3*.pc
