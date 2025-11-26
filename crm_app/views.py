# crm_app/views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin  # 認証 (ログイン必須)
from django.shortcuts import get_object_or_404
from .models import Customer
from .forms import CustomerForm


# 顧客一覧表示ビュー (ListView)
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'crm_app/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    # 認可: ログインしているユーザーが担当の会社だけを取得する
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user).order_by("company_name")


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