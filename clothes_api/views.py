from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from clothes_app.models import Products , Client , Cart
from rest_framework.authentication import TokenAuthentication

# Create your views here.

####################################################################### products #################################################################
class ProcutsApi(APIView):

    # authentication
    authentication_classes = (TokenAuthentication,)

    # get all products
    def get(self,request):
        products = Products.objects.all()
        product_serializer = ProductSerializer(products, many=True)
        return Response(product_serializer.data)

    # update product
    def put(self, request):
        if request.user.is_authenticated:
            productId = request.data.get('id')

            # finding product by id
            try:
                product = Products.objects.get(id=productId)
                serializers = ProductSerializer(data=request.data, instance=product, partial=True)
                if serializers.is_valid():
                    serializers.save()
                    return Response({"status": "success", "data": serializers.data})

                return Response({"status": "success", "data": product})
            except Products.DoesNotExist as e:
                return Response({"status": "failed", "data": "the product does not exist"})
        else:
            return Response({"status": "failed", "data": "invalid user"})
    ####################################################################### cart #################################################################
# all method of card
class CartApi(APIView):

    # get method to get all the cards
    def get(self , request , phone):

        # getting client by phone
        try:
            # finding client
            client = Client.objects.get(phone=phone)
            
            #finding the cards
            cards = Cart.objects.filter(client=client)
            card_serializer = CartSerializer(instance=cards, many=True)
            return Response({"status": "success", "data": card_serializer.data})
        except Client.DoesNotExist as e:
            return Response({"status": "failed", "data": []})

    # post method to add a card
    def post(self , request , phone):
        try:
            #finding client
            client = Client.objects.get(phone = phone)
            deserialize = CartSerializer(data=request.data)
            if deserialize.is_valid():
                # checking if the client is the same as phone or not
                if phone != deserialize.validated_data['client']:
                    return Response({"status": "failed", "data": "the phone does not match"})
                
                deserialize.save()
                return Response({"status": "success", "data": deserialize.data})
            return Response(deserialize.errors)
        
        except Client.DoesNotExist as e:
            return Response({"status": "failed", "data": "the client does not exist"})
        
    # Delete method to delete a card
    def delete(self, request, phone):

        # checking if the client is the same as phone or not
        if phone!= request.data.get('client'):
            return Response({"status": "failed", "data": "the phone does not match"})
        
        # finding card
        try:
            # finding client
            client = Client.objects.get(phone = phone)
            
            # finding product
            print(request.data.get('product'))
            try:
                product = Products.objects.get(title = request.data.get('product'))

                # finding card and delete it
                try:
                    card = Cart.objects.get(client = client, product = product)
                    card.delete()

                    return Response({"status": "success", "data": "the card has been deleted"})
                
                except Cart.DoesNotExist as e:
                    return Response({"status": "failed", "data": "the card does not exist for this client"})
            
            except Products.DoesNotExist as e:
                return Response({"status": "failed", "data": "Product not found"})
            
        except Client.DoesNotExist as e:
            return Response({"status": "failed", "data": []})
    