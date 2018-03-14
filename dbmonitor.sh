#! /usr/bin/env bash
set -euo pipefail

# how often to collect data
interval=10

# where to log results
log=db_rw.json

login="-uroot -ptest123"
db="-Dmeta"

per_second(){
    echo "($1 - $2) / $interval" | bc
}

# start an array in the log
echo -n "[" > $log

trap on_term INT

# finish it on exit
on_term(){

    # remove trailing comma
    sed -i '$ s/.$//' $log

    # close off array
    echo -n "]" >> $log
    echo
    echo bye
    exit 0
}

# get current values
row_inserts=$(mysqladmin extended-status $login | grep rows_inserted | awk {'print $4'})
reads=$(mysqladmin extended-status $login | grep rows_read | awk {'print $4'})

while true; do
      echo
      echo -n "Collecting data for $interval seconds"
      for i in $(seq $interval); do
          sleep 1
          echo -n "."
      done

      # counting reads and inserts does not alter metrics
      new_row_inserts=$(mysqladmin extended-status $login | grep rows_inserted | awk {'print $4'})
      new_reads=$(mysqladmin extended-status $login | grep rows_read | awk {'print $4'})

      rps="$(per_second $new_reads $reads)"
      ips="$(per_second $new_row_inserts $row_inserts)"
      human_date=$(date +%H:%M:%S)
      machine_date=$(date +%s)

      # tell the humans
      echo "[ $human_date ]"
      echo "    inserts per second: $ips"
      echo "      reads per second: $rps"

      echo -n "[$(date +%s), $rps, $ips]," >> $log

      row_inserts=$new_row_inserts
      reads=$new_reads
done

