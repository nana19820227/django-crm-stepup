# crm_app/views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.urls import reverse_lazy 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.shortcuts import get_object_or_404, redirect 
from django.db.models import Q #  Qをインポート 
from .forms import CustomerForm 
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse # JsonResponse をインポート
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required 
from .models import Customer, Activity
from .forms import CustomerForm, ActivityForm 



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
# Ajax専用ビューの定義

@login_required 
@require_POST
def ajax_add_activity(request):
   
    
    customer_id = request.POST.get('customer_id')
    customer = get_object_or_404(Customer, pk=customer_id)
    
    #自分の顧客でなければエラー
    if customer.user != request.user:
        return JsonResponse({'message': '権限がありません。'}, status=403)
        
    # フォームを使ってバリデーションエラー
    form = ActivityForm(request.POST)

    if form.is_valid():
        # まだdbには保存しない
        activity = form.save(commit=False)
        activity.customer = customer#紐付け
        activity.save()#保存
        
        #Java Script側に返すデータを辞書型で作る
        response_data = {
            'message': 'ok',
            'activity_date': activity.activity_date.strftime('%Y-%m-%d'),
            'status_display': activity.get_status_display(),
            'note': activity.note,
        }
        return JsonResponse(response_data) #Jsonとして返す
    else:
        # バリデーションエラーの場合
        return JsonResponse({'message': '入力内容に誤りがあります', 'errors': form.errors}, status=400)