from rest_framework import serializers
from clothes_app.models import Products , Cart , Client
# class ProductSerializers(serializers.ModelSerializer):
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"

class CartSerializer(serializers.Serializer):
    client = serializers.CharField(max_length = 11)
    product = serializers.CharField(max_length = 1000)
    count = serializers.IntegerField(default=0)

    # create function to create a new object related to is valid function
    def create(self, validated_data):
        client = Client.objects.get(phone = validated_data['client'])
        product = Products.objects.get(title = validated_data['product'])
        
        if Cart.objects.filter(client = client, product = product).exists():
            existProduct = Cart.objects.filter(client = client, product = product)[0]
            existProduct.count = existProduct.count + validated_data['count']
            existProduct.save()
            return existProduct
        
        return Cart.objects.create(client = client, product = product, count = validated_data['count']) 