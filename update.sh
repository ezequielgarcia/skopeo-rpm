#!/bin/bash
# This script delivers current documentation/configs and assures it has the intended
# settings for a particular branch/release.
# For questions reach to Jindrich Novy <jnovy@redhat.com>

ensure() {
  if grep ^$2[[:blank:]].*= $1 > /dev/null
  then
    sed -i "s;^$2[[:blank:]]=.*;$2 = $3;" $1
  else
    if grep ^\#.*$2[[:blank:]].*= $1 > /dev/null
    then
      sed -i "/^#.*$2[[:blank:]].*=/a \
$2 = $3" $1
    else
      echo "$2 = \"$3\"" >> $1
    fi
  fi
}

#./pyxis.sh
#./update-vendored.sh
spectool -f -g skopeo.spec
ensure storage.conf    driver                        \"overlay\"
ensure storage.conf    mountopt                      \"nodev,metacopy=on\"
ensure containers.conf events_logger                 \"file\"
if pwd | grep rhel-8 > /dev/null
then
ensure registries.conf unqualified-search-registries [\"registry.fedoraproject.org\",\ \"registry.access.redhat.com\",\ \"registry.centos.org\",\ \"docker.io\"]
ensure registries.conf short-name-mode               \"permissive\"
ensure containers.conf infra_image                   \"registry.access.redhat.com/ubi8/pause\"
ensure containers.conf runtime                       \"runc\"
else
ensure registries.conf unqualified-search-registries [\"registry.fedoraproject.org\",\ \"registry.access.redhat.com\",\ \"registry.centos.org\",\ \"quay.io\",\ \"docker.io\"]
ensure registries.conf short-name-mode               \"enforcing\"
ensure containers.conf infra_image                   \"registry.access.redhat.com/ubi9/pause\"
ensure containers.conf runtime                       \"crun\"
fi
[ `grep "keyctl" seccomp.json | wc -l` == 0 ] && sed -i '/\"kill\",/i \
				"keyctl",' seccomp.json
sed -i '/\"socketcall\",/i \
				"socket",' seccomp.json
if ! grep \"NET_RAW\" containers.conf > /dev/null
then
  sed -i '/^default_capabilities/a \
    "NET_RAW",' containers.conf
fi
