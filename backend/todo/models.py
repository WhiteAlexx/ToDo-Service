import time

from django.db import models

from users.models import User


def generate_pk(telegram_id):
    return int(f"{telegram_id}{int(time.time() * 1000)}")


class Category(models.Model):
    id = models.DecimalField(max_digits=23, decimal_places=0, primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Name')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='From user')

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_pk(self.user.telegram_id)
        super().save(*args, **kwargs)


class Task(models.Model):

    id = models.DecimalField(max_digits=23, decimal_places=0, primary_key=True)
    title = models.CharField(max_length=50, verbose_name='Title')
    description = models.TextField(blank=True, verbose_name='Description')
    created_at = models.DateField(auto_now_add=True, verbose_name='Created date')
    updated_at = models.DateField(auto_now=True, verbose_name='Updated date')
    due_date = models.DateField(null=True, blank=True, verbose_name='Due date')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='From category')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='From user')
    completed = models.BooleanField(default=False, verbose_name='Completed')

    class Meta:
        db_table = 'task'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_pk(self.user.telegram_id)
        super().save(*args, **kwargs)
