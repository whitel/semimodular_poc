#!/bin/bash

for m in `ls /local-modules`;
do
    echo Making $m repo available;
    NEW_REPO=$(cat <<EOF
[local-$m]
name=Local repo. for $m
baseurl=file:///local-modules/$m/results
type=rpm-md
skip_if_unavailable=True
gpgcheck=0
repo_gpgcheck=0
enabled=1
enabled_metadata=1

EOF
)
    echo "$NEW_REPO" >> /etc/yum.repos.d/local.repo
done

#cat /etc/yum.repos.d/local.repo
/bin/bash



