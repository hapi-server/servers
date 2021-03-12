#!/bin/bash

echo "begin makeGiantCatalog"
SECONDS=0 # Magic variable
cd  /home/jbf/ct/git/servers/index
git pull 
#java -cp /home/jbf/bin/autoplot.jar -Djava.awt.headless=true org.autoplot.AutoplotUI --script=makeGiantCatalog.jy
git commit -m "automatic update" *
git push
echo "finished in seconds: " $SECONDS
