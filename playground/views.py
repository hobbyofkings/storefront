# from django.core.mail import mail_admins, send_mail, BadHeaderError, send_mass_mail, EmailMessage
# from django.http import HttpResponse
from django.shortcuts import render
# from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
import requests
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__) # __name__ is the name of the current module


class HelloView(APIView):
    def get(self, request):
        try:
            logger.info('Calling the httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Response received')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('Failed to connect to httpbin')

        return render(request, 'hello.html', {'name':'Amadesa'})







# class HelloView(APIView):
#     # for class based views we use method_decorator for caching. for function based views we use @cache_page
#     @method_decorator(cache_page(5 * 60))
#     def get(self, request):
#         response = requests.get('https://httpbin.org/delay/2')
#         data = response.json()
#         return render(request, 'hello.html', {'name':'Amadesa'})



# @cache_page(5 * 60)
# def say_hello(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
#     return render(request, 'hello.html', {'name': data})





#
# def send_email(request):
#
#     try:
#         message = BaseEmailMessage(
#             template_name='emails/hello.html',
#             context={'name': 'Amadesa admins'}
#         )
#         message.send(['listingas@gmail.com'] )
#
#     except BadHeaderError:
#         return HttpResponse('Invalid header found.')
#
#     return render(request, 'hello.html', {'name': 'Amadesa users'})







