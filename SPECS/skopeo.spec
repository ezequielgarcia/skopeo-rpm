%global with_debug 1
%global with_check 0

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%if 0%{?rhel} > 7 && ! 0%{?fedora}
%define gobuild(o:) \
go build -buildmode pie -compiler gc -tags="rpm_crashtraceback no_openssl ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -compressdwarf=false -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags'" -a -v -x %{?**};
%endif # distro

%global provider github
%global provider_tld com
%global project containers
%global repo skopeo
# https://github.com/containers/skopeo
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path %{provider_prefix}
%global git0 https://%{import_path}
%global commit0 1715c9084124875cb71f006916396e3c7d03014e
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# manually listed arches due https://bugzilla.redhat.com/show_bug.cgi?id=1391932 (removed ppc64)
# remove ix86 temporarily because go-toolset issues
ExcludeArch: ppc64 %{ix86}

Name: %{repo}
Epoch: 1
Version: 0.1.32
Release: 4.git%{shortcommit0}%{?dist}
Summary: Inspect Docker images and repositories on registries
License: ASL 2.0
URL: %{git0}
Source0: %{git0}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Source1: storage.conf
Source2: containers-storage.conf.5.md
Source3: mounts.conf
Source4: registries.conf.5.md
Source5: registries.conf
Source6: policy.json.5.md
Source7: seccomp.json
BuildRequires: git
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires: golang-github-cpuguy83-go-md2man
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: pkgconfig(devmapper)
BuildRequires: ostree-devel
BuildRequires: glib2-devel
Requires: containers-common = %{epoch}:%{version}-%{release}

%description
Command line utility to inspect images and repositories directly on Docker
registries without the need to pull them

%package -n containers-common
Summary: Configuration files for working with image signatures
Obsoletes: atomic <= 1:1.13.1-2
Conflicts: atomic-registries <= 1:1.22.1-1
Obsoletes: docker-rhsubscription <= 2:1.13.1-31
Provides: %{name}-containers = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-containers <= 1:0.1.31-3
Recommends: fuse-overlayfs
Recommends: slirp4netns

%description -n containers-common
This package installs a default signature store configuration and a default
policy under `/etc/containers/`.

%prep
%autosetup -Sgit -n %{name}-%{commit0}

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

export GOPATH=$(pwd):$(pwd)/vendor:%{gopath}
#make BUILDTAGS='exclude_graphdriver_btrfs' binary-local docs
export BUILDTAGS="exclude_graphdriver_btrfs"
%gobuild -o %{name} ./cmd/%{name}
make docs

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_sysconfdir}
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/containers/storage.conf
mkdir -p %{buildroot}%{_mandir}/man5
go-md2man -in %{SOURCE2} -out %{buildroot}%{_mandir}/man5/containers-storage.conf.5
go-md2man -in %{SOURCE4} -out %{buildroot}%{_mandir}/man5/registries.conf.5
install -p -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/containers/
go-md2man -in %{SOURCE6} -out %{buildroot}%{_mandir}/man5/policy.json.5

mkdir -p %{buildroot}%{_datadir}/containers
install -m0644 %{SOURCE3} %{buildroot}%{_datadir}/containers/mounts.conf
install -m0644 %{SOURCE7} %{buildroot}%{_datadir}/containers/seccomp.json

# install secrets patch directory
install -d -p -m 750 %{buildroot}/%{_datadir}/rhel/secrets
# rhbz#1110876 - update symlinks for subscription management
ln -s %{_sysconfdir}/pki/entitlement %{buildroot}%{_datadir}/rhel/secrets/etc-pki-entitlement
ln -s %{_sysconfdir}/rhsm %{buildroot}%{_datadir}/rhel/secrets/rhsm
ln -s %{_sysconfdir}/yum.repos.d/redhat.repo %{buildroot}%{_datadir}/rhel/secrets/rhel7.repo

