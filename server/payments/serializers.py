from typing import List
from rest_framework import serializers

from products.models import Product


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    product_name = serializers.StringRelatedField()
    product_description = serializers.StringRelatedField()
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    product_image = serializers.StringRelatedField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, pk: str) -> bool:
        try:
            Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product Does not exist")

        return True


class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    cart_total = serializers.SerializerMethodField()

    def get_cart_total(self) -> float:
        total = 0
        for item in self.validated_data["items"]:
            total += item["quantity"] * item["product_price"]
        return total


class PaymentDataSerializer(serializers.Serializer):
    cart = CartSerializer()
    ui_mode = serializers.CharField()

    def create_line_items(self) -> List[dict]:
        cart_items = self.validated_data["cart"]["items"]

        line_items = [
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": item["product_name"],
                        "description": item.get("product_description", ""),
                        "images": [item["product_image"]]
                        if item.get("product_image")
                        else [],
                    },
                    "unit_amount": int(item["product_price"] * 100),
                    "tax_behavior": "inclusive",
                },
                "quantity": item["quantity"],
            }
            for item in cart_items
        ]
        return line_items

    def validate_ui_mode(self) -> None:
        if self.ui_mode not in ["embedded", "hosted"]:
            raise serializers.ValidationError(
                "Invalid UI mode. Choose either 'embedded' or 'hosted'."
            )
