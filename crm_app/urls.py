# crm_app/urls.py

from django.urls import path
from .views import (
    CustomerListView, 
    CustomerDetailView,
    CustomerCreateView, 
    CustomerUpdateView, 
    CustomerDeleteView ,
    ajax_add_activity # ★ 新規追加
) 

urlpatterns = [
    
    
    # 顧客一覧ページ (R: Read List)
    path('', CustomerListView.as_view(), name='customer_list'),

    # 顧客詳細ページ (R: Read Detail)
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    
    # 新規登録ページ (C: Create)
    path('customer/new/', CustomerCreateView.as_view(), name='customer_create'), 

    # 更新ページ (U: Update)
    path('customer/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_update'), 

    # 削除確認ページ (D: Delete)
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'), 

    # Ajax処理用URL
    path('ajax_add_activity/', ajax_add_activity, name='ajax_add_activity'), 

]