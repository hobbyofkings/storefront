#psql "host=amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com port=5432 dbname=postgres user=postgres password=Respublika10! sslmode=require sslrootcert=rds-ca-bundle.pem"
# psql -h amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com -U postgres -d Amadesa -W
# # psql -h amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com -U postgres -d postgres -W

#  ssh -i C:/Users/Kompiuteris/Desktop/SSH/amadesa.pem ubuntu@54.226.195.254
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