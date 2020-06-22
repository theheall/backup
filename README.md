# TheHeall Backup System

### How it works
1. List all UUID folder in the daemon-data folder
2. Create temporary archives for every server
4. Retrieve from pterodactyl API the servers' name from their UUID
3. Upload all the archives with the right name to a nextcloud instance 
4. Delete all local archives

### Dependencies
- python3 (Tested on python 3.8.3)
- python module requests, pyyaml and schedule

### Installing
```bash
apt -y install unzip

# Download the archive from github and then unzip it
wget https://github.com/TheHeall/backup/releases/download/v0.1.0/backup-v0.1.0.zip
unzip backup-v0.1.0.zip

# Start the installer and follow instruction
cd backup-v1.0.0/
sh ./install.sh
```

### Usage
```bash
# The service is enabled by default

# To disable the servive
systemctl disable backup

# To change the configuration
nano /etc/backup/config.yml
systemctl restart backup
```

### Default Config File
```yaml
panel:
  url: <http(s)://panel.server.tld>
  token: <PANEL_API_KEY with SERVER READ perm>
cloud:
  endpoint: <http(s)://cloud.server.tld/remote.php/dav/files/<user>/<path_to_folder>/>
  user: <NEXTCLOUD_USER>
  pass: <NEXTCLOUD_PASS>
folders:
  data: /srv/daemon-data/ # Where all server file are stored
  temp: /tmp/ # Where all temp archive are created
hours: 1 # min: 0.1 max: 24
logfile: /var/log/backup.log
```
