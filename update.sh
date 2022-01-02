cd /home/pi/Production/Janos-Orchestrator/

echo "[+] Stopping bot_telebot-orchestator-servergram service"
sudo service bot-orchestator-server stop
echo "[+] waiting ..."
sleep 10
echo "[+] Stopping bot-orchestator-telegram service"
sudo service bot-orchestator-telegram stop
echo "[+] waiting ..."
sleep 10
echo "[+] Downloading updates from git"
git pull
source venv/bin/activate
echo "[+] Installing requeriments"
pip3 install -r requeriments.txt
#export ORCHESTRATOR_DB=/home/pi/Production/Janos-Orchestrator/src/server/db/orchestrator.sqlite
#export SNORT_CONFIG=/home/pi/Production/Janos-Orchestrator/src/config/config.ini

#export ORCHESTRATOR_DB=/home/tota77/Developer/Janos-Orchestrator/src/server/db/orchestrator.sqlite
#export SNORT_CONFIG=/home/tota77/Developer/Janos-Orchestrator/src/config/config.ini

#python3 src/server/db/createDB.py
deactivate
echo "[+] Updating daemon services"
sudo cp systemd/bot-orchestator-server.service /etc/systemd/system/
sudo cp systemd/bot-orchestator-telegram.service /etc/systemd/system/
echo "[+] Reloading Dameons"
sudo systemctl daemon-reload
echo "[+] Starting bot_telebot-orchestator-servergram_pokedex service"
sudo service bot-orchestator-server start
echo "[+] Starting bot-orchestator-telegram service"
sudo service bot-orchestator-telegram start
echo "[+] Done"