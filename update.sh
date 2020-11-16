clone() {
    git clone https://github.com/containers/$1.git 2>/dev/null || true
    pushd $1
    git config pull.rebase false
    git pull origin master
    popd
}
#!/bin/sh
clone storage
sed -e 's/^driver.*=.*/driver = "overlay"/' -e 's/^mountopt.*=.*/mountopt = "nodev,metacopy=on"/' storage/storage.conf >  storage.conf
cp storage/docs/containers-storage.conf.5.md .

clone image
cp image/docs/*md .
sed -e 's/^#.*unqualified-search-registries.*=.*/unqualified-search-registries = ["registry.fedoraproject.org", "registry.access.redhat.com", "registry.centos.org", "docker.io"]/g' image/registries.conf >  registries.conf
rm signature-protocols.md

clone common
cp common/docs/*md .
cp common/pkg/config/containers.conf .
sed -e '/\"kill\",/i \
				"keyctl",' \
-e '/\"socketcall\",/i \
				"socket",' common/pkg/seccomp/seccomp.json > seccomp.json
sed -e 's/^#.*unqualified-search-registries.*=.*/unqualified-search-registries = ["registry.fedoraproject.org", "registry.access.redhat.com", "registry.centos.org", "docker.io"]/g' image/registries.conf >  registries.conf

clone podman
cp podman/docs/source/markdown/containers-mounts.conf.5.md .
