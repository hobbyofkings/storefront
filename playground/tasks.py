import logging
from time import sleep
from celery import shared_task
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


from celery import shared_task



@shared_task
def notify_customers(message):
    print('Sending emails...')
    print('Message:', message)
    sleep(10)
    print('Emails sent.')









