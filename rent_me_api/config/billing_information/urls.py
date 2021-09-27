from django.urls import path

from .views import BillingInfoAPIView, GetBillingInfos, EditBillingInfoDetails

urlpatterns = [
    path('save-info', BillingInfoAPIView.as_view(), name='save-info'),
    path('get-info', GetBillingInfos.as_view(), name='get-info'),
    path('edit-update-info/<int:id>', EditBillingInfoDetails.as_view(), name='edit-update-info'),
]
