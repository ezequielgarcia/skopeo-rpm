
%global with_devel 0
%global with_bundled 1
%global with_unit_test 0
%global with_check 0

%if 0%{?fedora} > 28
%global with_debug 0
%else
%global with_debug 1
%endif # rawhide

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider github
%global provider_tld com
%global project containers
%global repo skopeo
# https://github.com/containers/skopeo
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path %{provider_prefix}
%global git0 https://%{import_path}
%global commit0 097549748afb1a26e912ddc090fa3524869cdc69
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
# manually listed arches due https://bugzilla.redhat.com/show_bug.cgi?id=1391932 (removed ppc64)
ExcludeArch: ppc64

Name: %{repo}
%if 0%{?fedora} > 28
Epoch: 1
%else
Epoch: 0
%endif
Version: 0.1.36
Release: 7.dev.git%{shortcommit0}%{?dist}
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

%if 0%{?fedora}
BuildRequires: go-srpm-macros
BuildRequires: compiler(go-compiler)
%endif
BuildRequires: git
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires: golang-github-cpuguy83-go-md2man
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
# Dependencies for containers/storage
BuildRequires: btrfs-progs-devel
BuildRequires: pkgconfig(devmapper)
BuildRequires: ostree-devel
BuildRequires: glib2-devel
BuildRequires: make
Requires: containers-common = 1:%{version}-%{release}

