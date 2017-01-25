# TODO
# - ld.bfd enforced because gold does not understand '!' in version script (binutils-3:2.21.53.0.1-1)
%define		talloc_version	2:2.1.8
%define		tdb_version	2:1.3.12
%define		tevent_version	0.9.31
Summary:	LDAP-like embedded database
Summary(pl.UTF-8):	Wbudowana baza danych podobna do LDAP
Name:		ldb
Version:	1.1.29
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	https://www.samba.org/ftp/ldb/%{name}-%{version}.tar.gz
# Source0-md5:	9c90abfb94c1e2a693399392cf4cddb9
URL:		https://ldb.samba.org/
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt
BuildRequires:	openldap-devel
BuildRequires:	popt-devel >= 1.6
BuildRequires:	python-devel >= 1:2.4.2
BuildRequires:	python-talloc-devel >= %{talloc_version}
BuildRequires:	python-tdb >= %{tdb_version}
BuildRequires:	python-tevent >= %{tevent_version}
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	talloc-devel >= %{talloc_version}
BuildRequires:	tdb-devel >= %{tdb_version}
BuildRequires:	tevent-devel >= %{tevent_version}
Requires:	talloc >= %{talloc_version}
Requires:	tdb >= %{tdb_version}
Requires:	tevent >= %{tevent_version}
Requires:	popt >= 1.6
Provides:	libldb = %{version}-%{release}
Obsoletes:	libldb < 1.1.0-3
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

%package -n python-ldb
Summary:	Python bindings for the LDB library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki LDB
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs >= 1:2.4.2
Requires:	python-tdb >= %{tdb_version}
Obsoletes:	pyldb

%description -n python-ldb
Python bindings for the LDB library.

%description -n python-ldb -l pl.UTF-8
Wiązania Pythona do biblioteki LDB.

%package -n python-ldb-devel
Summary:	Development files for the Python bindings for the LDB library
Summary(pl.UTF-8):	Pliki programistyczne wiązań Pythona do biblioteki LDB
Group:		Development/Libraries
Requires:	python-ldb = %{version}-%{release}

%description -n python-ldb-devel
Development files for the Python bindings for the LDB library.

%description -n python-ldb-devel -l pl.UTF-8
Pliki programistyczne wiązań Pythona do biblioteki LDB.

%prep
%setup -q

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags} -fuse-ld=bfd" \
PYTHONDIR=%{py_sitedir} \
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

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n python-ldb -p /sbin/ldconfig
%postun	-n python-ldb -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libldb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libldb.so.1
%dir %{_libdir}/ldb
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
