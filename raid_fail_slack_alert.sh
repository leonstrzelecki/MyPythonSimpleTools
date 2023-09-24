#!/bin/bash
# Here's a script which i added to cronjobs on my server to monitor mdadm raid5 state. If there's any failure, it sends an alert to the slack channel
# req.: U need to create and configure an app in slack api 
# ref.: https://api.slack.com/authentication
# ref.: https://api.slack.com/messaging/sending

# Insert your api authentication token and slack channel's id
channel_id=""
auth_token=""

# Define the search string -> "U" * raid members
# example for 5 disks in raid
search_string="UUUUU"

# Check if the search string is in the file
if grep -q "$search_string" "/proc/mdstat"; then
    touch /tmp/raid_check_time_stamp
else
    echo $channel_id; curl -X POST -H "Authorization: Bearer $auth_token" -H 'Content-type: application/json; charset=utf-8' --data '{"channel":"'$channel_id'","text":"ALERT!!! ONE OF DISKS IN RAID IS DOWN"}' https://slack.com/api/chat.postMessage
fi
