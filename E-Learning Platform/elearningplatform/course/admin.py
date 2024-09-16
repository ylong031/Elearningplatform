from django.contrib import admin
from .models import *


# admin.site.index_template = 'memcache_status/admin_index.html';

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['title']
    


class ModuleInline(admin.StackedInline):
    model = Content


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'created']
    list_filter = ['created', 'department']
    search_fields = ['title', 'description']
    inlines = [ModuleInline]

admin.site.register(AppUser)