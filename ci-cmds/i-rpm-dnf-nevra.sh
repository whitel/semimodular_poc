#! /bin/sh

cmd="rpm -q --qf %{nevra}\n"

for i in dnf libdnf yum dnf-yum microdnf; do

  if $cmd $i > /dev/null; then
    $cmd $i
    # DNF currently has no changelog
    # rpm -q --changelog dnf
  fi
done

