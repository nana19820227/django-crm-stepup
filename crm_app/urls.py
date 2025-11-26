# crm_app/urls.py

from django.urls import path
from .views import CustomerListView, CustomerDetailView # 作成したCBVをインポート

urlpatterns = [
    # 顧客一覧ページ (URL: /)
    path('', CustomerListView.as_view(), name='customer_list'),

    # 顧客詳細ページ (URL: /customer/1/)
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
]