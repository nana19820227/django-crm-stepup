# crm_app/views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView # CreateView, UpdateView, DeleteViewをインポート
from django.urls import reverse_lazy # リダイレクト先を指定するためにインポート
from .models import Customer
from .forms import CustomerForm # 作成したフォームをインポート

# 前回作成した CustomerListView, CustomerDetailView は変更なし ---

# 顧客一覧表示ビュー (ListView)
class CustomerListView(ListView):
    model = Customer
    template_name = 'crm_app/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10
    queryset = Customer.objects.all().order_by('company_name')

# 顧客詳細表示ビュー (DetailView)
class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'crm_app/customer_detail.html'
    context_object_name = 'customer'

# 顧客の新規登録ビュー (CreateView)
class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm # 使用するフォームを指定
    template_name = 'crm_app/customer_form.html' # 新規も更新も同じテンプレートを使い回す
    success_url = reverse_lazy('customer_list') # 成功したら一覧ページにリダイレクト

# 顧客の更新ビュー (UpdateView)
class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'crm_app/customer_form.html'
    success_url = reverse_lazy('customer_list')
    # UpdateView は <int:pk> で渡されたIDの顧客データを自動でフォームにセットしてくれる

# 顧客の削除ビュー (DeleteView)
class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'crm_app/customer_confirm_delete.html' # 削除確認用の専用テンプレート
    success_url = reverse_lazy('customer_list')