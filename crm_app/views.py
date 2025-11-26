from django.views.generic import ListView, DetailView
from .models import Customer

# 顧客一覧表示用のビュー
class CustomerListView(ListView):
    model = Customer
    template_name = 'crm_app/customer_list.html'
    context_object_name = 'customers'
    
    # おまけ: 1ページに表示する件数 (ページネーション)
    paginate_by = 10
    
    # おまけ: 並び順の指定 (会社名順)
    queryset = Customer.objects.all().order_by('company_name')


# 顧客詳細表示用のビュー
class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'crm_app/customer_detail.html'
    context_object_name = 'customer'