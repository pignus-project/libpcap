%define pcap_sover 0.9

Name: libpcap
Epoch: 14
Version: 0.9.7
Release: 3%{?dist}
Summary: A system-independent interface for user-level packet capture
Group: Development/Libraries
License: BSD with advertising
URL: http://www.tcpdump.org
BuildRequires: glibc-kernheaders >= 2.2.0 bison flex
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
Patch1: libpcap-man.patch
Patch2: libpcap-0.9.7-shared.patch
Patch3: libpcap-s390.patch
Patch4: libpcap-0.8.3-ppp.patch

%description
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

Install libpcap if you need to do low-level network traffic monitoring
on your network.

%package devel
Summary: Libraries and header files for the libpcap library
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

This package provides the libraries, include files, and other 
resources needed for developing libpcap applications.
 
%prep
%setup -q

%patch1 -p1 -b .man 
%patch2 -p1 -b .shared 
%patch3 -p1 -b .s390
%patch4 -p0 -b .ppp

%build
export CFLAGS="$RPM_OPT_FLAGS $(getconf LFS_CFLAGS)"
%configure --enable-ipv6
make SOVERSION=%{pcap_sover}

%install
rm -rf $RPM_BUILD_ROOT

make SOVERSION=%{pcap_sover} DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/libpcap.a

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc LICENSE README CHANGES CREDITS doc/pcap.txt
%{_libdir}/libpcap.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/pcap*.h
%{_libdir}/libpcap.so
%{_mandir}/man3/pcap.3*

%changelog
* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.7-3
- update license tag

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 14:0.9.7-2
- Rebuild for RH #249435

* Tue Jul 24 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.7-1
- update to 0.9.7

* Tue Jun 19 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.6-1
- update to 0.9.6

* Tue Nov 28 2006 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.5-1
- split from tcpdump package (#193657)
- update to 0.9.5
- don't package static library
- maintain soname
