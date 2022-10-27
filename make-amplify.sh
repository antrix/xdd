#!/bin/bash -e

PUBLIC_DIR="./public"
STATIC_DIR="./static"

mkdir ${PUBLIC_DIR}
python3 compile.py

cp -r ${STATIC_DIR}/. ${PUBLIC_DIR}

find ${PUBLIC_DIR} -type f | xargs chmod 644
find ${PUBLIC_DIR} -type d | xargs chmod 755

ls -lR ${PUBLIC_DIR}
