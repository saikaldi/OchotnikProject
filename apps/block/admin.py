from django.contrib import admin
from .models import Block
# Register your models here.

class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title",)}
    
admin.site.register(Block, BlockAdmin)