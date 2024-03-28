from rest_framework import serializers

from about.models import About


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = "__all__"
        read_only_fields = ["id", "created"]
