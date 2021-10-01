#!/bin/bash -e

# Log program and kernel versions
echo "Important package versions:"
(
    uname -r
    rpm -qa | egrep 'skopeo|podman|conmon|crun|runc|iptable|slirp|systemd' | sort
) | sed -e 's/^/  /'

# Log environment; or at least the useful bits
echo "Environment:"
env | grep -v LS_COLORS= | sort | sed -e 's/^/  /'

SKOPEO_BINARY=/usr/bin/skopeo bats /usr/share/skopeo/test/system
