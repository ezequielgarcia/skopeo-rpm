%global with_devel 0
%global with_bundled 1
%global with_unit_test 0
%global with_check 0

%if 0%{?fedora}
%global with_debug 1
%else
%global with_debug 0
%endif

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) GO111MODULE=off go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld '" -a -v -x %{?**};
%endif

%if 0%{?fedora} && ! 0%{?rhel}
%define conditional_epoch 1
%else
%define conditional_epoch 2
%endif

%global provider github
%global provider_tld com
%global project containers
%global repo skopeo
# https://github.com/containers/skopeo
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global git0 https://%{import_path}
%global commit0 f5a028e4d9dd2bec64d3adff150604f3bb1b7074
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Used for comparing with latest upstream tag
# to decide whether to autobuild and set download url (non-rawhide only)
%define built_tag v1.2.2
%define built_tag_strip %(b=%{built_tag}; echo ${b:1})
%define download_url %{git0}/archive/%{built_tag}.tar.gz

Name: %{repo}
Epoch: %{conditional_epoch}
Version: 1.2.2
Release: 35.dev.git%{shortcommit0}%{?dist}
Summary: Inspect container images and repositories on registries
License: ASL 2.0
URL: %{git0}
Source0: %{git0}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
%if 0%{?fedora}
BuildRequires: go-srpm-macros
BuildRequires: compiler(go-compiler)
%endif
BuildRequires: git-core
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires: go-md2man
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
# Dependencies for containers/storage
%if 0%{?fedora} || 0%{?rhel} <= 7
BuildRequires: btrfs-progs-devel
%endif
BuildRequires: pkgconfig(devmapper)
BuildRequires: ostree-devel
BuildRequires: glib2-devel
BuildRequires: make
Requires: containers-common >= 4:1-6
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

%package tests
Summary: Tests for %{name}

Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: bats
Requires: gnupg
Requires: jq
Requires: podman
Requires: httpd-tools
Requires: openssl

%description tests
%{summary}

This package contains system tests for %{name}

%prep
%autosetup -Sgit -n %{name}-%{commit0}
sed -i 's/install-binary: bin\/%{name}/install-binary:/' Makefile
sed -i 's/install-docs: docs/install-docs:/' Makefile

%build
mkdir -p src/github.com/containers
ln -s ../../../ src/%{import_path}

export CGO_CFLAGS='-O2 -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -ffat-lto-objects -fexceptions -fasynchronous-unwind-tables -fstack-protector-strong -fstack-clash-protection -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64'
%ifarch x86_64
export CGO_CFLAGS="$CGO_CFLAGS -m64 -mtune=generic -fcf-protection"
%endif
# These extra flags present in %%{optflags} have been skipped for now as they break the build
#export CGO_CFLAGS="$CGO_CFLAGS -flto=auto -Wp,D_GLIBCXX_ASSERTIONS -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1"

