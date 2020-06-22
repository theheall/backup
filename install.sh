apt install -y python3 python3-pip
pip3 install -r requirements.txt

echo "# Configuration"
python3 configurator.py

mkdir /etc/backup
cp src/* /etc/backup/
cp backup.service /lib/systemd/system/

systemctl enable --now backup

rm -r ../backup-v1.0.0/