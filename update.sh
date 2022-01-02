cd /home/pi/Production/Janos-Orchestrator/
sudo service bot-orchestator-server stop
sleep 10
sudo service bot-orchestator-telegram stop
sleep 10
git pull
source venv/bin/activate
pip3 install -r requeriments.txt
#export ORCHESTRATOR_DB=/home/pi/Production/Janos-Orchestrator/src/server/db/orchestrator.sqlite
#export SNORT_CONFIG=/home/pi/Production/Janos-Orchestrator/src/config/config.ini
#python3 src/server/db/createDB.py
deactivate
sudo cp systemd/bot-orchestator-server.service /etc/systemd/system/
sudo cp systemd/bot-orchestator-telegram.service /etc/systemd/system/
sudo systemctl daemon-reload

sudo service bot-orchestator-server start
sudo service bot-orchestator-telegram start

sudo service bot-orchestator-server status
sudo service bot-orchestator-telegram status
