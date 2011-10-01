%define		talloc_version	2.0.5
%define		tdb_version		1.2.9
%define		tevent_version	0.9.12
Summary:	A schema-less, ldap like, API and database
Name:		libldb
Version:	1.1.0
Release:	1
License:	LGPL v3+
Group:		Development/Libraries
URL:		http://ldb.samba.org/
Source0:	http://samba.org/ftp/ldb/ldb-%{version}.tar.gz
# Source0-md5:	61145ad9cfe017ce4fca5cbc77b9552b
BuildRequires:	autoconf
BuildRequires:	docbook-style-xsl
BuildRequires:	libtalloc-devel >= %{talloc_version}
BuildRequires:	libxslt
BuildRequires:	popt-devel
BuildRequires:	python-devel
BuildRequires:	python-talloc-devel
BuildRequires:	python-tdb
BuildRequires:	tdb-devel >= %{tdb_version}
BuildRequires:	tevent-devel >= %{tevent_version}
Requires:	libtalloc >= %{talloc_version}
Requires:	tdb >= %{tdb_version}
Requires:	tevent >= %{tevent_version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An extensible library that implements an LDAP like API to access
remote LDAP servers, or use local tdb databases.

%package -n ldb-tools
Summary:	Tools to manage LDB files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n ldb-tools
Tools to manage LDB files.

%package devel
Summary:	Developer tools for the LDB library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libtalloc-devel >= %{talloc_version}
Requires:	pkgconfig
Requires:	tdb-devel >= %{tdb_version}
Requires:	tevent-devel >= %{tevent_version}

%description devel
Header files needed to develop programs that link against the LDB
library.

%package -n python-ldb
Summary:	Python bindings for the LDB library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-tdb = %{tdb_version}
Obsoletes:	pyldb

%description -n python-ldb
Python bindings for the LDB library.

%package -n python-ldb-devel
Summary:	Development files for the Python bindings for the LDB library
Group:		Development/Libraries
Requires:	pyldb = %{version}-%{release}

%description -n python-ldb-devel
Development files for the Python bindings for the LDB library

%prep
%setup -q -n ldb-%{version}

%build
# note: configure in fact is waf call
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
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

# Remove _tevent.so (it's managed by python-tevent)
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_tevent.so

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n python-ldb -p /sbin/ldconfig
%postun	-n python-ldb -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%dir %{_libdir}/ldb
%{_libdir}/libldb.so.*
%dir %{_libdir}/ldb/modules
%dir %{_libdir}/ldb/modules/ldb
%{_libdir}/ldb/modules/ldb/*.so

%files -n ldb-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ldbadd
%attr(755,root,root) %{_bindir}/ldbdel
%attr(755,root,root) %{_bindir}/ldbedit
%attr(755,root,root) %{_bindir}/ldbmodify
%attr(755,root,root) %{_bindir}/ldbrename
%attr(755,root,root) %{_bindir}/ldbsearch
%{_libdir}/ldb/libldb-cmdline.so
%{_mandir}/man1/ldbadd.1.*
%{_mandir}/man1/ldbdel.1.*
%{_mandir}/man1/ldbedit.1.*
%{_mandir}/man1/ldbmodify.1.*
%{_mandir}/man1/ldbrename.1.*
%{_mandir}/man1/ldbsearch.1.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/ldb_module.h
%{_includedir}/ldb_handlers.h
%{_includedir}/ldb_errors.h
%{_includedir}/ldb_version.h
%{_includedir}/ldb.h
%{_libdir}/libldb.so

%{_pkgconfigdir}/ldb.pc
%{_mandir}/man3/ldb.3*

%files -n python-ldb
%defattr(644,root,root,755)
%{py_sitedir}/ldb.so
%{_libdir}/libpyldb-util.so.1*

%files -n python-ldb-devel
%defattr(644,root,root,755)
%{_includedir}/pyldb.h
%{_libdir}/libpyldb-util.so
%{_pkgconfigdir}/pyldb-util.pc
