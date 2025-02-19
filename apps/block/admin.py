from django.contrib import admin
from .models import Block, AboutUs
from slugify import slugify

def generate_unique_slug(model, slug_field, source_field, instance):
    if not getattr(instance, slug_field):
        slug = slugify(getattr(instance, source_field))
        i = 1
        while model.objects.filter(**{slug_field: slug}).exists():
            slug = f"{slugify(getattr(instance, source_field))}-{i}"
            i += 1
        setattr(instance, slug_field, slug)

class BaseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    search_fields = ("title", "description")
    exclude = ("slug",)

    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, 'slug', 'title', obj)
        super().save_model(request, obj, form, change)

class AboutUsAdmin(BaseAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name', 'text')

    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, 'slug', 'name', obj)
        super().save_model(request, obj, form, change)

admin.site.register(Block, BlockAdmin)
admin.site.register(AboutUs, AboutUsAdmin)