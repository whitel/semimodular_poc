#! /bin/sh -e

dock="sudo docker"
SELINUX=":z"

if [ "x$1" = "x" ]; then
  exit 1
fi

img="$1"
if [ "x$2" = "x" ]; then
  imgid="$($dock images -q $img | head -1)"
else
  imgid="$2"
fi

echo "Looking at image $img with id $imgid"

if [ ! -d "$img/$imgid" ]; then
  mkdir -p "$img/$imgid"
fi

dockrun="$dock run --rm -it -v $(pwd):/mnt$SELINUX $imgid"

$dockrun /mnt/i-image-info-beg.sh $img/$imgid