Provides: bundled(golang(github.com/beorn7/perks)) = 4c0e84591b9aa9e6dcfdf3e020114cd81f89d5f9
Provides: bundled(golang(github.com/BurntSushi/toml)) = master
Provides: bundled(golang(github.com/containerd/continuity)) = d8fb8589b0e8e85b8c8bbaa8840226d0dfeb7371
Provides: bundled(golang(github.com/containers/image)) = master
Provides: bundled(golang(github.com/containers/storage)) = master
Provides: bundled(golang(github.com/davecgh/go-spew)) = master
Provides: bundled(golang(github.com/docker/distribution)) = master
Provides: bundled(golang(github.com/docker/docker-credential-helpers)) = d68f9aeca33f5fd3f08eeae5e9d175edf4e731d1
Provides: bundled(golang(github.com/docker/docker)) = da99009bbb1165d1ac5688b5c81d2f589d418341
Provides: bundled(golang(github.com/docker/go-connections)) = 7beb39f0b969b075d1325fecb092faf27fd357b6
Provides: bundled(golang(github.com/docker/go-metrics)) = 399ea8c73916000c64c2c76e8da00ca82f8387ab
Provides: bundled(golang(github.com/docker/go-units)) = 8a7beacffa3009a9ac66bad506b18ffdd110cf97
Provides: bundled(golang(github.com/docker/libtrust)) = master
Provides: bundled(golang(github.com/ghodss/yaml)) = 73d445a93680fa1a78ae23a5839bad48f32ba1ee
Provides: bundled(golang(github.com/go-check/check)) = v1
Provides: bundled(golang(github.com/gogo/protobuf)) = fcdc5011193ff531a548e9b0301828d5a5b97fd8
Provides: bundled(golang(github.com/golang/glog)) = 44145f04b68cf362d9c4df2182967c2275eaefed
Provides: bundled(golang(github.com/golang/protobuf)) = 8d92cf5fc15a4382f8964b08e1f42a75c0591aa3
Provides: bundled(golang(github.com/gorilla/context)) = 14f550f51a
Provides: bundled(golang(github.com/gorilla/mux)) = e444e69cbd
Provides: bundled(golang(github.com/imdario/mergo)) = 6633656539c1639d9d78127b7d47c622b5d7b6dc
Provides: bundled(golang(github.com/kr/pretty)) = v0.1.0
Provides: bundled(golang(github.com/kr/text)) = v0.1.0
Provides: bundled(golang(github.com/matttproud/golang_protobuf_extensions)) = c12348ce28de40eed0136aa2b644d0ee0650e56c
Provides: bundled(golang(github.com/mistifyio/go-zfs)) = 22c9b32c84eb0d0c6f4043b6e90fc94073de92fa
Provides: bundled(golang(github.com/mtrmac/gpgme)) = master
Provides: bundled(golang(github.com/opencontainers/go-digest)) = master
Provides: bundled(golang(github.com/opencontainers/image-spec)) = 149252121d044fddff670adcdc67f33148e16226
Provides: bundled(golang(github.com/opencontainers/image-tools)) = 6d941547fa1df31900990b3fb47ec2468c9c6469
Provides: bundled(golang(github.com/opencontainers/runc)) = master
Provides: bundled(golang(github.com/opencontainers/runtime-spec)) = v1.0.0
Provides: bundled(golang(github.com/opencontainers/selinux)) = master
Provides: bundled(golang(github.com/ostreedev/ostree-go)) = aeb02c6b6aa2889db3ef62f7855650755befd460
Provides: bundled(golang(github.com/pborman/uuid)) = v1.0
Provides: bundled(golang(github.com/pkg/errors)) = master
Provides: bundled(golang(github.com/pmezard/go-difflib)) = master
Provides: bundled(golang(github.com/pquerna/ffjson)) = d49c2bc1aa135aad0c6f4fc2056623ec78f5d5ac
Provides: bundled(golang(github.com/prometheus/client_golang)) = c332b6f63c0658a65eca15c0e5247ded801cf564
Provides: bundled(golang(github.com/prometheus/client_model)) = 99fa1f4be8e564e8a6b613da7fa6f46c9edafc6c
Provides: bundled(golang(github.com/prometheus/common)) = 89604d197083d4781071d3c65855d24ecfb0a563
Provides: bundled(golang(github.com/prometheus/procfs)) = cb4147076ac75738c9a7d279075a253c0cc5acbd
Provides: bundled(golang(github.com/sirupsen/logrus)) = v1.0.0
Provides: bundled(golang(github.com/stretchr/testify)) = v1.1.3
Provides: bundled(golang(github.com/syndtr/gocapability)) = master
Provides: bundled(golang(github.com/tchap/go-patricia)) = v2.2.6
Provides: bundled(golang(github.com/ulikunitz/xz)) = v0.5.4
Provides: bundled(golang(github.com/urfave/cli)) = v1.17.0
Provides: bundled(golang(github.com/vbatts/tar-split)) = v0.10.2
Provides: bundled(golang(github.com/xeipuuv/gojsonpointer)) = master
Provides: bundled(golang(github.com/xeipuuv/gojsonreference)) = master
Provides: bundled(golang(github.com/xeipuuv/gojsonschema)) = master
Provides: bundled(golang(go4.org)) = master
Provides: bundled(golang(golang.org/x/crypto)) = master
Provides: bundled(golang(golang.org/x/net)) = master
Provides: bundled(golang(golang.org/x/sys)) = master
Provides: bundled(golang(golang.org/x/text)) = master
Provides: bundled(golang(gopkg.in/cheggaaa/pb.v1)) = ad4efe000aa550bb54918c06ebbadc0ff17687b9
Provides: bundled(golang(gopkg.in/yaml.v2)) = d466437aa4adc35830964cffc5b5f262c63ddcb4
Provides: bundled(golang(k8s.io/client-go)) = master

%description
Command line utility to inspect images and repositories directly on Docker
registries without the need to pull them