mkdir -p vendor/src
for v in vendor/*; do
    if test ${v} = vendor/src; then continue; fi
    if test -d ${v}; then 
      mv ${v} vendor/src/
    fi
done

%if ! 0%{?with_bundled}
rm -rf vendor/
export GOPATH=$(pwd)
%else
export GOPATH=$(pwd):$(pwd)/vendor
%endif

mkdir -p bin
%if 0%{?centos} >= 8
export BUILDTAGS='exclude_graphdriver_btrfs btrfs_noversion'
%endif
%gobuild -o bin/%{name} ./cmd/%{name}
pushd docs
for file in $(ls | grep 1.md)
do
export FILE_OUT=$(echo $file | sed -e 's/\.md//')
go-md2man -in $file -out $FILE_OUT 
done
popd

%install
make \
    PREFIX=%{_prefix} DESTDIR=%{buildroot} \
    install-binary install-docs install-completions

# system tests
install -d -p %{buildroot}/%{_datadir}/%{name}/test/system
cp -pav systemtest/* %{buildroot}/%{_datadir}/%{name}/test/system/

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
* Wed Mar 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-35.dev.gitf5a028e
- autobuilt f5a028e

* Tue Mar 09 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-34.dev.git3d1d297
- autobuilt 3d1d297

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-33.dev.git035eb33
- autobuilt 035eb33

* Mon Mar 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-32.dev.git6cbb0c4
- autobuilt 6cbb0c4

* Mon Mar 08 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-31.dev.git663fe44
- built commit 663fe44

* Wed Mar 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-30.dev.git6cbb0c4
- autobuilt 6cbb0c4

* Mon Mar 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-29.dev.git663fe44
- autobuilt 663fe44

* Wed Feb 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-28.dev.gitb7bf15b
- autobuilt b7bf15b

* Wed Feb 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-27.dev.git61b62f9
- autobuilt 61b62f9

* Tue Feb 23 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-26.dev.git2c8655e
- autobuilt 2c8655e

* Mon Feb 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-25.dev.gitbe60097
- autobuilt be60097

* Wed Feb 17 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-24.dev.git15f0d5c
- autobuilt 15f0d5c

* Thu Feb 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-23.dev.git6fa6342
- autobuilt 6fa6342

* Wed Feb 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-22.dev.gite224b78
- autobuilt e224b78

* Tue Feb 09 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-21.dev.git1c4b0fc
- fix build and update containers-common dependency

* Mon Feb 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-20.dev.git1c4b0fc
- autobuilt 1c4b0fc

* Wed Feb 03 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-19.dev.gitaff1b62
- autobuilt aff1b62

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-18.dev.gite0ba05a
- autobuilt e0ba05a

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-17.dev.git55b9782
- autobuilt 55b9782

* Mon Feb 01 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-16.dev.git3375a90
- autobuilt 3375a90

* Sat Jan 30 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-15.dev.gitf3c8d26
- autobuilt f3c8d26

* Sat Jan 30 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-14.dev.gita9e9bdc
- autobuilt a9e9bdc

* Thu Jan 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-13.dev.git77a2e08
- autobuilt 77a2e08

* Thu Jan 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-12.dev.gita3c21f2
- autobuilt a3c21f2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.2-11.dev.gitefc0170
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-10.dev.gitefc0170
- autobuilt efc0170

* Thu Jan 21 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-9.dev.git0d0a97e
- autobuilt 0d0a97e

* Fri Jan 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-8.dev.gitef6f46a
- autobuilt ef6f46a

* Thu Jan 14 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-7.dev.git3156212
- autobuilt 3156212

* Tue Jan 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-6.dev.git2e90a8a
- Requires: containers-common-4:0.33.0-2

* Tue Jan 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-5.dev.git2e90a8a
- depend on containers-common >= 4:0.33.0-1

* Tue Jan 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.2-4.dev.git2e90a8a
- depend on standalone containers-common package

* Mon Jan 11 2021 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.2.2-3.dev.git2e90a8a
- Update documentaton for containers.conf, seccomp.json and new shortnames.conf

* Mon Jan 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.2-2.dev.git2e90a8a
- bump to 1.2.2
- autobuilt 2e90a8a

* Sun Jan 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-43.dev.gitbeadcbb
- autobuilt beadcbb

* Sat Jan  9 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-42.dev.gitac07bf2
- autobuilt ac07bf2

* Fri Jan  8 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-41.dev.gitb0da056
- autobuilt b0da056

* Fri Jan  8 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-40.dev.gitc4fb936
- autobuilt c4fb936

* Mon Jan  4 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-39.dev.git81535c5
- autobuilt 81535c5

* Wed Dec 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-38.dev.git84232cf
- autobuilt 84232cf

* Tue Dec 22 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.2.1-37.dev.git342b839
- Update man pages and conf files for containers-common

* Mon Dec 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-36.dev.git342b839
- autobuilt 342b839

* Sat Dec 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-35.dev.git6294875
- autobuilt 6294875

* Tue Dec  8 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-34.dev.git4769dd0
- autobuilt 4769dd0

* Tue Dec 8 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.2.1-33.dev.git4aaa9b4
- Update man pages and conf files for containers-common

* Tue Dec  8 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-32.dev.git4aaa9b4
- autobuilt 4aaa9b4

* Mon Dec  7 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-31.dev.gited32180
- autobuilt ed32180

* Sat Dec  5 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.1-30.dev.git5b8fe7f
- harden cgo binaries
- Reported-by: Wade Mealing <wmealing@gmail.com>

* Fri Dec  4 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-29.dev.git5b8fe7f
- autobuilt 5b8fe7f

* Mon Nov 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-28.dev.git1b813f8
- autobuilt 1b813f8

* Tue Nov 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-27.dev.git42e9121
- autobuilt 42e9121

* Sat Nov 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-26.dev.gitc88576b
- autobuilt c88576b

* Fri Nov 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-25.dev.git0f4dc80
- autobuilt 0f4dc80

* Thu Nov 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-23.dev.git7fee912
- autobuilt 7fee912

* Tue Nov 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-22.dev.git2342171
- autobuilt 2342171

* Mon Nov 16 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.2.1-21.dev.git1a3ae14
- Add initial shortnames.conf file for expanding shortnames

* Mon Nov 16 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.2.1-20.dev.git1a3ae14
- Update man pages and storage.conf
- Add update.sh to make getting man pages and configuration files easier

* Fri Nov 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-19.dev.git4ad2c75
- autobuilt 4ad2c75

* Thu Nov 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-18.dev.git11b4fd3
- autobuilt 11b4fd3

* Mon Nov 9 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.2.1-17.dev.git1a3ae14
- Fix default ping range in containers.conf
- Allow setting of --remote default in containers.conf

* Sat Nov  7 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-16.dev.git1a3ae14
- autobuilt 1a3ae14

* Thu Nov  5 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-15.dev.git32e2425
- autobuilt 32e2425

* Mon Oct 26 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.2.1-14.dev.gitceaee44
- fix seccomp.json typos

* Thu Oct 22 2020 Jindrich Novy <jnovy@redhat.com> - 1:1.2.1-13.dev.gitceaee44
- use %%rhel instead of %%eln

* Wed Oct 21 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.2.1-12.dev.gitceaee44
- Add time64 syscalls to seccomp.json

* Wed Oct 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-11.dev.gitceaee44
- autobuilt ceaee44

* Thu Oct 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-10.dev.git362f70b
- autobuilt 362f70b

* Sat Oct 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-9.dev.git10da9f7
- autobuilt 10da9f7

* Thu Oct  8 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-8.dev.git4cc72b9
- autobuilt 4cc72b9

* Tue Oct  6 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:1.2.1-7.dev.git027d7e4
- no btrfs for eln or centos >= 8
- use old style changelogs without timezone/timestamp

* Sat Oct  3 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-6.dev.git027d7e4
- autobuilt 027d7e4

* Fri Oct 2 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.2.1-5.dev.gitd8bc8b6
- Add SETFCAP back into default capabilities
- Remove AUDIT_WRITE from default capabilities

* Fri Oct  2 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-4.dev.gitd8bc8b6
- autobuilt d8bc8b6

* Wed Sep 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-3.dev.git6dabefa
- autobuilt 6dabefa

* Fri Sep 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.2.1-2.dev.git44beab6
- bump to 1.2.1
- autobuilt 44beab6

* Fri Sep 25 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.1.1-51.dev.git5d5756c
- Modify the range of groups used in net.ipv4.ping_group_range to be 1 so that
- it will work more easily with User Namespaces
- Also turn back on AUDIT_WRITE until seccomp.json file is fixed

* Mon Sep 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-50.dev.git8151b89
- autobuilt 8151b89

* Mon Sep 21 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.1.1-49.dev.git5d5756c
- Add SYS_CHROOT back into default capabilities

* Mon Sep 21 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.1.1-48.dev.git5d5756c
- Remove fchmodat2 from seccomp.json (This syscall does not exist yet)

* Fri Sep 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-47.dev.git77293ff
- autobuilt 77293ff

* Thu Sep 17 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.1.1-46.dev.git5d5756c
- Remove NET_RAW, SYS_CHROOT, MKNOD and AUDIT_WRITE from default list of capabilities
- Turn on ping for 65k users

* Tue Sep 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-45.dev.gitbbd800f
- autobuilt bbd800f

* Mon Sep 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-44.dev.git12ab19f
- autobuilt 12ab19f

* Sat Sep 12 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.1.1-43.dev.git5d5756c
- update man pages
- Update seccomp rules
- Update configuration files in containers-common
- Update configuration files in containers-storage

* Fri Sep 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-42.dev.git45a9efb
- autobuilt 45a9efb

* Wed Sep  9 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-41.dev.git5dd09d7
- autobuilt 5dd09d7

* Wed Sep  9 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-40.dev.git23cb1b7
- autobuilt 23cb1b7

* Wed Sep  2 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-39.dev.git662f9ac
- autobuilt 662f9ac

* Wed Sep  2 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-38.dev.gitae26454
- autobuilt ae26454

* Fri Aug 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-37.dev.gitc4998eb
- autobuilt c4998eb

* Thu Aug 27 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-36.dev.gita13b581
- autobuilt a13b581

* Mon Aug 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-35.dev.git87484a1
- autobuilt 87484a1

* Wed Aug 19 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.1.1-34.dev.git5d5756c
- Update configuration files in containers-common
- Update configuration files in containers-storage

* Wed Aug 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-33.dev.git5d5756c
- autobuilt 5d5756c

* Wed Aug 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-32.dev.git88c8c47
- autobuilt 88c8c47

* Tue Aug 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-31.dev.gitea10e61
- autobuilt ea10e61

* Mon Aug 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-30.dev.git0c2c7f4
- autobuilt 0c2c7f4

* Sun Aug 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-29.dev.git0f94dbc
- autobuilt 0f94dbc

* Sat Aug 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-28.dev.gitbaeaad6
- autobuilt baeaad6

* Fri Aug 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-27.dev.git78d2f67
- autobuilt 78d2f67

* Mon Aug 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-26.dev.gitc052ed7
- autobuilt c052ed7

* Mon Aug 03 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-25.dev.git5e88eb5
- autobuilt 5e88eb5

* Sun Aug 2 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.1.1-23.dev.git62fd5a7
- Update configuration files in containers-common
- Update configuration files in containers-storage

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-23.dev.git62fd5a7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-22.dev.git62fd5a7
- autobuilt 62fd5a7

* Thu Jul 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-21.dev.git6252c22
- autobuilt 6252c22

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-20.dev.git153f18d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-19.dev.git153f18d
- autobuilt 153f18d

* Sat Jul 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-18.dev.git494d237
- autobuilt 494d237

* Fri Jul 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-17.dev.git89fb89a
- autobuilt 89fb89a

* Thu Jul 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-16.dev.git29eec32
- autobuilt 29eec32

* Thu Jul 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-15.dev.git2fa7b99
- autobuilt 2fa7b99

* Sat Jul 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-14.dev.git6284ceb
- autobuilt 6284ceb

* Sat Jul 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-13.dev.git6e295a2
- autobuilt 6e295a2

* Fri Jul 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-12.dev.gitf63685f
- autobuilt f63685f

* Thu Jul 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-11.dev.gitdc5f68f
- autobuilt dc5f68f

* Thu Jul 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-10.dev.git840c487
- autobuilt 840c487

* Wed Jul 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-9.dev.gitee72e80
- autobuilt ee72e80

* Thu Jul 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-8.dev.git6182aa3
- autobuilt 6182aa3

* Wed Jul 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-7.dev.gitac6b871
- autobuilt ac6b871

* Tue Jun 30 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.1.1-6.dev.gitba8cbf5
- Update configuration files in containers-common

* Fri Jun 26 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-5.dev.gitba8cbf5
- autobuilt ba8cbf5

* Mon Jun 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-4.dev.git7815c8a
- autobuilt 7815c8a

* Mon Jun 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-3.dev.git233e61c
- autobuilt 233e61c

* Thu Jun 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.1.1-2.dev.git96bd4a0
- bump to 1.1.1
- autobuilt 96bd4a0

* Thu Jun 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-17.dev.git6b78619
- autobuilt 6b78619

* Wed Jun 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-16.dev.git091f924
- autobuilt 091f924

* Wed Jun 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-15.dev.gitb70dfae
- autobuilt b70dfae

* Tue Jun 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-14.dev.git0bd78a0
- autobuilt 0bd78a0

* Thu Jun 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-13.dev.git827293a
- autobuilt 827293a

* Thu Jun 11 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:1.0.1-12.dev.git161ef5a
- Update man pages

* Wed Jun 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-10.dev.git161ef5a
- autobuilt 161ef5a

* Thu Jun 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-9.dev.gitf9b0d93
- autobuilt f9b0d93

* Fri May 29 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-8.dev.gitc6b488a
- autobuilt c6b488a

* Mon May 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-7.dev.gita2c1d46
- autobuilt a2c1d46

* Mon May 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-6.dev.git8b4b954
- autobuilt 8b4b954

* Sat May 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-5.dev.git3a94432
- autobuilt 3a94432

* Thu May 21 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-4.dev.git96353f2
- autobuilt 96353f2

* Wed May 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-3.dev.git91a88de
- autobuilt 91a88de

* Mon May 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:1.0.1-2.dev.gitdcaee94
- bump to 1.0.1
- autobuilt dcaee94

* Mon May 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-12.dev.gita214a30
- autobuilt a214a30

* Fri May 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-11.dev.git0d9939d
- autobuilt 0d9939d

* Thu May 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-10.dev.gitfbf0612
- autobuilt fbf0612

* Thu May 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-9.dev.git2af1726
- autobuilt 2af1726

* Tue May 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-8.dev.git4ca9b13
- autobuilt 4ca9b13

* Mon May 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-7.dev.git71a14d7
- autobuilt 71a14d7

* Mon May 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-6.dev.git8936e76
- autobuilt 8936e76

* Mon May 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-5.dev.gita6ab229
- autobuilt a6ab229

* Sun May 10 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.2.0-4.dev.git42f68c1
- bump release tag for smooth upgrade path from f32

* Sat May 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-0.8.dev.git42f68c1
- autobuilt 42f68c1

* Tue May 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-0.7.dev.git1ddb736
- autobuilt 1ddb736

* Mon May 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-0.6.dev.gite7a7f01
- autobuilt e7a7f01

* Fri May 1 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.2.0-0.5.dev.git2415f3f
- Fix containers-registries.conf.5 man page to match upstream

* Wed Apr 29 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.2.0-0.4.dev.git2415f3f
- Fix registries.conf file to correctly pass the unqualified-search-registries

* Sat Apr 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-0.3.dev.gitb230a50
- autobuilt b230a50

- Update registries.conf to use version 2 definitions
- Update containers.conf to include latest changes
- Update seccomp.json to allow a few more syscalls for contaners within containers.
- Update storage.conf to match upstream

* Thu Apr 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.2.0-0.1.dev.git2415f3f
- bump to 0.2.0
- autobuilt 2415f3f

* Thu Apr 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-8.0.dev.git2d91b93
- autobuilt 2d91b93

* Wed Apr 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-7.0.dev.git101901a
- autobuilt 101901a

* Wed Apr 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-6.0.dev.git9d21b48
- autobuilt 9d21b48

* Wed Apr 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-5.0.dev.git9d63c7c
- autobuilt 9d63c7c

* Tue Apr 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-4.0.dev.git6ac3dce
- autobuilt 6ac3dce

* Tue Apr 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-3.0.dev.git71a8ff0
- autobuilt 71a8ff0

* Tue Apr 7 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.1.42-2
- Update man pages to match upstream

* Tue Apr 7 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.1.42-1
- Update containers.conf and containers.conf.5.md to upstream

* Mon Apr 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.16.dev.git8fa3326
- autobuilt 8fa3326

* Tue Mar 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.15.dev.git5d512e2
- autobuilt 5d512e2

* Tue Mar 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.14.dev.git3e9d8ae
- autobuilt 3e9d8ae

* Tue Mar 31 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.13.dev.gitbd20786
- autobuilt bd20786

* Mon Mar 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.12.dev.git6db5626
- autobuilt 6db5626

* Mon Mar 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.11.dev.giteb199dc
- autobuilt eb199dc

* Mon Mar 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.10.dev.git018a010
- autobuilt 018a010

* Sat Mar 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.9.dev.gita6f5ef1
- autobuilt a6f5ef1

* Wed Mar 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.8.dev.git501452a
- autobuilt 501452a

* Fri Mar 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.7.dev.gite31d5a0
- autobuilt e31d5a0

* Fri Mar 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.6.dev.git7fee7d5
- autobuilt 7fee7d5

* Thu Mar 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.5.dev.git12865fd
- autobuilt 12865fd

* Thu Mar 19 2020 Jonathan Lebon <jonathan@jlebon.com> - 1:0.1.42-0.4.dev.git7a0a8c2
- Drop /srv/containers and /var/srv/container from file list

* Thu Mar 19 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.3.dev.git7170702
- autobuilt 7170702

* Wed Mar 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.2.dev.gitb541fef
- autobuilt b541fef

* Mon Mar 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.42-0.1.dev.git7a0a8c2
- bump to 0.1.42
- autobuilt 7a0a8c2

* Mon Feb 17 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.1.41-27.dev.git7cbb8ad
- Allow s390x to use clone syscall in seccomp.json
- Add support for containers.conf and man page

* Thu Feb 6 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.1.41-26.dev.git7cbb8ad
- Remove quay.io from list of search registries, removes risk of squatters.
- Update man pages to match upstream

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.1.41-25.dev.git7cbb8ad
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-24.dev.git7cbb8ad
- autobuilt 7cbb8ad

* Wed Jan 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-23.dev.git4489ddd
- autobuilt 4489ddd

* Tue Jan 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-22.dev.git763e488
- autobuilt 763e488

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-21.dev.gite955849
- autobuilt e955849

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-20.dev.git8652b65
- autobuilt 8652b65

* Mon Dec 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-19.dev.gitc3e6b4f
- autobuilt c3e6b4f

* Mon Dec 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-18.dev.git5291aac
- autobuilt 5291aac

* Mon Dec 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-17.dev.git407f2e9
- autobuilt 407f2e9

* Sat Dec 07 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-16.dev.gite8d49d6
- autobuilt e8d49d6

* Wed Dec 04 2019 Dusty Mabe <dusty@dustymabe.com> - 1:0.1.41-15.dev.git3ed6e83
- mounts: update symlink name from rhel7.repo to redhat.repo

* Mon Dec 2 2019 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.1.41-14.dev.git3ed6e83
- Change default order of registries.conf to push docker.io to the back.
- Allo clock_adjtime by default in seccomp.json since it can be used in read/only mode

* Mon Dec 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-12.dev.git9c402f3
- autobuilt 9c402f3

* Mon Dec 2 2019 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.1.41-11.dev.git3ed6e83
- Update man pages to reflect upstream sources
- Also update storage.conf to remove skip_mount_home which is no longer
supported.

* Sat Nov 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-10.dev.git3ed6e83
- autobuilt 3ed6e83

* Thu Nov 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-9.dev.git73248bd
- autobuilt 73248bd

* Wed Nov 27 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-8.dev.git2bfa895
- autobuilt 2bfa895

* Tue Nov 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-7.dev.gitce6ec77
- autobuilt ce6ec77

* Tue Nov 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-6.dev.git912b7e1
- autobuilt 912b7e1

* Mon Nov 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-5.dev.git34ab4c4
- autobuilt 34ab4c4

* Fri Nov 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-4.dev.git39540db
- autobuilt 39540db

* Thu Nov 21 2019 Dan Walsh <dwalsh@fedoraproject.org> - - 1:0.1.41-2.dev.git24f4f82
- Update to use new storage.conf configuration files.

* Tue Nov 19 2019 Dan Walsh <dwalsh@fedoraproject.org> - - 1:0.1.41-2.dev.git24f4f82
- add clock_adjtime as valid syscall when CAP_SYS_TIME added

* Fri Nov 8 2019 Dan Walsh (Bot) <dwalsh+bot@fedoraproject.org> - - 1:0.1.41-1.dev.git24f4f82
- Change default search order on registries.conf.
- Quay.io should be last to make sure no one is squating on repos that are
  provided by upstream packages.

* Sat Nov 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-0.9.dev.git24f4f82
- autobuilt 24f4f82

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-0.8.dev.git332bb45
- autobuilt 332bb45

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-0.7.dev.git307d9c2
- autobuilt 307d9c2

* Fri Nov 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-0.6.dev.git1094c7d
- autobuilt 1094c7d

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-0.5.dev.git75b7d1e
- autobuilt 75b7d1e

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-0.4.dev.git10d0ebb
- autobuilt 10d0ebb

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-0.3.dev.git02432cf
- autobuilt 02432cf

* Wed Oct 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-0.2.dev.git153520e
- autobuilt 153520e

* Mon Oct 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.41-0.1.dev.gita263b35
- bump to 0.1.41
- autobuilt a263b35

* Mon Oct 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-0.17.dev.git8057da7
- autobuilt 8057da7

* Tue Oct 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-0.16.dev.git4b6a5da
- autobuilt 4b6a5da

* Wed Oct 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-0.15.dev.git5f9a6ea
- autobuilt 5f9a6ea

* Tue Oct 15 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-0.14.dev.git5b0a789
- autobuilt 5b0a789

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-0.13.dev.gitf72e39f
- autobuilt f72e39f

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-0.12.dev.git881edbf
- autobuilt 881edbf

* Mon Sep 30 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1:0.1.40-0.11.dev.gitfa6e580
- autobuilt fa6e580

* Thu Sep 19 2019 Michael Nguyen <mnguyen@redhat.com> - 1:0.1.40-0.10.dev.git7eb5f39
- Add /srv/containers and /var/srv/container directories to containers-common

* Wed Sep 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-0.9.dev.git7eb5f39
- autobuilt 7eb5f39

* Sat Sep 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-0.8.dev.git5ae6b16
- autobuilt 5ae6b16

* Tue Sep 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-0.7.dev.git18f0e1e
- autobuilt 18f0e1e

* Fri Aug 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-0.6.dev.git9019e27
- autobuilt 9019e27

* Wed Aug 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-0.5.dev.gitc4b0c7c
- autobuilt c4b0c7c

* Mon Aug 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-0.4.dev.git1e2d6f6
- autobuilt 1e2d6f6

* Thu Aug 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-0.3.dev.git481bb94
- autobuilt 481bb94

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-0.2.dev.gitee9e9df
- autobuilt ee9e9df

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.40-0.1.dev.git44bc4a9
- bump to 0.1.40
- autobuilt 44bc4a9

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.39-0.2.dev.gitc040b28
- autobuilt c040b28

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.39-0.1.dev.git202c1ea
- bump to 0.1.39
- autobuilt 202c1ea

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-9.dev.gitbf8089c
- autobuilt bf8089c

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-8.dev.git65b3aa9
- autobuilt 65b3aa9

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-7.dev.git19025f5
- autobuilt 19025f5

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-6.dev.git2ad9ae5
- autobuilt 2ad9ae5

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-5.dev.git8a9641c
- autobuilt 8a9641c

* Thu Jul 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-4.dev.gitb58088a
- autobuilt b58088a

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.38-3.dev.git5f45112
- autobuilt 5f45112

* Tue Jul 9 2019 Dan Walsh (Bot) <dwalsh+bot@fedoraproject.org> - 1:0.1.38-2.dev
- Update containers-registries.conf.md man page for mirroring support
- Update regsitries.conf file to match containers/image

* Mon Jun 24 2019 Dan Walsh (Bot) <dwalsh+bot@fedoraproject.org> - 1:0.1.38-1.dev
- Bump up to 1:0.1.38

* Wed May 15 2019 Dan Walsh (Bot) <dwalsh+bot@fedoraproject.org> - 1:0.1.36-19.dev.git0fa335c
- Add metacopy=on flag to storage.conf

* Sun May 5 2019 Dan Walsh (Bot) <dwalsh+bot@fedoraproject.org> - 1:0.1.36-18.dev.git0fa335c
- Update man pages and add missing man pages to containers-common.

* Fri Apr 26 2019 Lokesh Manvdekar <lsm5@fedoraproject.org> - 1:0.1.36-17.dev.git0fa335c
- Fixes @openshift/machine-config-operator#669
- install /etc/containers/oci/hooks.d

* Wed Apr 24 2019 Dan Walsh (Bot) <dwalsh+bot@fedoraproject.org> - 1:0.1.36-16.dev.git0fa335c
- Fix location of sigstore atomic->containers

* Wed Apr 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-15.dev.git0fa335c
- autobuilt 0fa335c

* Thu Apr 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-14.dev.git2af7114
- autobuilt 2af7114

* Wed Apr 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-13.dev.gite255ccc
- autobuilt e255ccc

* Sat Apr 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-12.dev.git18ee5f8
- autobuilt 18ee5f8

* Fri Apr 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-11.dev.git81c5e94
- autobuilt 81c5e94

* Thu Apr 11 2019 Dan Walsh <dwalsh@fedoraproject.org> - 1:0.1.36-10.dev.gitc73bcba
- add containers-storage.conf man page

* Tue Apr 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-9.dev.gitc73bcba
- autobuilt c73bcba

* Thu Mar 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.1.36-8.dev.git854f766
- autobuilt 854f766

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
