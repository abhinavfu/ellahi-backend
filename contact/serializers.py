from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False)
    service = serializers.CharField(max_length=100, required=False)
    message = serializers.CharField()
    time = serializers.CharField(max_length=50, required=False)