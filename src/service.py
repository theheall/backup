import os, logging, schedule, time
from requests import get, put
from random import choices
from yaml import load, Loader
from sys import stdout
from shutil import make_archive
from requests.exceptions import RequestException

config = load(open('/etc/backup/config.yml', 'r').read(), Loader=Loader)
logging.basicConfig(level=logging.INFO, filename=config['logfile'], datefmt='%Y-%m-%d %H:%M:%S', format='[%(asctime)s] %(levelname)s: %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(stdout))

def backup():
    logging.info('Start backup tasks')
    folder = [o for o in os.listdir(config['folders']['data']) if os.path.isdir(os.path.join(config['folders']['data'],o))]
    logging.info('Found ' + str(len(folder)) + ' servers\' folder: ' + ', '.join(folder))
    response = get(config['panel']['url'] + '/api/application/servers', headers={'authorization': 'Bearer ' + config['panel']['token']})
    if (response.status_code == 200):
        servers = {server["attributes"]["uuid"]: server["attributes"]["name"] for server in response.json()['data']}
        logging.info('The connection to the pterodactyl panel was successful')
    else:
        logging.critical(f'Unable to retrieve servers\' name from Pterodactyl Panel. Status code: {response.status_code}')

    for uuid in folder:
        start = time.time()
        print(f'\nServer {servers[uuid]} - {uuid}:')
        random_archive = config['folders']['temp'] + ''.join(choices("012345689ABCEF", k=6))
        logging.info(f'  Zipping the {servers[uuid]} server\'s content to {random_archive}.zip...')
        zip_start = time.time()
        make_archive(random_archive, 'zip', config['folders']['data'] + uuid)
        logging.info(f'  Zipped in {round(time.time() - zip_start, 2)}s')
        logging.info(f'  Uploading {random_archive}.zip to cloud...')
        try:
            response = put(config['cloud']['endpoint'] + servers[uuid] + '.zip', data=open(random_archive + '.zip','rb').read(), auth=(config['cloud']['user'], config['cloud']['pass']))
            if(response.status_code in [201, 204]):
                logging.info(f'  Uploaded {round(os.stat(random_archive + ".zip").st_size/2**20, 2)} MB in {round(response.elapsed.total_seconds(), 2)}s ({round((os.stat(random_archive + ".zip").st_size/2**20)/response.elapsed.total_seconds(), 2)} MB/s)')
                os.remove(random_archive + '.zip')
                logging.info(f'  {random_archive}.zip removed from temp folder')
        except RequestException as e:
            logging.warning(f'  Upload failed ({e}). You can get the backup in {random_archive}')
        logging.info(f'  -> Backup completed SUCCESSFUL in {round(time.time() - start, 2)}s')

schedule.every(1).hours.do(backup).run()

while True:
    schedule.run_pending()
    time.sleep(60)