%if 0%{?with_devel}
%package devel
Summary: %{summary}
BuildArch: noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/Azure/go-ansiterm/winterm)
BuildRequires: golang(github.com/Sirupsen/logrus)
BuildRequires: golang(github.com/docker/distribution)
BuildRequires: golang(github.com/docker/distribution/context)
BuildRequires: golang(github.com/docker/distribution/digest)
BuildRequires: golang(github.com/docker/distribution/manifest)
BuildRequires: golang(github.com/docker/distribution/manifest/manifestlist)
BuildRequires: golang(github.com/docker/distribution/manifest/schema1)
BuildRequires: golang(github.com/docker/distribution/manifest/schema2)
BuildRequires: golang(github.com/docker/distribution/reference)
BuildRequires: golang(github.com/docker/distribution/registry/api/errcode)
BuildRequires: golang(github.com/docker/distribution/registry/api/v2)
BuildRequires: golang(github.com/docker/distribution/registry/client)
BuildRequires: golang(github.com/docker/distribution/registry/client/auth)
BuildRequires: golang(github.com/docker/distribution/registry/client/transport)
BuildRequires: golang(github.com/docker/distribution/registry/storage/cache)
BuildRequires: golang(github.com/docker/distribution/registry/storage/cache/memory)
BuildRequires: golang(github.com/docker/distribution/uuid)
BuildRequires: golang(github.com/docker/docker/api)
BuildRequires: golang(github.com/docker/docker/daemon/graphdriver)
BuildRequires: golang(github.com/docker/docker/distribution/metadata)
BuildRequires: golang(github.com/docker/docker/distribution/xfer)
BuildRequires: golang(github.com/docker/docker/dockerversion)
BuildRequires: golang(github.com/docker/docker/image)
BuildRequires: golang(github.com/docker/docker/image/v1)
BuildRequires: golang(github.com/docker/docker/layer)
BuildRequires: golang(github.com/docker/docker/opts)
BuildRequires: golang(github.com/docker/docker/pkg/archive)
BuildRequires: golang(github.com/docker/docker/pkg/chrootarchive)
BuildRequires: golang(github.com/docker/docker/pkg/fileutils)
BuildRequires: golang(github.com/docker/docker/pkg/homedir)
BuildRequires: golang(github.com/docker/docker/pkg/httputils)
BuildRequires: golang(github.com/docker/docker/pkg/idtools)
BuildRequires: golang(github.com/docker/docker/pkg/ioutils)
BuildRequires: golang(github.com/docker/docker/pkg/jsonlog)
BuildRequires: golang(github.com/docker/docker/pkg/jsonmessage)
BuildRequires: golang(github.com/docker/docker/pkg/longpath)
BuildRequires: golang(github.com/docker/docker/pkg/mflag)
BuildRequires: golang(github.com/docker/docker/pkg/parsers/kernel)
BuildRequires: golang(github.com/docker/docker/pkg/plugins)
BuildRequires: golang(github.com/docker/docker/pkg/pools)
BuildRequires: golang(github.com/docker/docker/pkg/progress)
BuildRequires: golang(github.com/docker/docker/pkg/promise)
BuildRequires: golang(github.com/docker/docker/pkg/random)
BuildRequires: golang(github.com/docker/docker/pkg/reexec)
BuildRequires: golang(github.com/docker/docker/pkg/stringid)
BuildRequires: golang(github.com/docker/docker/pkg/system)
BuildRequires: golang(github.com/docker/docker/pkg/tarsum)
BuildRequires: golang(github.com/docker/docker/pkg/term)
BuildRequires: golang(github.com/docker/docker/pkg/term/windows)
BuildRequires: golang(github.com/docker/docker/pkg/useragent)
BuildRequires: golang(github.com/docker/docker/pkg/version)
BuildRequires: golang(github.com/docker/docker/reference)
BuildRequires: golang(github.com/docker/docker/registry)
BuildRequires: golang(github.com/docker/engine-api/types)
BuildRequires: golang(github.com/docker/engine-api/types/blkiodev)
BuildRequires: golang(github.com/docker/engine-api/types/container)
BuildRequires: golang(github.com/docker/engine-api/types/filters)
BuildRequires: golang(github.com/docker/engine-api/types/image)
BuildRequires: golang(github.com/docker/engine-api/types/network)
BuildRequires: golang(github.com/docker/engine-api/types/registry)
BuildRequires: golang(github.com/docker/engine-api/types/strslice)
BuildRequires: golang(github.com/docker/go-connections/nat)
BuildRequires: golang(github.com/docker/go-connections/tlsconfig)
BuildRequires: golang(github.com/docker/go-units)
BuildRequires: golang(github.com/docker/libtrust)
BuildRequires: golang(github.com/gorilla/context)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer/user)
BuildRequires: golang(github.com/vbatts/tar-split/archive/tar)
BuildRequires: golang(github.com/vbatts/tar-split/tar/asm)
BuildRequires: golang(github.com/vbatts/tar-split/tar/storage)
BuildRequires: golang(golang.org/x/net/context)
%endif

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary: Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires: %{name}-devel = %{version}-%{release}

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%package -n containers-common
Summary: Configuration files for working with image signatures
Obsoletes: atomic <= 1.13.1-2
Conflicts: atomic-registries <= 1.22.1-1
Obsoletes: docker-rhsubscription <= 2:1.13.1-31
Provides: %{name}-containers = 1:%{version}-%{release}
Obsoletes: %{name}-containers <= 1:0.1.31-2

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

