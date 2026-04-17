from django.contrib import admin
import blog.models as blog_models

# Register your models here.
admin.site.site_header = "Blog Admin"
admin.site.site_title = "Blog Admin Portal"
admin.site.index_title = "Welcome to the Blog Admin Portal"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# custom BlogAdmin 
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'slug')
    list_filter = ('created_at', 'category', 'author')
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Organization', {
            'fields': ('category', 'tags')
        }),
        ('Meta', {
            'fields': ('meta_description',)
        }),
        ('Author & Timestamps', {
            'fields': ('author', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(blog_models.Category, CategoryAdmin)
admin.site.register(blog_models.Tag, TagAdmin)
admin.site.register(blog_models.Post, BlogAdmin)
