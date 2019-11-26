#!/usr/bin/env bash

BUCKET_NAME=''

sam package --template-file template.yaml --output-template-file output.yaml --s3-bucket ${BUCKET_NAME}
