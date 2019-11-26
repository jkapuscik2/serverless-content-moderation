#!/usr/bin/env bash

STACK_NAME=''

sam deploy --template-file output.yaml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM