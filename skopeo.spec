%global with_check 0

%global import_path github.com/containers/%{name}
#%%global branch release-1.14
%global commit0 e2ea426918973e5e007a5e1e2457a41ab336fc41
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Epoch: 2
Name: skopeo
Version: 1.15.1
Release: 2%{?dist}
Summary: Inspect container images and repositories on registries
License: ASL 2.0
URL: https://%{import_path}
# https://fedoraproject.org/wiki/PackagingDrafts/Go#Go_Language_Architectures
ExclusiveArch: %{go_arches}
%if 0%{?branch:1}
Source0: https://%{import_path}/tarball/%{commit0}/%{branch}-%{shortcommit0}.tar.gz
%else
Source0: https://%{import_path}/archive/%{commit0}/%{name}-%{version}-%{shortcommit0}.tar.gz
%endif
BuildRequires: git-core
BuildRequires: golang >= 1.20.10
BuildRequires: /usr/bin/go-md2man
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: pkgconfig(devmapper)
BuildRequires: glib2-devel
BuildRequires: go-rpm-macros
BuildRequires: make
Requires: containers-common >= 2:1-2
Requires: system-release

%description
Command line utility to inspect images and repositories directly on Docker
registries without the need to pull them

%package tests
Summary: Tests for %{name}
Requires: %{name} = %{epoch}:%{version}-%{release}
#Requires: bats  (which RHEL8 doesn't have. If it ever does, un-comment this)
Requires: gnupg
Requires: jq
Requires: golang >= 1.20.10
Requires: podman
Requires: crun
Requires: httpd-tools
Requires: openssl
Requires: squashfs-tools

%description tests
%{summary}

This package contains system tests for %{name}

%prep
%if 0%{?branch:1}
%autosetup -Sgit -n containers-%{name}-%{shortcommit0}
%else
%autosetup -Sgit -n %{name}-%{commit0}
%endif
sed -i 's/install-binary: bin\/%{name}/install-binary:/' Makefile
sed -i 's/completions: bin\/%{name}/completions:/' Makefile
sed -i 's/install-docs: docs/install-docs:/' Makefile

%build
mkdir -p src/github.com/containers
ln -s ../../../ src/%{import_path}

mkdir -p vendor/src
for v in vendor/*; do
    if test ${v} = vendor/src; then continue; fi
    if test -d ${v}; then
      mv ${v} vendor/src/
    fi
done

export GOPATH=$(pwd):$(pwd)/vendor
export GO111MODULE=off
export CGO_CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export BUILDTAGS="exclude_graphdriver_btrfs btrfs_noversion $(hack/libdm_tag.sh)"
mkdir -p bin
%gobuild -o bin/%{name} ./cmd/%{name}
%{__make} docs

%install
make install-binary install-docs install-completions DESTDIR=%{buildroot} PREFIX=%{_prefix}

# system tests
install -d -p %{buildroot}/%{_datadir}/%{name}/test/system
cp -pav systemtest/* %{buildroot}/%{_datadir}/%{name}/test/system/

%check
%if 0%{?with_check}
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}

%gotest %{import_path}/integration
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}

%files tests
%license LICENSE
%{_datadir}/%{name}/test

%changelog
* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 2:1.15.1-2
- Bump release for June 2024 mass rebuild

* Thu May 16 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.15.1-1
- update to https://github.com/containers/skopeo/releases/tag/v1.15.1
- Related: RHEL-34195

* Thu Mar 28 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.15.0-3
- BR: go-rpm-macros
- Related: RHEL-30637

* Thu Mar 28 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.15.0-2
- remove Fedora hack
- Related: RHEL-30637

* Thu Mar 28 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.15.0-2.14.2
- Sync with RHEL9
- Resolves: RHEL-30637
