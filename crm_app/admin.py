from django.contrib import admin
from .models import Customer, Activity, Tag # 作成したモデルをインポート

# Tagモデル用の設定 (TagAdmin)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

# 顧客モデル用の設定 (CustomerAdmin)
class CustomerAdmin(admin.ModelAdmin):
    # Customer モデルには 'user' (担当営業) があるため、残します。
    list_display = ('company_name', 'contact_name', 'email', 'user', 'created_at',)
    list_filter = ('tags', 'user',)
    search_fields = ('company_name', 'contact_name', 'email',)

    fieldsets = (
        ("基本情報", {'fields': ('company_name', 'contact_name', 'email', 'phone',)}),
        ("担当者", {'fields': ('user',)}),
        ("タグ", {'fields': ('tags',)}),
    )
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at',)


# 商談履歴モデル用の設定 (ActivityAdmin)
# 🚨 エラー箇所を修正: Activity モデルに直接 'user' フィールドはないため、削除します。
class ActivityAdmin(admin.ModelAdmin):
    # 'user' の参照を削除
    list_display = ('status', 'activity_date', 'customer', 'created_at',)
    # 'user' の参照を削除
    list_filter = ('status', 'customer',)
    
    search_fields = ('customer__company_name', 'note',)
    
    date_hierarchy = 'activity_date'
    
    # 'user' の参照を削除
    fields = ('customer', 'activity_date', 'status', 'note',)
    
    # 'user' の参照を削除
    raw_id_fields = ('customer',) # 修正後
    
# Adminサイトにモデルと設定クラスを登録する
admin.site.register(Tag, TagAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Activity, ActivityAdmin)