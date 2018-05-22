#! /bin/sh -e

# This should go away when DNF works.
/mnt/i-fixup-yumdb-checksums.py

d=/mnt/$1

/mnt/i-list-modules-py3.py > $d/mods
/mnt/i-list-modules-py3.py latest > $d/mods-latest
/mnt/i-list-rpmdb-sizes.py > $d/rpmdb
/mnt/i-rpm-dnf-nevra.sh > $d/dnf
/mnt/i-list-repos-py3.py > $d/repos
/mnt/i-list-multi-mod-rpms-py3.py > $d/mmrpms

