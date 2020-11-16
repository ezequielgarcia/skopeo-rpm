clone() {
    git clone https://github.com/containers/$1.git 2>/dev/null || true
    pushd $1
    git config pull.rebase false
    git pull origin master
    git pull origin main
    popd
}
#!/bin/sh
# checkout containers/storage and get man pages and storage.conf
clone storage
sed -e 's/^driver.*=.*/driver = "overlay"/' -e 's/^mountopt.*=.*/mountopt = "nodev,metacopy=on"/' storage/storage.conf >  storage.conf
cp storage/docs/containers-storage.conf.5.md .

# checkout containers/image and get man pages and registries.conf
clone image
cp image/docs/*md .
sed -e 's/^#.*unqualified-search-registries.*=.*/unqualified-search-registries = ["registry.fedoraproject.org", "registry.access.redhat.com", "registry.centos.org", "docker.io"]/g' image/registries.conf >  registries.conf
rm signature-protocols.md

# checkout containers/common and get man pages, seccomp.json and containers.conf
clone common
cp common/docs/*md .
cp common/pkg/config/containers.conf .
sed -e '/\"kill\",/i \
				"keyctl",' \
-e '/\"socketcall\",/i \
				"socket",' common/pkg/seccomp/seccomp.json > seccomp.json
sed -e 's/^#.*unqualified-search-registries.*=.*/unqualified-search-registries = ["registry.fedoraproject.org", "registry.access.redhat.com", "registry.centos.org", "docker.io"]/g' image/registries.conf >  registries.conf

# checkout containers/podman and get mounts.conf man page
clone podman
cp podman/docs/source/markdown/containers-mounts.conf.5.md .

# checkout containers/shortnames and get shortnames.conf man page
clone shortnames
cp shortnames/shortnames.conf .
