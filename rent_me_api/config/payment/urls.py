from django.urls import path

from .views import PaymentTemplateView, SuccessTemplateView, ErrorTemplateView, PaymentAPIView, DemoTemplateView
# , TransactionAPIView

urlpatterns = [
    path('flutterwave/', PaymentTemplateView.as_view(), name='flutterwave'),
    path('flutterwave/success-page', SuccessTemplateView.as_view(), name='success-page'),
    path('flutterwave/error-page', ErrorTemplateView.as_view(), name='error-page'),
    
    path('checkout/', PaymentAPIView.as_view(), name='checkout'),
    # path('frontend-demo/', DemoTemplateView.as_view(), name='frontend-demo'),
]
