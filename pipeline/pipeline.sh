#!/usr/bin/env bash

arn=$(aws cloudformation describe-stacks \
 --profile honeycomb-dev4 \
 --region ${region} \
 --stack-name p4-${region}-shared-pipeline \
 --query 'Stacks[0].Outputs[?OutputKey==`KmsArn`].OutputValue' \
 --output text)

aws cloudformation deploy \
 --profile honeycomb-dev4 \
 --region ${region} \
 --stack-name happy-lemon-wardrobe-${region}-pipeline \
 --template-file pipeline.yml \
 --parameter-overrides \
  TestAccount=${test} \
  BetaAccount=${beta} \
  ProdAccount=${prod} \
  KmsArn=${arn} \
 --capabilities CAPABILITY_NAMED_IAM