%define enable_gir 0
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%define enable_gir 1
%endif

%define enable_gtkdoc 0
%if 0%{?fedora} >= 13 || 0%{?rhel} >= 7
%define enable_gtkdoc 1
%endif

Name:          rest
Version:       0.7.92
Release:       2%{?dist}
Summary:       A library for access to RESTful web services

Group:         System Environment/Libraries
License:       LGPLv2
URL:           http://www.gnome.org
Source0:       http://download.gnome.org/sources/%{name}/0.7/%{name}-%{version}.tar.xz
Patch0:        rest-fixdso.patch
Patch1:        0001-oauth-Add-missing-include.patch

BuildRequires: glib2-devel
%if %{?enable_gir}
BuildRequires: gobject-introspection-devel
%endif
BuildRequires: libsoup-devel
BuildRequires: libxml2-devel
%if %{?enable_gtkdoc}
BuildRequires: gtk-doc
%endif
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

%description
This library was designed to make it easier to access web services that
claim to be "RESTful". A RESTful service should have urls that represent 
remote objects, which methods can then be called on. The majority of services 
don't actually adhere to this strict definition. Instead, their RESTful end 
point usually has an API that is just simpler to use compared to other types 
of APIs they may support (XML-RPC, for instance). It is this kind of API that 
this library is attempting to support.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with %{name}.

%prep
%setup -q
%patch0 -p1 -b .fixdso
%patch1 -p1 -b .missinginclude

%build
autoreconf -vif
%if %{?enable_gir}
%define gir_arg --enable-introspection
%else
%define gir_arg --disable-introspection
%endif

%if %{?enable_gtkdoc}
%define gtkdoc_arg --enable-gtk-doc
%else
%define gtkdoc_arg --disable-gtk-doc
%endif

%configure --disable-static %{gtkdoc_arg} %{gir_arg}

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/librest-0.7.so.0
%{_libdir}/librest-0.7.so.0.0.0
%{_libdir}/librest-extras-0.7.so.0
%{_libdir}/librest-extras-0.7.so.0.0.0
%if %{?enable_gir}
%{_libdir}/girepository-1.0/Rest-0.7.typelib
%{_libdir}/girepository-1.0/RestExtras-0.7.typelib
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/rest-0.7
%{_libdir}/pkgconfig/rest*
%{_libdir}/librest-0.7.so
%{_libdir}/librest-extras-0.7.so
#even when gtk-doc is disabled, these files get built
#if %{?enable_gtkdoc}
%{_datadir}/gtk-doc/html/%{name}*0.7
#endif
%if %{?enable_gir}
%{_datadir}/gir-1.0/Rest-0.7.gir
%{_datadir}/gir-1.0/RestExtras-0.7.gir
%endif

%changelog
* Tue Jan 20 2015 Christophe Fergeau <cfergeau@redhat.com> 0.7.92-2
- Add patch fixing memory corruption with oauth
- Fix build on RHEL6
Resolves: #981677

* Mon Sep  8 2014 Debarshi Ray <rishi@fedoraproject.org> - 0.7.92-1
- Update to 0.7.92
Resolves: #1136793

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.7.90-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.7.90-6
- Mass rebuild 2013-12-27

* Wed Oct 16 2013 Debarshi Ray <rishi@fedoraproject.org> 0.7.90-5
- Attempt another rebuild to fix multilib issue with gtk-doc (Red Hat #881246)

* Tue Jul 16 2013 Matthias Clasen <mclasen@redhat.com> 0.7.90-4
- Rebuild with newer gtk-doc to fix multilib issue

* Sat Apr 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.90-3
- Run autoreconf for aarch64 (RHBZ 926440)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.7.90-1
- Release 0.7.90

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.12-1
- Release 0.7.12. Fixes CVE-2011-4129 RHBZ 752022

* Fri Oct 28 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.11-1
- Release 0.7.11

* Sun Apr 24 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.10-1
- Update to 0.7.10

* Sun Apr  3 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.9-1
- Update to 0.7.9

* Wed Mar 23 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.8-1
- Update to 0.7.8

* Tue Feb 22 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.6-1
- Update to 0.7.6

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.5-1
- Update to 0.7.5
- Now its on gnome we have official tar file releases

* Wed Sep 29 2010 jkeating - 0.7.3-2
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.3-1
- Update to 0.7.3

* Mon Aug 30 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.2-1
- Update to 0.7.2

* Thu Aug  5 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.0-1
- Update to 0.7.0

* Sun Jul 11 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.4-1
- Update to 0.6.4

* Wed May 12 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.3-2
- some cleanups and fixes

* Wed May 12 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.3-1
- Update to 0.6.3, update url and source details, enable introspection

* Mon Feb 15 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-4
- Add patch to fix DSO linking. Fixes bug 564764

* Mon Jan 25 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-3
- Bump build

* Mon Jan 25 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-2
- Move to official tarball release of 0.6.1

* Sat Oct 10 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-1
- New upstream 0.6.1 release

* Wed Aug 19 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-1
- New upstream 0.6 release

* Fri Aug  7 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.5-3
- A few minor spec file cleanups

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.5-1
- Update to 0.5

* Mon Jun 22 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.4-1
- Update to 0.4

* Wed Jun 17 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.3-1
- Initial packaging
