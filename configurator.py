from yaml import load, dump, Loader, Dumper

config = load(open('src/config.yml', 'r').read(), Loader=Loader)

config['panel']['url'] = input("Pterodactyl panel url: ")
config['panel']['token'] = input("Pterodactyl application api key with server read perm: ")

cloud_url = input("Nextcloud url: ")
cloud_user = input("Nextcloud user: ")
cloud_path = input("Nextcloud path to backup folder: ")
config['cloud']['endpoint'] = cloud_url + "/remote.php/dav/files/" + cloud_user + "/" + cloud_path
config['cloud']['user'] = cloud_user
config['cloud']['pass'] = input("Nextcloud pass: ")

config['folders']['data'] = input("Data folder: ")
config['folders']['temp'] = input("Temp folder: ")

config['logfile'] = input("Log file: ")
config['hours'] = float(input("Every how many hours do backups: "))


open('src/config.yml', 'w').write(dump(config, Dumper=Dumper))
