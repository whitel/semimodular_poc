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

beg="$(date)"
echo "Testing image $img with id $imgid"

TESTD="$img/$imgid"
ITESTD="/mnt/$TESTD"
if [ ! -d "$TESTD" ]; then
  echo "Need image-info."
  exit 1
fi

dockrun="$dock run --rm -it -v $(pwd):/mnt$SELINUX $imgid"

# Now run install tests for each module:

rm -f $TESTD/test-*
for i in $(cat $TESTD/mods-latest | awk '{ print $1 ":" $2 }'); do
  n="$(echo $i | cut -f1 -d :)"
  s="$(echo $i | cut -f2 -d :)"
  if [ "x$n" != "x$lastn" ]; then
    $dockrun /mnt/i-test-install.sh $n $ITESTD/test-$n
  fi

  $dockrun /mnt/i-test-install.sh $n:$s $ITESTD/test-$n:$s

  # Check profiles...
  for p in $(fgrep $n $TESTD/mods-latest | fgrep " $s " | \
           awk '{ print $4 }' | tr , " "); do
    $dockrun /mnt/i-test-install.sh $n/$p $ITESTD/test-$n
    $dockrun /mnt/i-test-install.sh $n:$s/$p $ITESTD/test-$n:$s
  done

  # Permissions:
  # cat $TESTD/test-$n:s >> $TESTD/test-$n

  lastn="$n"
done

end="$(date)"
echo "FINISHED: Testing image $img with id $imgid"
echo "Started: $beg"
echo "Ended:   $end"
