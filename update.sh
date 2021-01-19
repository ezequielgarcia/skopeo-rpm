#!/bin/bash
spectool -f -g skopeo.spec
sed -i -e 's/^driver.*=.*/driver = "overlay"/' -e 's/^mountopt.*=.*/mountopt = "nodev,metacopy=on"/' storage.conf
[ `grep "keyctl" seccomp.json | wc -l` == 0 ] && sed -i '/\"kill\",/i \
				"keyctl",' seccomp.json
sed -i '/\"socketcall\",/i \
				"socket",' seccomp.json
sed -i 's/^#.*unqualified-search-registries.*=.*/unqualified-search-registries = ["registry.fedoraproject.org", "registry.access.redhat.com", "registry.centos.org", "docker.io"]/g' registries.conf
sed -i 's,#.*events_logger.*=.*"journald",events_logger = "file",' containers.conf
if ! grep \"NET_RAW\" containers.conf
then
  sed -i '/^default_capabilities/a \
    "NET_RAW",' containers.conf
fi
