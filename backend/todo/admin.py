from django.contrib import admin

from todo.models import Category, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user',]
    search_fields = ['name', 'user',]

    readonly_fields = ['id',]
    fields = ['name', 'user',]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category', 'user', 'completed',]
    search_fields = ['title', 'category', 'user',]

    readonly_fields = ['id', 'created_at', 'updated_at',]
    fields = [
        ('title', 'description'),
        ('created_at', 'updated_at'),
        ('due_date', 'completed'),
        'category', 'user',
    ]
