from django.urls import path
from .views import ContactFormView

urlpatterns = [
    path('api/contact/', ContactFormView.as_view(), name='contact-form'),
]