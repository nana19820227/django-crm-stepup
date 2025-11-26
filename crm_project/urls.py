# crm_project/urls.py

from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    # Adminサイトへのルーティング
    path('admin/', admin.site.urls),
    
    # ルートURL (http://127.0.0.1:8000/) を crm_app の urls.py へ誘導
    path('', include('crm_app.urls')),
]