import logging

import requests
from django.shortcuts import render
from rest_framework.views import APIView
from .tasks import notify_customers

logger = logging.getLogger(__name__)


# from django.core.mail import EmailMessage, BadHeaderError
# from templated_mail.mail import BaseEmailMessage

# def send_mail(request):
#     try:
#        message = BaseEmailMessage(
#            template_name='emails/hello.html',
#            context={'name': 'Mosh'}
#        )
#        message.send(['john@moshbuy.com'])
#     except BadHeaderError:
#         pass
#     return render(request, 'hello.html', {'name': 'Mosh'})

# from django.core.cache import cache
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# class Caching(APIView):
#     @method_decorator(cache_page(5 * 60))
#     def get(self, request):
#         response = requests.get('https://httpbin.org/delay/2')
#         data = response.json()
#         return render(request, 'hello.html', {'name': 'Mosh'})

class HelloView(APIView):
    def get(self, request):
        # celery
        notify_customers.delay('Hello World')
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Received the response')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('httpbin is offline')
        return render(request, 'hello.html', {'name': 'Mosh'})
