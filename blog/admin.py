from django.contrib import admin
from .models import Post,Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display=('id','title','slug','author','publish','status')
    list_filter =('status','created','publish','author')
    prepopulated_fields={'slug':('title',)}
    search_fields =('title','body')
    date_hierarchy = 'publish'
    ordering = ('status','publish')
    
class CommentAdmin(admin.ModelAdmin):
    list_display =('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields =('name','email','body')
    
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)