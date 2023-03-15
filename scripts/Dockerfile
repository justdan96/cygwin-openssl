# syntax=docker/dockerfile:1
ARG FEDORA_IMAGE=fedora:38
FROM $FEDORA_IMAGE AS builder
MAINTAINER Dan Bryant (daniel.bryant@linux.com)

ENV TZ=Europe/London

# install basic dependencies for Linux build
RUN dnf update -y
RUN dnf install -y nano

# install Linux tools required to build Windows packages
RUN dnf install -y cmake gcc make ninja-build zip
RUN dnf upgrade -y

# enable cygwin COPR
RUN dnf install -y dnf-plugins-core
RUN dnf copr enable -y yselkowitz/cygwin
RUN dnf update -y
RUN dnf install -y cygwin-binutils cygwin-filesystem-base cygwin64-gcc cygwin-gcc-common cygwin64-w32api-headers \
	cygwin64-w32api-runtime cygwin64-zlib cygwin64-zlib-static cygwin64-pkg-config cygwin64-gcc-c++
RUN dnf install -y findutils xz
RUN dnf install -y cygwin64-libiconv-static 
RUN dnf download -y --source cygwin-libiconv
RUN rpm -ivh cygwin-libiconv*.src.rpm
RUN rm -f cygwin-libiconv*.src.rpm
RUN dnf install -y perl
RUN dnf install -y byacc flex
RUN dnf install -y git file zip patch rpmdevtools rpmlint wget
RUN dnf install -y cygwin32 cygwin32-gcc cygwin32-zlib imake

# clone and compile cygwin-openssl - we use an updated version of yselkowitz's specfile
RUN mkdir -p /root/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
RUN rm -f /root/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}/*
RUN echo cache_111t
RUN cd /root/rpmbuild/SPECS && git clone https://github.com/justdan96/cygwin-openssl.git .
RUN cd /root/rpmbuild/SPECS && awk '/^Version:.*/ {print $2}' cygwin-openssl.spec > /root/rpmbuild/VERSION
RUN cd /root/rpmbuild/SPECS && sed -i "s/make depend/sed -i 's!-m64!!g' Makefile\nsed -i 's!^CPPFLAGS=.*!CPPFLAGS=!g' Makefile\nsed -i 's!^CFLAGS=.*!CFLAGS=!g' Makefile\nsed -i 's!^CXXFLAGS=.*!CXXFLAGS=!g' Makefile\nsed -i 's!^LDFLAGS=.*!LDFLAGS=!g' Makefile\nmake depend/g" cygwin-openssl.spec
RUN cd /root/rpmbuild/SOURCES && wget http://www.openssl.org/source/openssl-$(cat /root/rpmbuild/VERSION).tar.gz
RUN rpmbuild -bb /root/rpmbuild/SPECS/cygwin-openssl.spec

# remove the debuginfo RPMs - we don't need them
RUN rm -f /root/rpmbuild/RPMS/noarch/*-debuginfo-*.rpm

# copy all the created RPMs to the host
FROM scratch AS export
COPY --from=builder /root/rpmbuild/RPMS/noarch/*.rpm .
