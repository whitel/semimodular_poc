#! /bin/sh -e

# FIXME: Check rpmdb now?

if [ ! -f $2 ]; then
  /mnt/i-list-rpmdb-sizes.py version > $2
fi

printf "%38s => " $1 >> $2
dnf history > /tmp/ohist
echo "Testing: dnf module install -y $1"
if dnf module install -y "$1"; then
  if dnf history > /tmp/nhist; then
    if [ "x$(cat /tmp/ohist)" != "x$(cat /tmp/nhist)" ]; then
      echo "   pass" >> $2
    else
      echo "** FAIL: Did nothing fast **" >> $2
    fi
  else
    echo '** FAIL: SYS error **' >> $2
  fi
else
  echo '** FAIL: DNF error **' >> $2
fi

/mnt/i-list-rpmdb-sizes.py version >> $2
