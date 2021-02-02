%global with_check 0

%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0

%if 0%{?rhel} > 7 && ! 0%{?fedora}
%define gobuild(o:) \
go build -buildmode pie -compiler gc -tags="rpm_crashtraceback libtrust_openssl ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -compressdwarf=false -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags'" -a -v %{?**};
%else
%define gobuild(o:) GO111MODULE=off go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld '" -a -v %{?**};
%endif

%global import_path github.com/containers/skopeo
%global branch release-1.2
# Bellow definitions are used to deliver config files from a particular branch
# of c/image, c/common, c/storage vendored in all podman, skopeo, buildah.
# These vendored components must have the same version. If it is not the case,
# pick the oldest version on c/image, c/common, c/storage vendored in
# podman/skopeo/podman.
%global podman_branch v3.0
%global image_branch  v5.9.0
%global common_branch v0.33.0
%global storage_branch v1.24.5
%global shortnames_branch main
%global commit0 a05ddb8d1de6d8e4220c936850308f4c595eba66
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Epoch: 1
Name: skopeo
Version: 1.2.1
Release: 5%{?dist}
Summary: Inspect container images and repositories on registries
License: ASL 2.0
URL: %{git0}
# https://fedoraproject.org/wiki/PackagingDrafts/Go#Go_Language_Architectures
#ExclusiveArch: %%{go_arches}
# still use arch exclude as the macro above still refers %%{ix86} in RHEL8.4:
# https://bugzilla.redhat.com/show_bug.cgi?id=1905383
ExcludeArch: %{ix86}
%if 0%{?branch:1}
Source0: https://%{import_path}/tarball/%{commit0}/%{branch}-%{shortcommit0}.tar.gz
%else
Source0: https://%{import_path}/archive/%{commit0}/%{name}-%{version}-%{shortcommit0}.tar.gz
%endif
Source1: https://raw.githubusercontent.com/containers/storage/%{storage_branch}/storage.conf
Source2: https://raw.githubusercontent.com/containers/storage/%{storage_branch}/docs/containers-storage.conf.5.md
Source3: mounts.conf
Source4: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-registries.conf.5.md
#Source5: https://raw.githubusercontent.com/containers/image/%%{image_branch}/registries.conf
Source5: registries.conf
Source6: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-policy.json.5.md
Source7: https://raw.githubusercontent.com/containers/common/%{common_branch}/pkg/seccomp/seccomp.json
Source8: https://raw.githubusercontent.com/containers/podman/%{podman_branch}/docs/source/markdown/containers-mounts.conf.5.md
Source9: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-signature.5.md
Source10: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-transports.5.md
Source11: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-certs.d.5.md
Source12: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-registries.d.5.md
Source13: https://raw.githubusercontent.com/containers/common/%{common_branch}/pkg/config/containers.conf
Source14: https://raw.githubusercontent.com/containers/common/%{common_branch}/docs/containers.conf.5.md
Source15: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-auth.json.5.md
Source16: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-registries.conf.d.5.md
Source17: https://raw.githubusercontent.com/containers/shortnames/%{shortnames_branch}/shortnames.conf
Source18: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-registries.conf.5.md
Source19: rhel-shortnames.conf
BuildRequires: git
BuildRequires: golang >= 1.12.12-4
BuildRequires: go-md2man
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: pkgconfig(devmapper)
BuildRequires: ostree-devel
BuildRequires: glib2-devel
BuildRequires: make
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
Suggests: subscription-manager

%description -n containers-common
This package installs a default signature store configuration and a default
policy under `/etc/containers/`.

%package tests
Summary:         Tests for %{name}
Requires: %{name} = %{epoch}:%{version}-%{release}
#Requires: bats  (which RHEL8 doesn't have. If it ever does, un-comment this)
Requires: gnupg
Requires: jq
Requires: podman
Requires: httpd-tools

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

