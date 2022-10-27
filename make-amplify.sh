#!/bin/bash -e

export OUTPUT_DIR="./public"
STATIC_DIR="./static"

mkdir ${OUTPUT_DIR}
python3 compile.py

cp -r ${STATIC_DIR}/. ${OUTPUT_DIR}

find ${OUTPUT_DIR} -type f | xargs chmod 644
find ${OUTPUT_DIR} -type d | xargs chmod 755

ls -lR ${OUTPUT_DIR}
