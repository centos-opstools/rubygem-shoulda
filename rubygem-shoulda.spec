%global gem_name shoulda
%global railsver %(gem list rails | grep rails | cut -d\\( -f2 | cut -d\\) -f1 | head -1 )
# Tests are currently commented out, make this cleaner.
%global with_tests 0

Summary: Making tests easy on the fingers and eyes
Name: rubygem-%{gem_name}
Version: 2.11.3
Release: 8%{?dist}
Group: Development/Languages
License: MIT
URL: http://thoughtbot.com/community/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# The following files are needed for testing, but are not part of the
# distribution. Here's how you obtain these files:
# 
# git clone git://github.com/thoughtbot/shoulda.git
# cd shoulda
# git checkout v2.11.3 # the version 
# cp tasks/shoulda.rake /path/to/SOURCES/rubygem-shoulda-tasks_shoulda.rake
# cp init.rb /path/to/SOURCES/rubygem-shoulda-init.rb
Source1:        rubygem-shoulda-tasks_shoulda.rake
Source2:        rubygem-shoulda-init.rb

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: dos2unix
%if 0%{?with_tests}
BuildRequires: rubygem(cucumber)
BuildRequires: rubygem(rake)
BuildRequires: rubygem(rails)
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(mocha)
%endif
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Making tests easy on the fingers and eyes

%package doc
Summary:           Documentation for %{name}
Group:             Documentation
Requires:          %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.



%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Notified upstream of lack of ability to run tests after running gem install 
#  on Sep 03, 2010.  Not holding my breath.

# This task is not part of the distribution but is required for rake test in %%check
mkdir -p %{buildroot}%{gem_instdir}/tasks
cp -a -p %{SOURCE1} %{buildroot}%{gem_instdir}/tasks/%{gem_name}.rake
# This is also not part of dist gem, but needed for tests
cp -a -p %{SOURCE2} %{buildroot}%{gem_instdir}/init.rb
# This is also not part of dist gem, but needed for tests
cp -a -p %{buildroot}/%{gem_dir}/specifications/* %{buildroot}%{gem_instdir}/shoulda.gemspec

# environment.rb set to use a static Rails version -- it's not pretty, but it works
echo 'RAILS_GEM_VERSION="%{railsver}" '  >  %{buildroot}%{gem_instdir}/test/rails2_root/config/environment.tmp.rb
cat %{buildroot}%{gem_instdir}/test/rails2_root/config/environment.rb >> %{buildroot}%{gem_instdir}/test/rails2_root/config/environment.tmp.rb
mv -f  %{buildroot}%{gem_instdir}/test/rails2_root/config/environment.tmp.rb %{buildroot}%{gem_instdir}/test/rails2_root/config/environment.rb

# Fix end-of-line encoding
dos2unix %{buildroot}/%{gem_instdir}/MIT-LICENSE



%clean
rm -rf %{buildroot}

%check 
%if 0%{?with_tests}
pushd %{buildroot}%{gem_instdir}
# TODO: run when new version comes out
# (tests of this version only work with rails 2.x.x)
#rake test
popd
%endif

%files
%defattr(-, root, root, -)
%{_bindir}/convert_to_should_syntax
%dir %{gem_instdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/MIT-LICENSE
%{gem_cache}
%{gem_spec}
%{gem_libdir}
%{gem_instdir}/bin
%{gem_instdir}/rails

%files doc
%defattr(-, root, root, -)
%{gem_instdir}/tasks
%{gem_instdir}/init.rb
%{gem_instdir}/*.gemspec
%{gem_docdir}
%{gem_instdir}/CONTRIBUTION_GUIDELINES.rdoc
%{gem_instdir}/test
%{gem_instdir}/Rakefile



%changelog
* Mon Nov 10 2014 Troy Dawson <tdawson@redhat.com> - 2.11.3-8
- Bump release for rebuild on epel7

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 2.11.3-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 2.11.3-4
- Rebuilt for Ruby 1.9.3.

* Sun Jan 08 2012 <stahnma@fedoraproject.org> - 2.11.3-2
- Jumped in to help with FTBFS bz#715949

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 01 2010 Michael Stahnke <stahnma@fedoraproject.org> - 2.11.3-1
- New version
- Fix many broken tests 
- Split into -doc package

* Sat Jan  9 2010 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.10.2-2
- Fix BuildRequires
- First package