%if ! 0%{?with_bundled}
rm -rf vendor/
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/vendor:%{gopath}
%endif

%gobuild -o %{name} ./cmd/%{name}
%{__make} docs

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_sysconfdir}
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/containers/storage.conf
mkdir -p %{buildroot}%{_mandir}/man5
go-md2man -in %{SOURCE2} -out %{buildroot}%{_mandir}/man5/containers-storage.conf.5
go-md2man -in %{SOURCE4} -out %{buildroot}%{_mandir}/man5/registries.conf.5
install -p -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/containers/
mkdir -p %{buildroot}%{_sysconfdir}/containers/certs.d
go-md2man -in %{SOURCE6} -out %{buildroot}%{_mandir}/man5/policy.json.5

mkdir -p %{buildroot}%{_datadir}/containers
install -m0644 %{SOURCE3} %{buildroot}%{_datadir}/containers/mounts.conf
install -m0644 %{SOURCE7} %{buildroot}%{_datadir}/containers/seccomp.json

# install secrets patch directory
install -d -p -m 755 %{buildroot}/%{_datadir}/rhel/secrets
# rhbz#1110876 - update symlinks for subscription management
ln -s %{_sysconfdir}/pki/entitlement %{buildroot}%{_datadir}/rhel/secrets/etc-pki-entitlement
ln -s %{_sysconfdir}/rhsm %{buildroot}%{_datadir}/rhel/secrets/rhsm
ln -s %{_sysconfdir}/yum.repos.d/redhat.repo %{buildroot}%{_datadir}/rhel/secrets/rhel7.repo

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go" | grep -v "./vendor") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go" | grep -v "./vendor"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%gotest %{import_path}/integration
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc README.md
%endif

%files -n containers-common
%dir %{_sysconfdir}/containers
%dir %{_sysconfdir}/containers/certs.d
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
* Tue Mar 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-7.dev.git0975497
- autobuilt 0975497

* Tue Mar 19 2019 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.1.36-6.dev.git2134209
- make /usr/share/rhel/secrets world searchable.   This will help allow RHEL containers to be built with rootless.

* Thu Mar 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-5.dev.gitd93a581
- autobuilt d93a581

* Wed Mar 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-4.dev.git94728fb
- autobuilt 94728fb

* Thu Mar 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-3.dev.git0490018
- autobuilt 0490018

* Wed Mar 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-2.dev.git2031e17
- autobuilt 2031e17

* Tue Mar 05 2019 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.1.36-1.dev.git2134209
- Bump version

* Sat Mar 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-14.dev.git2134209
- autobuilt 2134209

* Fri Mar 1 2019 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.1.35-13.dev.git932b037
- Add /etc/containers/certs.d to containers-common
- Update containers-storage.conf man page to match latest upstream
- Update registries.conf man page to match latest upstream

* Sat Feb 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-12.dev.git932b037
- autobuilt 932b037

* Sun Feb 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-11.dev.gitfee5981
- autobuilt fee5981

* Thu Feb 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-10.dev.gitb8b9913
- autobuilt b8b9913

* Wed Feb 13 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.35-9.dev.gitb329dd0
- drop conditional epoch for containers-common, module build seems to fail
without it

* Wed Feb 13 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.35-8.dev.gitb329dd0
- Epoch changes for containers-common

* Fri Feb 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-7.dev.gitb329dd0
- autobuilt b329dd0

* Sat Feb 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-6.dev.gitbba2874
- autobuilt bba2874

* Fri Jan 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-5.dev.git42b01df
- autobuilt 42b01df

* Wed Jan 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-4.dev.gitf7c608e
- autobuilt f7c608e

* Sat Jan 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-3.dev.git17bea86
- autobuilt 17bea86

