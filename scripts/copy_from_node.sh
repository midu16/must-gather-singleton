#!/bin/bash -x

printf "Type $1 Node $2 file $3"

FILENAME=`basename $3`

if [  "${1}" = "ocp" ]
then
  oc debug node/$2 -- cat $3 > /apps/must-gather/${FILENAME}
else
  kubectl debug node/$2 --image=fedora -it -- cat $3 > /apps/must-gather/${FILENAME}
fi


