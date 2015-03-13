Name: libpcap
Epoch: 14
Version: 1.7.2
Release: 1%{?dist}
Summary: A system-independent interface for user-level packet capture
Group: Development/Libraries
License: BSD with advertising
URL: http://www.tcpdump.org
BuildRequires: glibc-kernheaders >= 2.2.0 bison flex

Source:  http://www.tcpdump.org/release/%{name}-%{version}.tar.gz

Patch0001:      0001-man-tcpdump-and-tcpslice-have-manpages-in-man8.patch
Patch0002:      0002-pcap-config-mitigate-multilib-conflict.patch
Patch0003:      0003-pcap-linux-apparently-ctc-interfaces-on-s390-has-eth.patch
Patch0004:      0004-pcap-linux-don-t-use-TPACKETV3-for-memory-mmapped-ca.patch

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
%autopatch -p1

#sparc needs -fPIC
%ifarch %{sparc}
sed -i -e 's|-fpic|-fPIC|g' configure
%endif

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/libpcap.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc LICENSE README CHANGES CREDITS
%{_libdir}/libpcap.so.*
%{_mandir}/man7/pcap*.7*

%files devel
%defattr(-,root,root)
%{_bindir}/pcap-config
%{_includedir}/pcap*.h
%{_includedir}/pcap
%{_libdir}/libpcap.so
%{_mandir}/man1/pcap-config.1*
%{_mandir}/man3/pcap*.3*
%{_mandir}/man5/pcap*.5*

%changelog
* Fri Mar 13 2015 Michal Sekletar <msekleta@redhat.com> - 14:1.7.2-1
- update to 1.7.2 (#1201078)

* Mon Feb 23 2015 Michal Sekletar <msekleta@redhat.com> - 14:1.6.2-2
- fix scaling of pcap-ng timestamps (#1169322)
- remove kernel-devel from buildrequires

* Mon Sep 29 2014 Michal Sekletar <msekleta@redhat.com> - 14:1.6.2-1
- update to 1.6.2 (#1124174)
- disable TPACKET_V3 support (#1131500)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Michal Sekletar <msekleta@redhat.com> - 14:1.5.3-3
- don't link against libnl

* Fri Mar 28 2014 Michal Sekletar <msekleta@redhat.com> - 14:1.5.3-2
- link against libnl (#765716)

* Wed Jan 15 2014 Michal Sekletar <msekleta@redhat.com> - 14:1.5.3-1
- update to 1.5.3

* Thu Nov 28 2013 Michal Sekletar <msekleta@redhat.com> - 14:1.5.1-1
- update to 1.5.1

* Fri Nov 08 2013 Michal Sekletar <msekleta@redhat.com> - 14:1.5.0-1.20131108git459712e
- update to snapshot 20131108git459712e

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 Michal Sekletar <msekleta@redhat.com> - 14:1.4.0-1
- update to 1.4.0

* Tue Mar 26 2013 Michal Sekletar <msekleta@redhat.com> - 14:1.3.0-4
- remove unused variable from pcap-config to prevent multilib conflicts
- specfile cleanup

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Michal Sekletar <msekleta@redhat.com> 14:1.3.0-1
- Update to 1.3.0

* Thu Jan 05 2012 Jan Synáček <jsynacek@redhat.com> 14:1.2.1-2
- Rebuilt for GCC 4.7

* Tue Jan 03 2012 Jan Synáček <jsynacek@redhat.com> 14:1.2.1-1
- Update to 1.2.1
- Drop unnecessary -fragment patch

* Fri Dec 02 2011 Michal Sekletar <msekleta@redhat.com> 14:1.2.0-1
- update to 1.2.0

* Tue Sep 06 2011 Michal Sekletar <msekleta@redhat.com> 14:1.1.1-4
- fix capture of fragmented ipv6 packets

* Fri Apr 22 2011 Miroslav Lichvar <mlichvar@redhat.com> 14:1.1.1-3
- ignore /sys/net/dev files on ENODEV (#693943)
- drop ppp patch
- compile with -fno-strict-aliasing

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 06 2010 Miroslav Lichvar <mlichvar@redhat.com> 14:1.1.1-1
- update to 1.1.1

* Wed Dec 16 2009 Miroslav Lichvar <mlichvar@redhat.com> 14:1.0.0-5.20091201git117cb5
- update to snapshot 20091201git117cb5

* Sat Oct 17 2009 Dennis Gilmore <dennis@ausil.us> 14:1.0.0-4.20090922gite154e2
- use -fPIC on sparc arches

* Wed Sep 23 2009 Miroslav Lichvar <mlichvar@redhat.com> 14:1.0.0-3.20090922gite154e2
- update to snapshot 20090922gite154e2
- drop old soname

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.0.0-2.20090716git6de2de
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Miroslav Lichvar <mlichvar@redhat.com> 14:1.0.0-1.20090716git6de2de
- update to 1.0.0, git snapshot 20090716git6de2de

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:0.9.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 27 2008 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.8-3
- use CFLAGS when linking (#445682)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 14:0.9.8-2
- Autorebuild for GCC 4.3

* Wed Oct 24 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.8-1
- update to 0.9.8

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
