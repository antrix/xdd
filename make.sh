#!/bin/bash -e

OUTPUT_DIR="./public"
STATIC_DIR="./static"


rm -rf ${OUTPUT_DIR}/*
python compile.py

cp -r ${STATIC_DIR} ${OUTPUT_DIR}

find ${OUTPUT_DIR} -type f | xargs chmod 644
find ${OUTPUT_DIR} -type d | xargs chmod 755
