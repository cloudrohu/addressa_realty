from django.contrib import admin

from core.models import PocketCategory, PocketItem

# Register your models here.


# ================= CATEGORY ADMIN =================
@admin.register(PocketCategory)
class PocketCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


# ================= ITEM ADMIN =================
@admin.register(PocketItem)
class PocketItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'slug']
    list_filter = ['category']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}