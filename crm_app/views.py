# crm_app/views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.urls import reverse_lazy 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.shortcuts import get_object_or_404, redirect 
from django.db.models import Q #  Qをインポート 
from .models import Customer
from .forms import CustomerForm 


# 顧客一覧表示ビュー (ListView)
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'crm_app/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    
    def get_queryset(self):
        # 1. まず、基本となる「自分の担当顧客」を取得
        queryset = Customer.objects.filter(user=self.request.user).order_by('company_name')

        # 2. GETパラメータから 'query' (検索キーワード) を取得
        query = self.request.GET.get('query')

        # 3. キーワードが存在する場合のみOR絞り込みを行う
        if query:
            # Qオブジェクトを使って「OR条件」を構築
            queryset = queryset.filter(
                Q(company_name__icontains=query) | 
                Q(contact_name__icontains=query) |
                Q(email__icontains=query) |
                Q(tags__name__icontains=query)  # タグ名での検索を追加
            ).distinct() # 重複を排除 (重要)
        
        return queryset
    
    # 検索キーワードをテンプレートに返すための設定 (UX向上)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # テンプレートに { 'query': ユーザーの入力値 } を設定 (UX向上)
        context['query'] = self.request.GET.get('query', '')
        return context

# 顧客詳細表示ビュー (DetailView)
class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "crm_app/customer_detail.html"
    context_object_name = "customer"

    # 認可: 自分が担当のデータのみを対象とする
    def get_object(self, queryset=None):
        return get_object_or_404(
            Customer.objects.filter(user=self.request.user),  # ログインユーザーで絞り込み
            pk=self.kwargs["pk"],
        )


# 顧客の新規登録ビュー (CreateView)
class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "crm_app/customer_form.html"
    success_url = reverse_lazy("customer_list")

    # 認可: フォーム保存直前に、担当営業(user)フィールドにログインユーザーをセット
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# 顧客の更新ビュー (UpdateView)
class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "crm_app/customer_form.html"
    success_url = reverse_lazy("customer_list")

    # 認可: 自分が担当のデータのみを対象とする
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)


# 顧客の削除ビュー (DeleteView)
class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = "crm_app/customer_confirm_delete.html"
    success_url = reverse_lazy("customer_list")

    # 認可: 自分が担当のデータのみを対象とする
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)