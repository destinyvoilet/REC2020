from django.contrib import admin

# Register your models here.
from myblog.models import Blog, Category, Tag

#admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Tag)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'click_nums', 'category', 'create_time', 'modify_time']

admin.site.register(Blog, BlogAdmin)