* Sat Dec 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.35-2.dev.git3e98377
- bump to 0.1.35
- autobuilt 3e98377

* Thu Dec 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.34-2.dev.git05212df
- bump to 0.1.34
- autobuilt 05212df

* Wed Dec 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.33-6.dev.gitecd675e
- autobuilt ecd675e

* Sat Dec 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.33-5.dev.gita51e38e
- autobuilt a51e38e

* Fri Dec 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.33-4.dev.git41d8dd8
- autobuilt 41d8dd8

* Fri Nov 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.33-3.dev.gitfbc2e4f
- autobuilt fbc2e4f

* Fri Nov 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.33-2.dev.git761a681
- autobuilt 761a681

* Wed Nov 07 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.33-1.dev.git.git5aa217f
- bump to 0.1.33
- built commit 5aa217f

* Sat Aug 18 2018 Kevin Fenzi <kevin@scrye.com> - 1:0.1.32-2.dev.git.gite814f96
- Fix containers-common requires to also use Epoch so skopeo is installable again.

* Sat Aug 11 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.32-1.dev.gite814f96
- bump to v0.1.32-dev
- built commit e814f96
- bump Epoch to 1, cause my autobuilder messed up earlier
- use %%gobuild
- add bundled Provides

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.1.320.1.32-2.dev.gite814f961
- Rebuild with fixed binutils

* Mon Jul 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.320.1.32-1.dev.gite814f961
- bump to 0.1.32
- autobuilt e814f96

* Wed Jul 25 2018 dwalsh <dwalsh@redhat.com> - 0.1.31-13.gite3034e1
- Update to latest storage.conf file
- Update to latest man pages

* Wed Jul 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-12.dev.gite3034e1
- autobuilt e3034e1

* Tue Jul 24 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.31-11.dev.gitae64ff7
- Resolves: #1606365 - solve FTBFS - disable debuginfo for rawhide (f29)
- remove centos conditionals, CentOS Virt SIG gets rhel rebuilds

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.31-10.dev.gitae64ff7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-9.gitae64ff7
- autobuilt ae64ff7

* Tue Jul 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-8.git196bc48
- autobuilt 196bc48

* Sat Jun 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-7.git6e23a32
- autobuilt 6e23a32

* Thu Jun 21 2018 dwalsh <dwalsh@redhat.com> - 0.1.31-6.git0144aa8
- add statx to seccomp.json to containers-config

* Thu Jun 7 2018 dwalsh <dwalsh@redhat.com> - 0.1.31-5.git0144aa8
- add seccomp.json to containers-config

* Thu May 31 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-4.git0144aa8
- autobuilt 0144aa8

* Wed May 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.31-3.gitf9baaa6
- should obsolete older skopeo-containers

* Wed May 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.31-2.gitf9baaa6
- rename skopeo-containers to containers-common
- enable debuginfo

* Sat May 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.31-1.gitf9baaa6
- bump to 0.1.31
- autobuilt f9baaa6

* Tue May 22 2018 dwalsh <dwalsh@redhat.com> - 0.1.30-14.git0b8ab9
- Add devicemapper support

* Wed May 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-13.git7e9a664
- autobuilt 7e9a664

* Tue May 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-12.git2d04db9
- autobuilt 2d04db9

* Sat May 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-11.git79225f2
- autobuilt 79225f2

* Fri May 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-10.gitc4808f0
- autobuilt c4808f0

* Tue May 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-9.git1f11b8b
- autobuilt 1f11b8b

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-8.gitab2bc6e
- autobuilt commit ab2bc6e

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-7.gitab2bc6e
- autobuilt commit ab2bc6e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-6.gitab2bc6e
- autobuilt commit ab2bc6e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-5.gitab2bc6e
- autobuilt commit ab2bc6e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-4.gitab2bc6e
- autobuilt commit ab2bc6e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-3.gitab2bc6e
- autobuilt commit ab2bc6e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.1.30-2.gitab2bc6e
- autobuilt commit ab2bc6e

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.30-1.git28080c8
- bump to 0.1.30
- autobuilt commit 28080c8
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
-       it is used by containers/image for pulling images to the OSTree storage.
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
