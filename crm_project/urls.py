# crm_project/urls.py

from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    # 1. AdminサイトのURL
    path('admin/', admin.site.urls),
    
    # 2. Django標準の認証URLを読み込む (ここに追加)
    path('accounts/', include('django.contrib.auth.urls')), # <--- この行を追加
    
    # 3. crm_appのURLをルートに誘導
    path('', include('crm_app.urls')),
]