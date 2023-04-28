from asyncio import format_helpers
from django.contrib import admin
from .models import Account, Tag, Category, Transaction, TransactionImage


class TransactionImageInline(admin.TabularInline):
    model = TransactionImage
    # extra = 5
    # max_num = 5


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'name',
        'balance'
    )
    list_display_links = (
        'id',
        'owner'
    )
    list_filter = ('owner',)
    list_editable = ('balance',)
    search_fields = ('name',)
    readonly_fields = ('id',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 1


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'account',
        'create_date',
        'category',
        'description',
        'amount'
    )
    list_display_links = (
        'id',
        'account',
        'create_date',
    )
    list_filter = (
        'account',
        'create_date',
        'category',
        'tags',
        'description',
        'amount'
    )
    search_fields = (
        'account',
        'category',
        'tags',
        'description',
    )
    inlines = (TransactionImageInline,)

    

@admin.register(TransactionImage)
class TransactionImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'image',
        'transaction'
    )

    def image_preview(self, obj):
        image_html = ''
        if obj.images.exists():
            image_html = format_helpers('<img src="{}" height="50"/>', obj.images.first().image.url)
        return image_html

    image_preview.short_description = 'Изображение'

    
