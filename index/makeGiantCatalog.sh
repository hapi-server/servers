cd  /home/jbf/ct/git/servers/index
git pull 
java -cp /home/jbf/bin/autoplot.jar -Djava.awt.headless=true org.autoplot.AutoplotUI --script=makeGiantCatalog.jy
git commit -m "automatic update" *
git push

