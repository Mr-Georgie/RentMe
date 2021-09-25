from django.urls import path

from .views import TransactionCreateAPIView, TransactionByReceiver, TransactionBySender



urlpatterns = [
    path('save/', TransactionCreateAPIView.as_view(), name='save-transaction'),
    path('list-by-sender/', TransactionBySender.as_view(), name='list-by-sender'),
    path('list-by-receiver/', TransactionByReceiver.as_view(), name='list-by-receiver'),
]
