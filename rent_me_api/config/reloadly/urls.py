from django.urls import path

from .views import ReloadlyPaymentAPIView, GetSupportedCountries

urlpatterns = [
    path('payment-api', ReloadlyPaymentAPIView.as_view(), name='payment-api'),
    path('get_countries', GetSupportedCountries.as_view(), name='get_countries')
]