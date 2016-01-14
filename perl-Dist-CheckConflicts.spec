%{?scl:%scl_package perl-Dist-CheckConflicts}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}perl-Dist-CheckConflicts
Version:	0.09
Release:	6.sc1%{?dist}
Summary:	Declare version conflicts for your dist
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Dist-CheckConflicts/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Dist-CheckConflicts-%{version}.tar.gz
Patch0:		Dist-CheckConflicts-0.08-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Module Build
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	%{?scl_prefix}perl(base)
BuildRequires:	%{?scl_prefix}perl(Carp)
BuildRequires:	%{?scl_prefix}perl(Exporter)
BuildRequires:	%{?scl_prefix}perl(List::MoreUtils) >= 0.12
BuildRequires:	%{?scl_prefix}perl(Module::Runtime)
BuildRequires:	%{?scl_prefix}perl(strict)
BuildRequires:	%{?scl_prefix}perl(warnings)
# Test Suite
BuildRequires:	%{?scl_prefix}perl(File::Find)
BuildRequires:	%{?scl_prefix}perl(File::Temp)
BuildRequires:	%{?scl_prefix}perl(lib)
BuildRequires:	%{?scl_prefix}perl(Test::Fatal)
BuildRequires:	%{?scl_prefix}perl(Test::More) >= 0.47
# Extra Tests
%if ! 0%{?scl:1}
BuildRequires:	%{?scl_prefix}perl(Pod::Coverage::TrustPod)
BuildRequires:	%{?scl_prefix}perl(Test::EOL)
BuildRequires:	%{?scl_prefix}perl(Test::NoTabs)
BuildRequires:	%{?scl_prefix}perl(Test::Pod)
BuildRequires:	%{?scl_prefix}perl(Test::Pod::Coverage)
%endif
# Runtime
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})

# We need to patch the test suite if we have an old version of Test::More
%{?scl:%global old_test_more %(scl enable %{scl} "perl -MTest::More -e 'print ((\\$Test::More::VERSION < 0.88) ? 1 : 0)'" 2>/dev/null || echo 0)}
%{!?scl:%global old_test_more %(perl -MTest::More -e 'print ($Test::More::VERSION < 0.88 ? 1 : 0);' 2>/dev/null || echo 0)}

%description
One shortcoming of the CPAN clients that currently exist is that they have no
way of specifying conflicting downstream dependencies of modules. This module
attempts to work around this issue by allowing you to specify conflicting
versions of modules separately, and deal with them after the module is done
installing.

For instance, say you have a module Foo, and some other module Bar uses Foo. If
Foo were to change its API in a non-backwards-compatible way, this would cause
Bar to break until it is updated to use the new API. Foo can't just depend on
the fixed version of Bar, because this will cause a circular dependency
(because Bar is already depending on Foo), and this doesn't express intent
properly anyway - Foo doesn't use Bar at all. The ideal solution would be for
there to be a way to specify conflicting versions of modules in a way that would
let CPAN clients update conflicting modules automatically after an existing
module is upgraded, but until that happens, this module will allow users to do
this manually.

%prep
%setup -q -n Dist-CheckConflicts-%{version}

# Test suite needs patching if we have Test::More < 0.88
%if 00%{old_test_more}
%patch0
%endif

%build
%{?scl:scl enable %{scl} "}
perl Makefile.PL INSTALLDIRS=vendor
%{?scl:"}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} "}
make pure_install DESTDIR=%{buildroot}
%{?scl:"}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}
%if ! 0%{?scl:1}
%{?scl:scl enable %{scl} - << \EOF}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%{?scl:EOF}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/Dist/
%{_mandir}/man3/Dist::CheckConflicts.3pm*

%changelog
* Tue Feb 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-6
- Fixed getting of %%old_test_more
- Resolves: rhbz#1063206

* Mon Feb 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-5
- Get correct value for %%old_test_more on SCL
- Resolves: rhbz#1063206

* Sun Nov 24 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-4
- Rebuilt for SCL

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 0.09-2
- Perl 5.18 rebuild

* Mon Jul 22 2013 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Support Perl 5.6.x

* Wed Jul 10 2013 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Instead of silently ignoring conflicts that do not compile, issue a
    conflict warning (CPAN RT#75486)
- BR: perl(Module::Runtime)
- Classify buildreqs by usage
- Explicitly run the extra tests

* Sat Jun 22 2013 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06
  - Add optional runtime conflict warnings
  - Require 5.8.1, clean up a few things and add a few more tests
  - Use Exporter instead of Sub::Exporter
- Update patch for building with Test::More < 0.88
- Drop patch for building with old ExtUtils::MakeMaker, no longer needed
- Don't need to remove empty directories from the buildroot

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.02-6
- Perl 5.16 rebuild

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.02-5
- Pod::Coverage::TrustPod now available in all supported releases
- BR: perl(Carp)

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.02-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Paul Howarth <paul@city-fan.org> - 0.02-2
- Sanitize for Fedora submission

* Tue Jan  4 2011 Paul Howarth <paul@city-fan.org> - 0.02-1
- Initial RPM version
