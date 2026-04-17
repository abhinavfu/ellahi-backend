from rest_framework import serializers
from .models import Post, Category, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    image = serializers.ImageField(required=False, allow_null=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='tags'
    )

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'image',
            'category', 'category_id', 'tags', 'tag_ids',
            'author', 'meta_description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        category_id = validated_data.pop('category_id', None)
        
        if category_id:
            validated_data['category_id'] = category_id
        
        post = Post.objects.create(**validated_data)
        if tags:
            post.tags.set(tags)
        
        return post

    def update(self, instance, validated_data):
        # Handle image deletion when updating
        if 'image' in validated_data:
            if instance.image:
                instance.image.delete(save=False)
        
        tags = validated_data.pop('tags', None)
        category_id = validated_data.pop('category_id', None)
        
        if category_id is not None:
            validated_data['category_id'] = category_id
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags is not None:
            instance.tags.set(tags)
        
        return instance