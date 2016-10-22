%{?scl:%scl_package perl-Dist-CheckConflicts}

# We need to patch the test suite if we have an old version of Test::More
%global old_test_more %(%{?scl:scl enable %{scl} '}perl -MTest::More -e %{?scl:'"}'%{?scl:"'}print (($Test::More::VERSION < 0.88) ? 1 : 0);%{?scl:'"}'%{?scl:"'} 2>/dev/null || echo 0%{?scl:'})

Name:		%{?scl_prefix}perl-Dist-CheckConflicts
Version:	0.11
Release:	8%{?dist}
Summary:	Declare version conflicts for your dist
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Dist-CheckConflicts/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Dist-CheckConflicts-%{version}.tar.gz
Patch0:		Dist-CheckConflicts-0.11-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Module Build
BuildRequires:	%{?scl_prefix}perl-generators
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	%{?scl_prefix}perl(base)
BuildRequires:	%{?scl_prefix}perl(Carp)
BuildRequires:	%{?scl_prefix}perl(Exporter)
BuildRequires:	%{?scl_prefix}perl(Module::Runtime) >= 0.009
BuildRequires:	%{?scl_prefix}perl(strict)
BuildRequires:	%{?scl_prefix}perl(warnings)
# Test Suite
BuildRequires:	%{?scl_prefix}perl(File::Spec)
BuildRequires:	%{?scl_prefix}perl(IO::Handle)
BuildRequires:	%{?scl_prefix}perl(IPC::Open3)
BuildRequires:	%{?scl_prefix}perl(lib)
BuildRequires:	%{?scl_prefix}perl(Test::Fatal)
BuildRequires:	%{?scl_prefix}perl(Test::More) >= 0.47
# Extra Tests
%if !%{defined perl_small}
BuildRequires:	%{?scl_prefix}perl(Pod::Coverage::TrustPod)
BuildRequires:	%{?scl_prefix}perl(Test::EOL)
BuildRequires:	%{?scl_prefix}perl(Test::NoTabs)
BuildRequires:	%{?scl_prefix}perl(Test::Pod) >= 1.41
BuildRequires:	%{?scl_prefix}perl(Test::Pod::Coverage) >= 1.08
%endif
# Runtime
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))

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
%if %{old_test_more}
%patch0
%endif

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}
%if !%{defined perl_small}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Dist/
%{_mandir}/man3/Dist::CheckConflicts.3pm*

%changelog
* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 0.11-8
- SCL

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-4
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr  3 2014 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11
  - Drop the dep on List::MoreUtils
    (https://github.com/doy/dist-checkconflicts/pull/8)
- Update patch for building with Test::More < 0.88
- Don't try to run the extra tests for EPEL builds
- Specify version requirements for extra test modules

* Wed Dec 18 2013 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10
  - We need Module::Runtime 0.009 for module_notional_filename (#6)
- Update patch for building with Test::More < 0.88
- Drop %%defattr, redundant since rpm 4.4

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
