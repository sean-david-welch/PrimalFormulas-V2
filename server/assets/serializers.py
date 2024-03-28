from rest_framework import serializers

from assets.models import Assets


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = "__all__"
        read_only_fields = ["id", "created"]
