#!/bin/bash
pattern=${1:-*}

for fname in `ls configs`
do
  if [[ $fname == $pattern ]]
  then
    base="node amex-offer-monitor.js "
    configoption="--config configs/"
    configfile=$fname
    command=$base$configoption$configfile

    eval "$command"

    sleep 5m
  fi
done
