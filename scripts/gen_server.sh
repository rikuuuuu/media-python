#!/usr/bin/env bash

APP_ROOT=$(dirname $0)/..

rm -f ${APP_ROOT}/pb/*
mkdir -p ${APP_ROOT}/pb

protoc --proto_path=${APP_ROOT}/proto/. \
       --twirpy_out=${APP_ROOT}/pb/ \
       --python_out=${APP_ROOT}/pb/ \
       ${APP_ROOT}/proto/*.proto

# rm -f ${APP_ROOT}/proto/third_party/lafool/go/*
# mkdir -p ${APP_ROOT}/proto/third_party/lafool/go

# protoc --proto_path=${APP_ROOT}/proto/third_party/lafool/. \
#        --twirp_out=${APP_ROOT}/proto/third_party/lafool/go/ \
#        --go_out=${APP_ROOT}/proto/third_party/lafool/go/ \
#        ${APP_ROOT}/proto/third_party/lafool/*.proto

# cp ${APP_ROOT}/di/wire_gen.default.go ${APP_ROOT}/di/wire_gen.go

# go generate ${APP_ROOT}/di/wire_gen.go