export GOPATH=$(pwd):$(pwd)/vendor:%{gopath}
export GO111MODULE=off
export CGO_CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export BUILDTAGS="exclude_graphdriver_btrfs btrfs_noversion $(hack/libdm_tag.sh) $(hack/ostree_tag.sh)"
mkdir -p bin
%gobuild -o bin/%{name} ./cmd/%{name}
%{__make} docs

%install
make \
   DESTDIR=%{buildroot} \
   SIGSTOREDIR=%{buildroot}%{_sharedstatedir}/containers/sigstore \
   install
install -dp %{buildroot}%{_sysconfdir}/containers/{certs.d,oci/hooks.d,registries.d,registries.conf.d}
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/containers/storage.conf
install -m0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/containers/registries.conf
install -m0644 %{SOURCE17} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/shortnames.conf
install -m0644 %{SOURCE19} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/rhel-shortnames.conf
install -dp %{buildroot}%{_mandir}/man5
go-md2man -in %{SOURCE2} -out %{buildroot}%{_mandir}/man5/containers-storage.conf.5
go-md2man -in %{SOURCE4} -out %{buildroot}%{_mandir}/man5/containers-registries.conf.5
go-md2man -in %{SOURCE6} -out %{buildroot}%{_mandir}/man5/containers-policy.json.5
go-md2man -in %{SOURCE8} -out %{buildroot}%{_mandir}/man5/containers-mounts.conf.5
go-md2man -in %{SOURCE9} -out %{buildroot}%{_mandir}/man5/containers-signature.5
go-md2man -in %{SOURCE10} -out %{buildroot}%{_mandir}/man5/containers-transports.5
go-md2man -in %{SOURCE11} -out %{buildroot}%{_mandir}/man5/containers-certs.d.5
go-md2man -in %{SOURCE12} -out %{buildroot}%{_mandir}/man5/containers-registries.d.5
go-md2man -in %{SOURCE18} -out %{buildroot}%{_mandir}/man5/containers-registries.conf.d.5
go-md2man -in %{SOURCE14} -out %{buildroot}%{_mandir}/man5/containers.conf.5
go-md2man -in %{SOURCE15} -out %{buildroot}%{_mandir}/man5/containers-auth.json.5
go-md2man -in %{SOURCE16} -out %{buildroot}%{_mandir}/man5/containers-registries.conf.d.5

install -dp %{buildroot}%{_datadir}/containers
install -m0644 %{SOURCE3} %{buildroot}%{_datadir}/containers/mounts.conf
install -m0644 %{SOURCE7} %{buildroot}%{_datadir}/containers/seccomp.json
install -m0644 %{SOURCE13} %{buildroot}%{_datadir}/containers/containers.conf

# install secrets patch directory
install -d -p -m 755 %{buildroot}/%{_datadir}/rhel/secrets
# rhbz#1110876 - update symlinks for subscription management
ln -s %{_sysconfdir}/pki/entitlement %{buildroot}%{_datadir}/rhel/secrets/etc-pki-entitlement
ln -s %{_sysconfdir}/rhsm %{buildroot}%{_datadir}/rhel/secrets/rhsm
ln -s %{_sysconfdir}/yum.repos.d/redhat.repo %{buildroot}%{_datadir}/rhel/secrets/redhat.repo

# ship preconfigured /etc/containers/registries.d/ files with containers-common - #1903813
cat <<EOF > %{buildroot}%{_sysconfdir}/containers/registries.d/registry.access.redhat.com.yaml
docker:
     registry.access.redhat.com:
         sigstore: https://access.redhat.com/webassets/docker/content/sigstore
EOF

cat <<EOF > %{buildroot}%{_sysconfdir}/containers/registries.d/registry.redhat.io.yaml
docker:
     registry.redhat.io:
         sigstore: https://registry.redhat.io/containers/sigstore
EOF

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

