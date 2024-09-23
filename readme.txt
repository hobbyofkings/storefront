#psql "host=amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com port=5432 dbname=postgres user=postgres password=Respublika10! sslmode=require sslrootcert=rds-ca-bundle.pem"
# psql -h amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com -U postgres -d Amadesa -W
# # psql -h amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com -U postgres -d postgres -W

ssh -i C:/Users/Kompiuteris/Desktop/SSH/amadesa.pem ubuntu@54.226.195.254
# linux: source env/bin/activate
# in home pc: .\env\Scripts\Activate.ps1
# git
# go to pjrocect 'cd storefront'
# git pull origin amazon

# stash git if shiwing merge:

git stash
git pull origin amazon
git stash pop


#migrate
python manage.py migrate
python3 manage.py makemigrations


date
sudo apt install ntp
sudo service ntp restart
psql "host=amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com port=5432 dbname=amadesa user=postgres password=Respublika10! sslmode=disable"
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem -O ~/storefront/rds-ca-bundle.pem
psql "host=amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com port=5432 dbname=amadesa user=postgres password=Respublika10! sslmode=require sslrootcert=rds-ca-bundle.pem"



gunicorn --workers 3 storefront.wsgi:application
sudo nano /etc/nginx/sites-available/amadesa.com



Check Gunicorn Status Check if Gunicorn is running:
sudo systemctl status gunicorn

Restart Gunicorn:
sudo systemctl restart gunicorn
Reload the systemd configuration:

sudo systemctl daemon-reload
Check Nginx Status
Check if Nginx is running:

sudo systemctl status nginx
Restart Nginx:

sudo systemctl restart nginx
Test Nginx configuration:

sudo nginx -t
Check Active Connections
Check open ports and listening services:

sudo netstat -tuln
Check Logs
View Gunicorn logs:

sudo journalctl -u gunicorn
View Nginx error logs:

sudo tail -f /var/log/nginx/error.log


Test HTTP Response
Test Nginx server response locally:
curl http://127.0.0.1
Test the public IP or domain:
curl http://<your-public-ip>


Check Firewall Rules
Check firewall status:
sudo ufw status

List running services:
sudo systemctl list-units --type=service

View the status of all system services:
sudo systemctl --failed




