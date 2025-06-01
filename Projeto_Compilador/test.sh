#!/usr/bin/bash

for element in programas_teste/exemplo*.pas
do
  echo $element
  cat $element | python3 src/compiler_program.py $element
done