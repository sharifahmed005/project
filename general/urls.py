from general.views import about, agreeculturist, contact, home, message_expart, message_farmer, message_list, order, privacy, report, sms_farmar, subscriber, terms
from django.urls.conf import path


urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('terms-of-policy', terms, name='terms'),
    path('privacy-policy', privacy, name='privacy'),
    path('contact', contact, name='contact'),
    path('subcriber', subscriber, name='sub'),
    path('agreecuture', agreeculturist, name='agreeculturist'),
    path('sms/', sms_farmar, name='sms'),
    path('order/', order, name='order'),
    path('report/', report, name='report'),
    path('message/<int:id>/', message_farmer, name='message'),
    path('message-reply/<int:id>/', message_expart, name='message_reply'),
    path('message-list/', message_list, name='message_list'),
]
