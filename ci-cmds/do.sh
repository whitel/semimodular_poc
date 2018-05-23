#! /bin/sh -e

img=langdon/addon-modular-boltron

if [ "x$1" != "x" ]; then
  img="$1"
fi

dock="sudo docker"
imgid="$($dock images -q $img | head -1)"

if [ ! -d "$img/$imgid" ]; then
  imgid="<none>"
else
  echo "OLD IMG: $img:$imgid"
fi

while true; do
  sudo docker pull $img

  nimgid="$($dock images -q $img | head -1)"
  echo "IMG: $img:$nimgid"
  if [ "x$nimgid" != "x$imgid" ]; then
    ./image-info.sh $img
    ./test-info.sh  $img

    pass="$(./report.py $img/$nimgid | fgrep Pass | head -1 | awk '{ print $2 }')"
    if [ "x$pass" != "x0" ]; then
      ln -sf "$nimgid" "$img/tested"
      sudo docker tag $nimgid $img:tested
      echo "Pushing tested tag."
      sudo docker push $img:tested || true
    fi
  fi
  imgid="$nimgid"
  ln -sf "$imgid" "$img/latest"

  echo "Sleeping ~1 hour, from: $(date --iso=minutes | tr T ' ')"
  sleep 66m
done
