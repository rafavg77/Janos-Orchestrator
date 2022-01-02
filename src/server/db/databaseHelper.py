import os
import logging
import sqlite3
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def selectHistory():
    conn = sqlite3.connect('/home/pi/Production/Janos-Orchestrator/src/server/db/hosts.db')
    cursor = conn.execute("SELECT * from HOSTS")
    print(cursor.fetchall())
    conn.close()

def intert2History(ip,mac,hostname):
    conn = sqlite3.connect('/home/pi/Production/Janos-Orchestrator/src/server/db/hosts.db')
    first_time = datetime.datetime.now()
    try:
        conn.execute("INSERT INTO HOSTS (IP,MAC,HOSTNAME,DATE) VALUES (?, ?, ?,?)",('{}'.format(ip), '{}'.format(mac), '{}'.format(hostname),first_time))
        conn.commit()
    except:  
        conn.rollback()  
    finally:
        conn.close()

def getLastDetected(mac):
    later_time = datetime.datetime.now()

    conn = sqlite3.connect('/home/pi/Production/Janos-Orchestrator/src/server/db/hosts.db')

    cursor = conn.execute("SELECT * FROM HOSTS WHERE MAC = '{}' ORDER BY DATE DESC LIMIT 1;".format(mac))
    #print(cursor.fetchall())
    records = cursor.fetchall()
    
    first_time = ''
    minutes = ''
    status = ''
    isNew = ''
    if not records:
        logging.info("Records " + str(len(records)))
        isNew = True
    else:
        logging.info("Records " + str(len(records)))

        for row in records:
            first_time = datetime.datetime.strptime(row[4],'%Y-%m-%d %H:%M:%S.%f')
            logging.info("Ultima vez visto: " + str(row[4]))
            logging.info("Ahora:            " + str(later_time))
            difference = later_time - first_time
            logging.info("{}".format(difference))
            minutes = str(divmod(difference.seconds,3600)[1]/60)
            hours  = str(divmod(difference.seconds,3600)[0])
            logging.info("{}".format(hours))
            if int(float(hours)) > 1:
                logging.info("Mayor de 1 hora")
                status = True
            elif int(float(hours)) < 1:
                logging.info("Menor de 1 hora")
                status = False
    conn.close()

    return first_time, minutes, status, isNew
