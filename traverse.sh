#!/bin/bash

for fname in `ls configs`
do
  if [[ $fname == * ]]
  then
    base="node amex-offer-monitor.js "
    configoption="--config configs/"
    configfile=$fname
    command=$base$configoption$configfile

    eval "$command"

    sleep 5m
  fi
done
