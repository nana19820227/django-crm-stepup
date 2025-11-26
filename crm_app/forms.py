# crm_app/forms.py

from django import forms
from .models import Customer

# 顧客情報登録・更新用のフォームを定義
class CustomerForm(forms.ModelForm):
    
    # フォームのメタ情報
    class Meta:
        model = Customer # どのモデルをベースにするか
        
        # フォームに表示するフィールド
        fields = ('company_name', 'contact_name', 'email', 'phone', 'user', 'tags')
        
        # 必須項目にしたくない場合など、個別の設定
        # (今回は user と tags を必須ではない設定にします)
        widgets = {
            # user と tags にフォームコントロールクラスを適用
            'user': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }