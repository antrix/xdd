#!/bin/bash -e

PUBLIC_DIR="./public"
STATIC_DIR="./static"

export OUTPUT_DIR=${PUBLIC_DIR}.$(/bin/date +%F.%H-%M-%S)

mkdir ${OUTPUT_DIR}
python compile.py

cp -r ${STATIC_DIR} ${OUTPUT_DIR}

find ${OUTPUT_DIR} -type f | xargs chmod 644
find ${OUTPUT_DIR} -type d | xargs chmod 755

CURRENT_LIVE_DIR="`readlink \"${PUBLIC_DIR}\"`"

ln -s ${OUTPUT_DIR} ${PUBLIC_DIR}.new
mv -T ${PUBLIC_DIR}.new ${PUBLIC_DIR}

rm -rf ${CURRENT_LIVE_DIR}
