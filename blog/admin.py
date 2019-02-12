from django.contrib import admin
from .models import Post, Comment, Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']


class PostAdmin(admin.ModelAdmin):
    list_display = ('tittle',)
    search_fields = ['tittle']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment,)

