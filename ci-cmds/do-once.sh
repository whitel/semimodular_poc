#! /bin/sh -e

img=langdon/addon-modular-boltron

if [ "x$1" != "x" ]; then
  img="$1"
fi

dock="sudo docker"
imgid="$($dock images -q $img | head -1)"

if [ ! -d "$img/$imgid" ]; then
  imgid="<none>"
  if [ -h "$img/latest" ]; then
    imgid="$(readlink $img/latest)"
    echo "Last IMG: $img:$imgid"
  fi
else
  echo "OLD IMG: $img:$imgid"
fi

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
      # sudo docker tag $nimgid $img:tested-$(date --iso)-$pass
      echo "Pushing tested tags."
      sudo docker push $img || true
    fi
    rm -f "$img/prev"
    mv "$img/latest" "$img/prev" || true
    ln -sf "$nimgid" "$img/tested"
  fi
  imgid="$nimgid"
  ln -sf "$imgid" "$img/latest"
