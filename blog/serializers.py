from rest_framework import serializers
from django.utils.text import slugify
from .models import Post, Category, Tag


# -------------------------------
# Helper: Unique slug generator
# -------------------------------
def get_unique_slug(model, name):
    base_slug = slugify(name)
    slug = base_slug
    counter = 1

    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


# -------------------------------
# Tag Serializer (Read Only)
# -------------------------------
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


# -------------------------------
# Category Serializer (Read Only)
# -------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


# -------------------------------
# Post Serializer
# -------------------------------
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    image = serializers.ImageField(required=False, allow_null=True)

    # ✅ WRITE (input from frontend)
    category = serializers.CharField(write_only=True, required=False)
    tags = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    # ✅ READ (response)
    category_detail = CategorySerializer(source='category', read_only=True)
    tags_detail = TagSerializer(source='tags', many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'image',

            # write
            'category', 'tags',

            # read
            'category_detail', 'tags_detail',

            'author', 'meta_description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'slug']

    # -------------------------------
    # Helpers
    # -------------------------------
    def get_or_create_category(self, name):
        if not name:
            return None

        name = name.strip()

        category = Category.objects.filter(name__iexact=name).first()

        if not category:
            category = Category.objects.create(
                name=name,
                slug=get_unique_slug(Category, name)
            )

        return category

    def get_or_create_tags(self, tag_list):
        tag_objects = []

        for tag_name in tag_list:
            tag_name = tag_name.strip()
            if not tag_name:
                continue

            tag = Tag.objects.filter(name__iexact=tag_name).first()

            if not tag:
                tag = Tag.objects.create(
                    name=tag_name,
                    slug=get_unique_slug(Tag, tag_name)
                )

            tag_objects.append(tag)

        return tag_objects

    # -------------------------------
    # CREATE
    # -------------------------------
    def create(self, validated_data):
        category_name = validated_data.pop('category', None)
        tags_data = validated_data.pop('tags', [])

        # Create category
        category = self.get_or_create_category(category_name)
        if category:
            validated_data['category'] = category

        # Create post
        post = Post.objects.create(**validated_data)

        # Create tags
        if tags_data:
            tags = self.get_or_create_tags(tags_data)
            post.tags.set(tags)

        return post

    # -------------------------------
    # UPDATE
    # -------------------------------
    def update(self, instance, validated_data):
        # Handle image replacement
        if 'image' in validated_data and instance.image:
            instance.image.delete(save=False)

        category_name = validated_data.pop('category', None)
        tags_data = validated_data.pop('tags', None)

        # Update category
        if category_name is not None:
            if category_name == "":
                instance.category = None
            else:
                instance.category = self.get_or_create_category(category_name)

        # Update fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Update tags
        if tags_data is not None:
            tags = self.get_or_create_tags(tags_data)
            instance.tags.set(tags)

        return instance