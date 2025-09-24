from rest_framework import serializers

from todo.models import Category, Task


class CategorySerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Category
        fields = ('id', 'name', 'user',)
        read_only_fields = ('id', 'user',)


class TaskSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'created_at', 'due_date', 'category', 'user', 'completed', 'category_name',)
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'category_name',)
