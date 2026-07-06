#!/bin/bash

DATE=$(date +%Y-%M-%d_%H-%M)
OUTPUT=~/cloud_journey/projects/health_report_$DATE.txt

echo '===========================' > $OUTPUT
echo 'SYSTEM HEALTH REPORT' >> $OUTPUT
echo 'Generated:'  $DATE  >> $OUTPUT
echo '===========================' >> $OUTPUT

echo '' >> $OUTPUT
echo '--- UPTIME ---' >> $OUTPUT
uptime >> $OUTPUT
echo '' >> $OUTPUT 

echo '--- MEMORY ---' >> $OUTPUT
free -h >>$OUTPUT
echo '' >>$OUTPUT

echo '--- DISK USAGE ---' >>$OUTPUT
df -h >> $OUTPUT
echo '' >> $OUTPUT

echo '--- TOP 5 PROCESSES BY CPU ---' >> $OUTPUT
ps aux --sort=-%cpu | head -6 >> $OUTPUT
echo '' >> $OUTPUT

echo '--- NETWORK INTERFACES ---' >> $OUTPUT
ip addr show >> $OUTPUT
echo '' >> $OUTPUT

echo '--- LAST 10 LOG ENTRIES ---' >> $OUTPUT
journalctl --no-pager -n 10 >> $OUTPUT 2>/dev/null || tail -10 /var/log/syslog >> $OUTPUT
echo '' >> $OUTPUT

echo '--- SERVICE STATUS ---' >> $OUTPUT
for SERVICE in ssh cron; do 
    STATUS=$(systemctl is-active $SERVICE 2>/dev/null || echo 'unknown')
    echo "$SERVICE: $STATUS" >> $OUTPUT
done
echo '' >> $OUTPUT

echo '' >> $OUTPUT
echo 'Report saved to:' $OUTPUT
cat $OUTPUT 
