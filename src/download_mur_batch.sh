#!/bin/bash

DATES=(20231016 20231017 20231018 20231019 20231020 20231021 20231022)

BASE_URL="https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-protected/MUR-JPL-L4-GLOB-v4.1"

OUT_DIR="data/raw/mur_sst_clean"
mkdir -p $OUT_DIR

for DATE in "${DATES[@]}"; do
  FILE="${DATE}090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"
  echo "⬇️ Downloading $FILE"
  wget --content-disposition --continue \
       --directory-prefix=$OUT_DIR \
       "$BASE_URL/$FILE"
done