%files -n containers-common
%dir %{_sysconfdir}/containers
%dir %{_sysconfdir}/containers/certs.d
%dir %{_sysconfdir}/containers/registries.d
%dir %{_sysconfdir}/containers/oci
%dir %{_sysconfdir}/containers/oci/hooks.d
%dir %{_sysconfdir}/containers/registries.conf.d
%config(noreplace) %{_sysconfdir}/containers/policy.json
%config(noreplace) %{_sysconfdir}/containers/registries.d/default.yaml
%config(noreplace) %{_sysconfdir}/containers/storage.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf.d/shortnames.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf.d/rhel-shortnames.conf
%config(noreplace) %{_sysconfdir}/containers/registries.d/*.yaml
%ghost %{_sysconfdir}/containers/containers.conf
%dir %{_sharedstatedir}/containers/sigstore
%{_mandir}/man5/*
%dir %{_datadir}/containers
%{_datadir}/containers/mounts.conf
%{_datadir}/containers/seccomp.json
%{_datadir}/containers/containers.conf
%dir %{_datadir}/rhel/secrets
%{_datadir}/rhel/secrets/*

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}

%files tests
%license LICENSE
%{_datadir}/%{name}/test

%changelog
* Tue Feb 02 2021 Jindrich Novy <jnovy@redhat.com> - 1:1.2.1-5
- update to the latest content of https://github.com/containers/skopeo/tree/release-1.2
  (https://github.com/containers/skopeo/commit/a05ddb8)

* Sun Jan 31 2021 Jindrich Novy <jnovy@redhat.com> - 1:1.2.1-4
- define 8.4.0 branch for podman (v3.0)
- remove redundant source file

* Fri Jan 29 2021 Jindrich Novy <jnovy@redhat.com> - 1:1.2.1-3
- convert subscription-manager from weak dep to a hint

* Tue Jan 19 2021 Jindrich Novy <jnovy@redhat.com> - 1:1.2.1-2
- fix rhel-shortnames.conf generation (avoid duplicates and records
  with invalid URL)
- Related: #1883490

* Thu Jan 14 2021 Jindrich Novy <jnovy@redhat.com> - 1:1.2.1-1
- ship preconfigured /etc/containers/registries.d/ files with containers-common

* Tue Dec 01 2020 Jindrich Novy <jnovy@redhat.com> - 1:1.2.0-6
- unify vendored branches
- add validation script

* Thu Nov 05 2020 Jindrich Novy <jnovy@redhat.com> - 1:1.2.0-5
- simplify spec file
- use short commit ID in tarball name

* Fri Oct 23 2020 Jindrich Novy <jnovy@redhat.com> - 1:1.2.0-4
- use shortcommit ID in branch tarball name

* Thu Oct 22 2020 Jindrich Novy <jnovy@redhat.com> - 1:1.2.0-3
- update sources and allow to deliver from upstream branch

* Fri Sep 25 2020 Jindrich Novy <jnovy@redhat.com> - 1:1.2.0-2
- fix build of the new skopeo-1.2.0

* Fri Sep 25 2020 Jindrich Novy <jnovy@redhat.com> - 1:1.2.0-1
- update to https://github.com/containers/skopeo/releases/tag/v1.2.0

* Thu Sep 17 2020 Jindrich Novy <jnovy@redhat.com> - 1:1.1.1-4
- sync with rhel8-8.3.0
- propagate proper CFLAGS to CGO_CFLAGS to assure code hardening and optimization
- Related: #1821193

* Wed Jun 19 2019 Eduardo Santiago <santiago@redhat.com> - 1:0.1.37-1
- Resolves: #1720654 - rebase to v0.1.37
- Resolves: #1721247 - enable fips mode
- add emergency debugging patch for figuring out gating-tests problem

* Tue Jun  4 2019 Eduardo Santiago <santiago@redhat.com> - 1:0.1.36-1.git6307635
- built upstream tag v0.1.36, including system tests

* Tue Apr 30 2019 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.32-4.git1715c90
- Fixes @openshift/machine-config-operator#669
- install /etc/containers/oci/hooks.d and /etc/containers/certs.d

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
