# Collectibles Database: Revolutionizing the World of Collecting


![Python Version](https://img.shields.io/badge/python-3.x-blue)
![Django Version](https://img.shields.io/badge/django-3.x-green)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

### Amadesa.com 

Collectibles Database is your all-in-one platform for everything collectible: coins, banknotes, stamps, cameras, and more. Designed for enthusiasts, researchers, and collectors, our mission is clear: provide the most comprehensive, accurate, and user-friendly resource in the collectibles world.

It will make a huge impact for these segments: ***Researchers, Collectors, Investors, and Dealers***.

### 1. Scholars, Students, and Researchers
Platform isn’t just a database; it’s a resource hub designed for in-depth exploration. From meticulously cataloged coins and banknotes to AI-powered image recognition and real sales data, we offer tools to elevate your research. Whether you're studying history, analyzing trends, or training cutting-edge AI models, our platform equips you with:

- Precise Data: Explore clean, structured data free of duplicates, enriched with detailed tags and specifications.
- Research-Ready Images: Download labeled, high-quality images for experiments or training datasets.
- Trends and Insights: Access real sales data to uncover historical trends and valuation patterns.
- With us, history meets innovation, making Amadesa.com the ultimate ally for curious minds.

### 2. Businesses (Dealers, Auction Houses, Museums, and Numismatists)
Revolutionize how you operate in the collectibles industry with Amadesa.com. Our platform offers businesses the tools they need to thrive in a competitive market:

- Market Intelligence: Analyze real sales data to understand pricing trends, demand, and rarity metrics, empowering informed decisions.
- Efficient Cataloging: Leverage our AI-powered tools to manage inventory, enhance product listings, and attract discerning buyers.
- Enhanced Exposure: Connect with a global community of collectors, researchers, and enthusiasts.
- Credibility and Trust: Provide transparent valuations backed by historical data, bolstering customer confidence.
- Whether you're auctioning a rare coin, managing a museum collection, or selling online, Amadesa.com is your partner in precision and profitability.

### 3. Enthusiasts and Everyday Collectors
Step into the world of collectibles with confidence, backed by Amadesa.com. Whether you're just starting out or looking to assess the value of a cherished item, we make it simple and rewarding:

- Know Your Treasure: Discover the true worth of your collectibles with real sales data and detailed rarity insights.
- Learn and Grow: Dive into trends, historical contexts, and market values to become a more informed collector.
- No More Guesswork: Our app transforms collecting into a tech-driven, stress-free hobby with all the knowledge you need at your fingertips.
- Join the Community: Connect with like-minded individuals, share stories, and grow your passion.




## What Makes Us Different?

### Real Sales Data, Real Insights ###
Forget speculative asking prices. Our platform tracks real sales, providing historical prices, trends, and dates of transactions. Whether you’re a collector or an investor, our insights will empower you to make informed decisions. Auctions won’t feel like a gamble anymore; you’ll know exactly what to bid, why, and when. From rarity metrics to price recommendations and risk factors, we make collectibles investing as precise as stock trading.

### Rich Data & Powerful Scraping ###
Imagine a database that consolidates data from auctions, catalogs, and countless other sources. Our platform scrapes images, specifications, and sales data to build an organized, tag-rich library. Every collectible will be meticulously cataloged, free of duplicates or mistakes. And to achieve near-perfect accuracy, we pair cutting-edge automation with human expertise because even the best AI needs a keen eye for details like text, names, and inscriptions.

### AI-Powered Image Recognition ###
With clean, well structured data and tons of labeled images, we aim to build the most efficient neural networks for image recognition. Our API will enable developers, students, and researchers to tap into this treasure trove. Need a batch of images with precise tags and labels? Download them effortlessly - ready for experiments or training AI models. This isn’t just a tool; it’s a launchpad for innovation.

### Simplifying Collecting for Everyone ###
Coin collecting used to be a daunting hobby, requiring deep knowledge and expertise. Not anymore. Our app transforms the experience, delivering everything you need - facts, values, trends - at your fingertips. No more guesswork, no more barriers. With us, anyone can confidently dive into the world of collectibles.

### Building a Global Community ###
Our platform isn’t just a database; it’s a movement. We’re creating a vibrant, easy-to-use space where collectors connect, share, and grow. Dealers, auction houses, and collectors alike will flock to us for the unparalleled tools and insights we provide.

## The Future of Collectibles ##
We believe in making collectibles great again. With our app, every auction becomes a well-informed decision, every collectible a smart investment. The result? Higher exposure, increased values, and a reinvigorated passion for collecting.

### Our Vision ###

- Empower collectors to know the true value of their items before selling.
- Equip investors with data-driven tools for maximizing returns.
- Attract tens of thousands of collectors, dealers, and auction houses to our game-changing platform.
- Deliver a seamless, enjoyable experience that transforms collecting into a modern, tech-driven hobby.

### The Bottom Line ###
This isn’t just an app - it’s a revolution in the collectibles industry. From skyrocketing exposure to community building, we’re here to make collecting not just great but extraordinary. Join us, and let’s make history together.

Because with us, the future of collecting is now.

------
## Now for the Python studies to pass the exam
While we talk about the world chaning ideas, we need to pass the exam first. So, let's start with the requirements.
### Final Full-Stack with Python Project (max grade 10)
#### Functionality:
- Register () -> not implemented because the project is private
- Log in (inplemented, inside django)
- Create a new category (only when logged in) -> implemented
- Edit a category (only when logged in) -> implemented
- Delete a category (only when logged in) -> implemented
- Create a new note (only when logged in) -> implemented
- A note should have a title and note text. -> implemented
- There should also be an option to add images to the note. -> implemented
- It should allow assigning the note to a specific category. -> implemented
- Edit a note (only when logged in) -> implemented
- Delete a note (only when logged in) -> implemented
- Search for notes by title (only when logged in) -> implemented
- Filter notes by category (only when logged in) -> implemented


## Technology Stack short description
This private project is hosted on Amazon Web Services (AWS) with a scalable architecture, leveraging Amazon EC2 for application deployment, Amazon RDS (PostgreSQL) for database management, and Route 53 for domain management. To handle large storage requirements, images are stored on a cost-effective SAS/NAS server, ensuring affordability for massive datasets exceeding 100 TB.


## Architecture
**Application Hosting**: Amazon EC2 (Elastic Compute Cloud) with Docker containers

**Database**: Amazon RDS with PostgreSQL for scalable and managed database services. Database architecture is here: https://dbdiagram.io/d/demony-66f94cab3430cb846cf8bee0

**Domain**: amadesa.com via Amazon Route 53 (DNS management)

**Storage**: Images stored on SAS/NAS servers for cost-effective large-scale storage. (not implemented yet)

**Backend**: Django REST framework for API development


# Libraries used in the project (only the most important ones)
- Django Debug Toolbar: For debugging and performance optimization
- Django REST framework: For building APIs
- Redis: For caching and session management
- Celery: For task scheduling and background processing
- PostgreSQL: For the database
- Gunicorn: For running the Django application
- Nginx: For serving static files and reverse proxying
- Docker: For containerization and deployment
- Djoser: For user authentication and registration



## Installation (Development Environment, for you my dear reader!)

To set up the project locally. We will call it **storefront***:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/hobbyofkings/storefront.git
   cd storefront

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. **Install dependencies:**
if you are willing to deploy it to ubuntu server, please mute 'psycopg2' or change it to 'psycopg2-binary' in the requirements.txt file because it may cause some issues with the installation on the ubuntu server.
    ```bash
    pip install -r requirements.txt

if you forget to mute 'psycopg2' or change it to 'psycopg2-binary' in the requirements.txt file, you can write this command

```bash
    pip install psycopg2-binary
   ```
and this one
```bash
while read line; do
    if [[ $line != *"psycopg2"* ]]; then
        pip install "$line"
    fi
done < requirements.txt
```




   
4. **Setup Environment Variables: Create a two .env files (.env and .env.dev) in the main app folder inside settings (storefront/settings) with the following configuration:**

Disclaimer:
We keep the environment variables in a separate file to keep the code clean and secure. The .env file is used to store sensitive information like API keys, passwords, and other secrets. It is not uploaded to the repository. The .env.dev file is used for development, and the .env file is used for production.
this is env.dev file
   ```bash
   DJANGO_SETTINGS_MODULE=storefront.settings.dev
   DATABASE_NAME=amadesadb_local
   DATABASE_USER=postgres
   DATABASE_PASSWORD=Password
   DATABASE_PORT=5432
   DATABASE_HOST=localhost
   DEBUG=True
   DJANGO_SECRET_KEY=your-development-secret-key
   LOG_DIR=logs  # Use a relative path for local logs, e.g., a folder in your project
   ALLOWED_ADMIN_IPS=78.62.144.136,127.0.0.1 # Add your IP address for the Django admin panel or delete this line to allow all IPs
   ```

this is env file (for production, it configures the database to connect to the RDS, AWS). If you dont have RDS, you can use the same configuration as in the env.dev file. In my case, I have RDS, so I need to configure the database to connect to the RDS.
   ```bash
   DJANGO_SETTINGS_MODULE=storefront.settings.prod
   DATABASE_NAME=amadesadb
   DATABASE_USER=amadesa
   DATABASE_PASSWORD=Password
   DATABASE_PORT=5432
   DEBUG=False # Set to False for production
   DATABASE_HOST=amadesadb.xxxxx.us-east-1.rds.amazonaws.com
   DJANGO_SECRET_KEY=your-very-secure-secret-key-go-here
   AWS_ACCESS_KEY_ID=xxxxxxxx
   AWS_SECRET_ACCESS_KEY=xxxxxx
   LOG_DIR=logs
   ALLOWED_ADMIN_IPS=78.62.144.136,127.0.0.1 # Add your IP address for the Django admin panel or delete this line to allow all IPs
   ```
  
5. **Apply migrations:**

    ```bash
    python manage.py migrate
   
  
6. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
   

7. set up the static files
    ```bash
    python manage.py collectstatic

8. **Set the environment variable:**
before starting the server we need to set the environment variable (it will be used to load the correct settings file)
   ```bash
   export DJANGO_ENV=development
   echo $DJANGO_ENV
   ```
While I'm doing this text for me, I will use my privilege to leave personal notes for myself. I will use the following command to set the environment variable in my machine
in powershell: (run as administrator)

   ```bash   
   cd "C:\Users\Kompiuteris\Downloads\Django 3- Resources\storefront3"
   .\env\Scripts\Activate  
   # Set the environment variable, only one of the following. Comment out 
   $env:DJANGO_ENV = "production" # For production 
   $env:DJANGO_ENV = "development" # For development
   echo $env:DJANGO_ENV
   python manage.py runserver      
```
   
iMac / Linux
   ```bash
   export DJANGO_ENV=production
   echo $DJANGO_ENV  
   ```

9. **Start the development server:**

```bash
python manage.py runserver
 ```
   
Access the application at http://127.0.0.1:8000/.

Congratulations! The project is now up and running. You can check the admin panel at /admin/ and log in with the superuser credentials you created earlier.
Please take a look to Django documentation for more information about the project structure and how to work with Django.
Some of the most important django commands are listed below, read: Django Commands

----------------
## Deployment: Production on AWS (For those planning AWS ECS and RDS Deployment)
Deploying a project to AWS ECS and RDS is a significant endeavor, requiring careful planning, configuration, and research. While this particular project might not be life-changing, deploying it properly demands time and effort. Below, you'll find an outline of the steps involved in preparing and deploying the project to AWS. Please note, this is not an exhaustive guide, and you'll need to dive deeper into specific topics as you proceed.

### Steps for AWS Deployment:
1. Prepare the Project for Production:
- Ensure the project is fully configured for production use, including setting DEBUG=False in Django settings.
- Use environment variables for sensitive information such as database credentials and secret keys.
- Configure static files and media storage (consider using S3 for production or other cloud storage services or if you are smart and you have huge ambitions, you can use SAS/NAS servers for cost-effective large-scale storage).

2. Set Up AWS Services:
- Create an RDS instance to host your PostgreSQL database.
- Set up an ECS cluster to manage your Dockerized application.
- Use Amazon ECR (Elastic Container Registry) to store your Docker images.
3. Containerization:

- Ensure the project is containerized using Docker.
- Build and push your Docker images to the ECR repository. 

4. Task Definition and Service Configuration:

- Create ECS task definitions for your services (e.g., Django app and Nginx).
- Configure an ECS service to handle task scaling and placement.
5. Networking:

- Set up a VPC, subnets, and security groups to ensure secure communication between ECS, RDS, and any other AWS resources.
- Configure a load balancer (ALB) for handling incoming traffic and directing it to ECS tasks.


6. Domain and SSL:

- Use Route 53 to manage your domain's DNS records.
- Configure SSL certificates using AWS Certificate Manager (ACM) for secure HTTPS connections.

7. Monitoring and Logging:

- Enable CloudWatch for monitoring application performance and logging.
- Set up alarms and notifications for critical events.
8. Deployment Process:

- Use AWS CLI, SDKs, or infrastructure as code tools like Terraform or CloudFormation to automate deployment.
- Test the deployment thoroughly in a staging environment before promoting it to production.
9. Post-Deployment Steps:

- Monitor application performance and address any issues promptly.
- Implement scaling policies to handle variable traffic loads.

While this overview highlights the essential steps, you’ll need to conduct detailed research and adapt the process to fit the specific needs of your project. AWS documentation and chatGPT are excellent resources to guide you through this madness. Good luck!

----------------

## Steps to connect to the server (Ubuntu) | Update the server | Run the project


1. ### Connect to the server:
I am using the SSH key, so I need to send the key to the server first. My SSH is saved in my desktop, so I need to send it to the server. I am using the scp command to send the key to the server.

```bash
scp -i "C:\Users\Kompiuteris\Desktop\SSH\amadesa.pem" "C:\Users\Kompiuteris\Desktop\SSH\amadesa.pem" ubuntu@67.202.22.239:~
 ```
now I can connect to the server using the SSH key. Ip address is the public IP address of the server.
    
```bash
ssh -i "C:\Users\Kompiuteris\Desktop\SSH\amadesa.pem" ubuntu@67.202.22.239
   ```
Congrats! now you are connected to the Ubuntu server. it should look like this:
    
```bash
ubuntu@ip-172-31-87-241:~$
   ```

2. ### Update the system (Ubuntu):
to update the system, I need to run the following commands:
    
```bash
sudo apt-get update
sudo apt-get upgrade
   ```
3. ### Activate the virtual environment:
to activate the virtual environment, I need to run the following commands:
    
```bash
cd ~/storefront
source venv/bin/activate
   ```


logs can be checked using the following command:
    
```bash
sudo cat /var/log/syslog
  ```

### 4. Run Tmux (To run multiple terminals in one terminal)
tmux (for the session, tmux is an open-source terminal multiplexer for Unix-like operating systems. It allows multiple terminal sessions to be accessed simultaneously in a single window
        
list of all tmux sessions
        
```bash
tmux list-sessions
 ```


to check if tmux is running

```bash
ps aux | grep tmux
```

should be Tmux session running with name gunicorn (if not, you can start it using the following command)
    
```bash
tmux new-session -s gunicorn
 ```
to attach to the session
        
```bash
tmux attach-session -t gunicorn
  ```
to detach from the session**
        
```bash
Ctrl+b, then d
```


### 5. Start the Gunicorn server:
to start the gunicorn server, I need to run the following command:
    
```bash
/home/ubuntu/storefront/venv/bin/gunicorn --env DJANGO_SETTINGS_MODULE=storefront.settings.prod storefront.wsgi:application --bind 0.0.0.0:8000 --log-level debug --workers 3
 ```

check if gunicorn is running
    
```bash
ps aux | grep gunicorn
  ```
restart the gunicorn server
    
```bash
sudo systemctl restart gunicorn
  ```


Now while Gunicon is running inside you can detach from the session (Ctrl+b, then d) and you can run the following command to check if the server is running

------------------------------
  

## Database commands (RDS and Postgres)
***RDS (Relational Database Service)*** is a managed service that makes it easy to set up, operate, and scale a relational database in the cloud. It provides cost-efficient and resizable capacity while automating time-consuming administration tasks such as hardware provisioning, database setup, patching, and backups.

to test if database is running (Amazon RDS)
```bash
Test-NetConnection -ComputerName amadesadb.cp8a808oguxu.us-east-1.rds.amazonaws.com -Port 5432
 ```

to connect to database
    
   ```bash
    psql -h amadesadb.cp8a808oguxu.us-east-1.rds.amazonaws.com -U amadesa -d amadesadb -p 5432
  ```



### For local development (Postgres)
to start from scratch with the Postgres database using terminal
we need to login to enter the Postgres shell
   ```bash
    psql -U postgres    
   ```
to create a new user (username will be postgres)
   ```bash
   
    CREATE USER postgres WITH PASSWORD 'password';
   ```

to create a new database

```bash
CREATE DATABASE amadesadb_local WITH OWNER postgres;
 ```
   
      
to grant all privileges to the user
```bash
GRANT ALL PRIVILEGES ON DATABASE amadesadb_local TO postgres;
 ```
    
to connect to the database
```bash
\c amadesadb_local
 ```

 
### Postgres commands
list all databases

   ```bash
    \l
  ```
list all tables in a database

   ```bash
    \c amadesadb
    \dt
  ```
list all columns in a table

   ```bash
    \d+ foundation_country
  ```

list all rows in a table

   ```bash
    SELECT * FROM foundation_country;
  ```

--------------------------
    
    



## Main Github commands (for me)
   ```bash   
   git pull origin amazon # pull the latest changes from the amazon branch
   git stash # save the changes
   git stash apply # apply the changes
   
   ```


## Django commands


to create a new project
```bash
django-admin startproject storefront
  ```

create superuser
```bash
python manage.py createsuperuser
  ```

to create a new app
```bash   
python manage.py startapp storefront
  ```

After creating a new app, add the app to the installed apps in the settings.py file
```bash   
 INSTALLED_APPS = [
 'storefront',
 ]
 ```
we create a new model in the storefront/models.py file
Django will create a table in the database for this model automatically
It will do a lot of behind the scenes work like creating a table, creating a primary key, creating a foreign key, etc.
Create a model for coins

```bash   
 class Coin(models.Model):
     name = models.CharField(max_length=100)
     description = models.TextField()
     year = models.IntegerField()
     country = models.ForeignKey(Country, on_delete=models.CASCADE)
     denomination = models.ForeignKey(Denomination, on_delete=models.CASCADE)
     metal = models.ForeignKey(Metal, on_delete=models.CASCADE)
     weight = models.DecimalField(max_digits=10, decimal_places=2)
     diameter = models.DecimalField(max_digits=10, decimal_places=2)
     thickness = models.DecimalField(max_digits=10, decimal_places=2)
     obverse = models.ImageField(upload_to='coins/')
     reverse = models.ImageField(upload_to='coins/')
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     def __str__(self):
         return self.name
  ```

to apply the changes
```bash   
 python manage.py makemigrations
 python manage.py migrate
  ```
views are used to handle the request and return the response
create a view in the storefront/views.py file
lets create a health check view (Amazons health check service will check this view to see if the server is running)
```bash   
 from django.shortcuts import render
 from django.http import HttpResponse
 def health_check(request):
     return HttpResponse('OK')
  ```
to create a url for the view
create a new file in the storefront folder called urls.py
```bash   
 from django.urls import path
 from . import views
 urlpatterns = [
     path('health/', views.health_check),
 ]
  ```
to include the urls in the main project
add the following line to the urlpatterns in the storefront/urls.py file
```bash   
path('', include('storefront.urls')),
  ```
to run the server
```bash   
python manage.py runserver
  ```
**to check the health check view**
endpoint ends with health_check, example: https://amadesa.com/health/
in local development, the endpoint will be http://


to check the admin panel
endpoint ends with /admin, example: http://amadesa.com/admin/
