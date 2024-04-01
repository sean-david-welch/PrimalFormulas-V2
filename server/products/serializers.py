from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    # type: ignore
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id", "created"]
