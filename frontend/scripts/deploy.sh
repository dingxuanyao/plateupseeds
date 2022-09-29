#!/usr/bin/env bash
#
# Deploying application to https://plateupseeds.com/

export AWS_PROFILE=tony_personal

src_path="/Users/tonyyao/workspace/plateupseeds/frontend/src"

aws s3 cp "${src_path}"/main.js s3://album-test-939326176859/
aws s3 cp "${src_path}"/style.css s3://album-test-939326176859/
aws s3 cp "${src_path}"/index.html s3://album-test-939326176859/
aws s3 cp "${src_path}"/favicon.png s3://album-test-939326176859/
aws s3 cp "${src_path}"/cup-hot.svg s3://album-test-939326176859/

aws cloudfront create-invalidation \
  --distribution-id E3757929QYYG7Y\
  --paths /index.html /main.js /style.css /favicon.png /cup-hot.svg /
