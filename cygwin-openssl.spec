%{?cygwin_package_header}

%define soversion 1.0.0

Name:           cygwin-openssl
Version:        1.1.1m
Release:        1%{?dist}
Summary:        Cygwin port of the OpenSSL toolkit

Group:          Development/Libraries
License:        OpenSSL
URL:            http://www.openssl.org/
BuildArch:      noarch

Source0:        http://www.openssl.org/source/openssl-%{version}.tar.gz

BuildRequires:  cygwin32-filesystem
BuildRequires:  cygwin32-binutils
BuildRequires:  cygwin32-gcc
BuildRequires:  cygwin32
BuildRequires:  cygwin32-zlib

BuildRequires:  cygwin64-filesystem
BuildRequires:  cygwin64-binutils
BuildRequires:  cygwin64-gcc
BuildRequires:  cygwin64
BuildRequires:  cygwin64-zlib

BuildRequires:  perl
BuildRequires:  sed
BuildRequires:  /usr/bin/cmp
BuildRequires:  /usr/bin/mktemp
BuildRequires:  /usr/bin/rename
# The build script uses /usr/bin/makedepend which comes from imake.
# We also use lndir below to set up duplicate build trees
BuildRequires:  imake


%description
OpenSSL encryption toolkit for Cygwin toolchains.

%package -n cygwin32-openssl
Summary:        Cygwin32 OpenSSL libraries
Group:          Development/Libraries

%description -n cygwin32-openssl
OpenSSL encryption toolkit for the Cygwin i686 toolchain.

%package -n cygwin64-openssl
Summary:        Cygwin64 OpenSSL libraries
Group:          Development/Libraries

%description -n cygwin64-openssl
OpenSSL encryption toolkit for the Cygwin x86_64 toolchain.

%{?cygwin_debug_package}


%prep
%setup -q -n openssl-%{version}

if ! iconv -f UTF-8 -t ASCII//TRANSLIT CHANGES >/dev/null 2>&1 ; then
  iconv -f ISO-8859-1 -t UTF-8 -o CHANGES.utf8 CHANGES && \
    mv -f CHANGES.utf8 CHANGES
fi


%build
# openssl must be built in-tree
mkdir -p ../build_32bit ../build_64bit
lndir -silent `pwd` ../build_32bit
lndir -silent `pwd` ../build_64bit
mv ../build_32bit ../build_64bit .

pushd build_32bit
./Configure \
  --prefix=%{cygwin32_prefix} \
  --cross-compile-prefix=%{cygwin32_target}- \
  shared zlib enable-seed enable-rfc3779 enable-camellia \
  enable-cms enable-md2 enable-rc5 Cygwin

make depend
make all EXE_EXT=.exe
popd


mkdir -p build_64bit
pushd build_64bit
./Configure \
  --prefix=%{cygwin64_prefix} \
  --cross-compile-prefix=%{cygwin64_target}- \
  shared zlib enable-seed enable-rfc3779 enable-camellia \
  enable-cms enable-md2 enable-rc5 Cygwin-x86_64

make depend
make all EXE_EXT=.exe
popd


%install
pushd build_32bit
make DESTDIR=$RPM_BUILD_ROOT install_sw EXE_EXT=.exe
popd
pushd build_64bit
make DESTDIR=$RPM_BUILD_ROOT install_sw EXE_EXT=.exe
popd

# Remove unnecessary Cygwin native binaries and runtime files
rm -f $RPM_BUILD_ROOT%{cygwin32_bindir}/c_rehash
rm -f $RPM_BUILD_ROOT%{cygwin32_bindir}/*.exe
rm -rf $RPM_BUILD_ROOT%{cygwin32_libdir}/engines/
rm -rf $RPM_BUILD_ROOT%{cygwin32_prefix}/ssl

rm -f $RPM_BUILD_ROOT%{cygwin64_bindir}/c_rehash
rm -f $RPM_BUILD_ROOT%{cygwin64_bindir}/*.exe
rm -rf $RPM_BUILD_ROOT%{cygwin64_libdir}/engines/
rm -rf $RPM_BUILD_ROOT%{cygwin64_prefix}/ssl

# Documentation already provided by Fedora native package
rm -rf $RPM_BUILD_ROOT%{cygwin32_mandir}
rm -rf $RPM_BUILD_ROOT%{cygwin64_mandir}


%files -n cygwin32-openssl
%doc CHANGES LICENSE NEWS
%{cygwin32_bindir}/cygcrypto-%{soversion}.dll
%{cygwin32_bindir}/cygssl-%{soversion}.dll
%{cygwin32_includedir}/openssl
%{cygwin32_libdir}/libcrypto.dll.a
%{cygwin32_libdir}/libssl.dll.a
%{cygwin32_libdir}/pkgconfig/libcrypto.pc
%{cygwin32_libdir}/pkgconfig/libssl.pc
%{cygwin32_libdir}/pkgconfig/openssl.pc

%files -n cygwin64-openssl
%doc CHANGES LICENSE NEWS
%{cygwin64_bindir}/cygcrypto-%{soversion}.dll
%{cygwin64_bindir}/cygssl-%{soversion}.dll
%{cygwin64_includedir}/openssl
%{cygwin64_libdir}/libcrypto.dll.a
%{cygwin64_libdir}/libssl.dll.a
%{cygwin64_libdir}/pkgconfig/libcrypto.pc
%{cygwin64_libdir}/pkgconfig/libssl.pc
%{cygwin64_libdir}/pkgconfig/openssl.pc


%changelog
* Wed Dec 22 2021 Dan Bryant <daniel.bryant@linux.com> - 1.1.1m-1
- new version

* Tue Dec 05 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.2m-1
- new version

* Sun Sep 11 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.2h-1
- Version bump.

* Tue Apr 08 2014 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.0.1g-1
- Version bump.

* Thu Jan 23 2014 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.0.1f-1
- Version bump.

* Tue Jul 02 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.0.1e-2
- Rebuild for new Cygwin packaging scheme.
- Add cygwin64 package.

* Sun Feb 17 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.0.1e-1
- Version bump.

* Thu May 24 2012 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.0.1c-1
- Version bump.

* Tue Mar 20 2012 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.0.1-1
- Version bump.
- Remove unnecessary files.

* Sun Mar 20 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 0.9.8r-1
- Initial spec file, largely based on mingw32-openssl.
