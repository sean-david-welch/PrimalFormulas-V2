from rest_framework import serializers

from assets.models import Asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Asset
        fields = "__all__"
        read_only_fields = ["id", "created"]