%check
%if 0%{?with_check}
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%gotest %{import_path}/integration
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files -n containers-common
%dir %{_sysconfdir}/containers
%dir %{_sysconfdir}/containers/registries.d
%config(noreplace) %{_sysconfdir}/containers/policy.json
%config(noreplace) %{_sysconfdir}/containers/registries.d/default.yaml
%config(noreplace) %{_sysconfdir}/containers/storage.conf 
%config(noreplace) %{_sysconfdir}/containers/registries.conf
%dir %{_sharedstatedir}/atomic/sigstore
%{_mandir}/man5/*
%dir %{_datadir}/containers
%{_datadir}/containers/mounts.conf
%{_datadir}/containers/seccomp.json
%dir %{_datadir}/rhel/secrets
%{_datadir}/rhel/secrets/etc-pki-entitlement
%{_datadir}/rhel/secrets/rhel7.repo
%{_datadir}/rhel/secrets/rhsm

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}

%changelog
* Thu Nov 28 2019 Jindrich Novy <jnovy@redhat.com> - 1:0.1.32-4.git1715c90
- rebuild because of CVE-2019-9512 and CVE-2019-9514
- Resolves: #1772130, #1772135

* Tue Dec 18 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:0.1.32-3.git1715c90
- rebase

* Mon Dec 17 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:0.1.32-2.git1715c90
- re-enable debuginfo

* Mon Dec 17 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:0.1.31-12.gitb0b750d
- go tools not in scl anymore

* Fri Sep 21 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.31-11.gitb0b750d
- Resolves: #1615609
- built upstream tag v0.1.31

* Thu Aug 23 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.31-10.git0144aa8
- Resolves: #1616069 - correct order of registries

* Mon Aug 13 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.31-9.git0144aa8
- Resolves: #1615609 - rebuild with gobuild tag 'no_openssl'

* Fri Aug 10 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.31-8.git0144aa8
- Resolves: #1614934 - containers-common soft dep on slirp4netns and
fuse-overlayfs

* Wed Aug 08 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.31-7.git0144aa8
- build with %%gobuild
- use scl-ized go-toolset as dep
- disable i686 builds temporarily because of go-toolset issues

* Wed Jul 18 2018 dwalsh <dwalsh@redhat.com> - 1:0.1.31-6.git0144aa8
- add statx to seccomp.json to containers-config
- add seccomp.json to containers-config

* Tue Jul 03 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.31-4.git0144aa8
- Resolves: #1597629 - handle dependency issue for skopeo-containers
- rename skopeo-containers to containers-common as in Fedora

* Mon Jun 25 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.31-3.git0144aa8
- Resolves: #1583762 - btrfs dep removal needs exclude_graphdriver_btrfs
buildtag

* Wed Jun 13 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.31-2.git0144aa8
- correct bz in previous changelog

* Wed Jun 13 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.31-1.git0144aa8
- Resolves: #1580938 - resolve FTBFS
- Resolves: #1583762 - remove dependency on btrfs-progs-devel
- bump to v0.1.31 (from master)
- built commit ca3bff6
- use go-toolset deps for rhel8

* Tue Apr 03 2018 baude <bbaude@redhat.com> - 0.1.29-5.git7add6fc
- Fix small typo in registries.conf

* Tue Apr 3 2018 dwalsh <dwalsh@redhat.com> - 0.1.29-4.git
- Add policy.json.5

* Mon Apr 2 2018 dwalsh <dwalsh@redhat.com> - 0.1.29-3.git
- Add registries.conf

* Mon Apr 2 2018 dwalsh <dwalsh@redhat.com> - 0.1.29-2.git
- Add registries.conf man page

* Thu Mar 29 2018 dwalsh <dwalsh@redhat.com> - 0.1.29-1.git
- bump to 0.1.29-1
- Updated containers/image
    docker-archive generates docker legacy compatible images
    Do not create $DiffID subdirectories for layers with no configs
    Ensure the layer IDs in legacy docker/tarfile metadata are unique
    docker-archive: repeated layers are symlinked in the tar file
    sysregistries: remove all trailing slashes
    Improve docker/* error messages
    Fix failure to make auth directory
    Create a new slice in Schema1.UpdateLayerInfos
    Drop unused storageImageDestination.{image,systemContext}
    Load a *storage.Image only once in storageImageSource
    Support gzip for docker-archive files
    Remove .tar extension from blob and config file names
    ostree, src: support copy of compressed layers
    ostree: re-pull layer if it misses uncompressed_digest|uncompressed_size
    image: fix docker schema v1 -> OCI conversion
    Add /etc/containers/certs.d as default certs directory

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.28-2.git0270e56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 2 2018 dwalsh <dwalsh@redhat.com> - 0.1.28-1.git
- Vendor in fixed libraries in containers/image and containers/storage

* Tue Nov 21 2017 dwalsh <dwalsh@redhat.com> - 0.1.27-1.git
- Fix Conflicts to Obsoletes
- Add better docs to man pages.
- Use credentials from authfile for skopeo commands
- Support storage="" in /etc/containers/storage.conf
- Add global --override-arch and --override-os options

* Wed Nov 15 2017 dwalsh <dwalsh@redhat.com> - 0.1.25-2.git2e8377a7
-  Add manifest type conversion to skopeo copy
-  User can select from 3 manifest types: oci, v2s1, or v2s2
-   e.g skopeo copy --format v2s1 --compress-blobs docker-archive:alp.tar dir:my-directory

* Wed Nov 8 2017 dwalsh <dwalsh@redhat.com> - 0.1.25-2.git7fd6f66b
- Force storage.conf to default to overlay

* Wed Nov 8 2017 dwalsh <dwalsh@redhat.com> - 0.1.25-1.git7fd6f66b
-   Fix CVE in tar-split
-   copy: add shared blob directory support for OCI sources/destinations
-   Aligning Docker version between containers/image and skopeo
-   Update image-tools, and remove the duplicate Sirupsen/logrus vendor
-   makefile: use -buildmode=pie
  
* Tue Nov 7 2017 dwalsh <dwalsh@redhat.com> - 0.1.24-8.git28d4e08a
- Add /usr/share/containers/mounts.conf

* Sun Oct 22 2017 dwalsh <dwalsh@redhat.com> - 0.1.24-7.git28d4e08a
- Bug fixes
- Update to release

* Tue Oct 17 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.24-6.dev.git28d4e08
- skopeo-containers conflicts with docker-rhsubscription <= 2:1.13.1-31

* Tue Oct 17 2017 dwalsh <dwalsh@redhat.com> - 0.1.24-5.dev.git28d4e08
- Add rhel subscription secrets data to skopeo-containers

* Thu Oct 12 2017 dwalsh <dwalsh@redhat.com> - 0.1.24-4.dev.git28d4e08
- Update container/storage.conf and containers-storage.conf man page
- Default override to true so it is consistent with RHEL.

* Tue Oct 10 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.24-3.dev.git28d4e08
- built commit 28d4e08

* Mon Sep 18 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.24-2.dev.git875dd2e
- built commit 875dd2e
- Resolves: gh#416

* Tue Sep 12 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.24-1.dev.gita41cd0
- bump to 0.1.24-dev
- correct a prior bogus date
- fix macro in comment warning

* Mon Aug 21 2017 dwalsh <dwalsh@redhat.com> - 0.1.23-6.dev.git1bbd87
- Change name of storage.conf.5 man page to containers-storage.conf.5, since
it conflicts with inn package
- Also remove default to "overalay" in the configuration, since we should
- allow containers storage to pick the best default for the platform.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.23-5.git1bbd87f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 0.1.23-4.git1bbd87f
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.23-3.git1bbd87f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 dwalsh <dwalsh@redhat.com> - 0.1.23-2.dev.git1bbd87
- Fix storage.conf man page to be storage.conf.5.gz so that it works.

* Fri Jul 21 2017 dwalsh <dwalsh@redhat.com> - 0.1.23-1.dev.git1bbd87
- Support for OCI V1.0 Images
- Update to image-spec v1.0.0 and revendor
- Fixes for authentication

* Sat Jul 01 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.22-2.dev.git5d24b67
- Epoch: 1 for CentOS as CentOS Extras' build already has epoch set to 1

* Wed Jun 21 2017 dwalsh <dwalsh@redhat.com> - 0.1.22-1.dev.git5d24b67
-  Give more useful help when explaining usage
-  Also specify container-storage as a valid transport
-  Remove docker reference wherever possible
-  vendor in ostree fixes

* Thu Jun 15 2017 dwalsh <dwalsh@redhat.com> - 0.1.21-1.dev.git0b73154
- Add support for storage.conf and storage-config.5.md from github container storage package
- Bump to the latest version of skopeo
- vendor.conf: add ostree-go
- it is used by containers/image for pulling images to the OSTree storage.
- fail early when image os does not match host os
- Improve documentation on what to do with containers/image failures in test-skopeo
-   We now have the docker-archive: transport
-   Integration tests with built registries also exist
- Support /etc/docker/certs.d
- update image-spec to v1.0.0-rc6

* Tue May 23 2017 bbaude <bbaude@redhat.com> - 0.1.20-1.dev.git0224d8c
- BZ #1380078 - New release

* Tue Apr 25 2017 bbaude <bbaude@redhat.com> - 0.1.19-2.dev.git0224d8c
- No golang support for ppc64.  Adding exclude arch. BZ #1445490

* Tue Feb 28 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.19-1.dev.git0224d8c
- bump to v0.1.19-dev
- built commit 0224d8c

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.17-3.dev.git2b3af4a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.1.17-2.dev.git2b3af4a
- Rebuild for gpgme 1.18

* Tue Dec 06 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.17-1.dev.git2b3af4a
- bump to 0.1.17-dev

* Fri Nov 04 2016 Antonio Murdaca <runcom@fedoraproject.org> - 0.1.14-6.git550a480
- Fix BZ#1391932

* Tue Oct 18 2016 Antonio Murdaca <runcom@fedoraproject.org> - 0.1.14-5.git550a480
- Conflicts with atomic in skopeo-containers

* Wed Oct 12 2016 Antonio Murdaca <runcom@fedoraproject.org> - 0.1.14-4.git550a480
- built skopeo-containers

* Wed Sep 21 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.14-3.gitd830391
- built mtrmac/integrate-all-the-things commit d830391

* Thu Sep 08 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.14-2.git362bfc5
- built commit 362bfc5

* Thu Aug 11 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.14-1.gitffe92ed
- build origin/master commit ffe92ed

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.13-6
- https://fedoraproject.org/wiki/Changes/golang1.7

* Tue Jun 21 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.13-5
- include go-srpm-macros and compiler(go-compiler) in fedora conditionals
- define %%gobuild if not already
- add patch to build with older version of golang

* Thu Jun 02 2016 Antonio Murdaca <runcom@fedoraproject.org> - 0.1.13-4
- update to v0.1.12

* Tue May 31 2016 Antonio Murdaca <runcom@fedoraproject.org> - 0.1.12-3
- fix go build source path

* Fri May 27 2016 Antonio Murdaca <runcom@fedoraproject.org> - 0.1.12-2
- update to v0.1.12

* Tue Mar 08 2016 Antonio Murdaca <runcom@fedoraproject.org> - 0.1.11-1
- update to v0.1.11

* Tue Mar 08 2016 Antonio Murdaca <runcom@fedoraproject.org> - 0.1.10-1
- update to v0.1.10
- change runcom -> projectatomic

* Mon Feb 29 2016 Antonio Murdaca <runcom@fedoraproject.org> - 0.1.9-1
- update to v0.1.9

* Mon Feb 29 2016 Antonio Murdaca <runcom@fedoraproject.org> - 0.1.8-1
- update to v0.1.8

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- https://fedoraproject.org/wiki/Changes/golang1.6

* Fri Jan 29 2016 Antonio Murdaca <runcom@redhat.com> - 0.1.4
- First package for Fedora
