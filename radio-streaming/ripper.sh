#!/bin/bash

clear

# folder to store in, no trailing slash
SAVETO=~/radio_files

# the default format of the recorded streams
FORMAT=mp3

# set recorder
RECORDER=streamripper

declare -A station

station[http://uk2.internet-radio.com:8332/live]=mba_101_1
station[http://cast3.servcast.net:8044/;stream.mp3?1580996196649]=pm_91_9
station[https://edge.mixlr.com/channel/xbxnh]=bk_100_5
station[http://66.55.145.43:7344/;?1581951649385]=bd_95_5
station[http://162.244.80.52:8732/stream/1/]=aka_89_9
station[http://www.radiosimba.ug:8000/stream]=sim_97_3
station[http://41.202.239.38:88/broadwave.mp3?src=3&rate=1&ref='']=cbs89_2
station[http://41.202.239.38:88/broadwave.mp3]=cbs88_8
station[http://144.217.203.226:8354/stream/1/]=bt_96_3
station[https://www.radiosapientia.com/live]=sap_94_4
station[http://66.55.145.43:7404/;?1582179456214]=pl_107_9
station[http://uk6.internet-radio.com:8358/stream]=st_107_0
station[http://66.55.145.43:7383/stream]=dig_106_5
station[http://66.55.145.43:7757/stream]=me_90_8
station[http://162.210.196.217:8112/stream.mp3]=re_97_7


DATETIME=`date -d '+3 hour' '+%F_T%H.%M.%S'`

# create the save directory if it doesn't exist
if [ ! -d $SAVETO ]; then
   mkdir $SAVETO
fi

# write log file
echo "*** Start $DATETIME ***" >> $SAVETO/log.txt

# execute the recording command
for st in ${!station[@]}; do
    FILENAME=${station[$st]}-$DATETIME.$FORMAT
    RECCMD="streamripper $st -u Mozilla/5.0 -d $SAVETO/ -a $FILENAME -s -A -l 300"
    $RECCMD
# schedule the recording command with time format hh:mm YYYY-MM-DD
    #echo $RECCMD | at $STARTTIME $DATE
done

# write log file
echo $RECCMD >> $SAVETO/log.txt
