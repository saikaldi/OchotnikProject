from django.contrib import admin
from .models import Block, AboutUs
# Register your models here.

class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title",)}
    
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name', 'test')
    prepopulated_fields = {"slug": ("name",)}
    
admin.site.register(Block, BlockAdmin)
admin.site.register(AboutUs, AboutUsAdmin)