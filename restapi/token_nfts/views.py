from django.http.request import QueryDict
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.renderers import JSONRenderer

from django.core.cache import cache

from eth_account.messages import encode_defunct
from web3 import Web3, HTTPProvider
from web3.auto import w3

from token_nfts.models import TokenNFT
from token_nfts.serializer import TokenNFTSerializer

from accounts.accounts import Account, Session
from accounts.models import UserAccount
from accounts.serializers import (
    UserAuthSerializer,
    MyTokenObtainPairSerializer
)


class TokenNFTPrivateViewSet(viewsets.ViewSet):
    # permission_classes = (IsAuthenticated, IsAdminUser)
    # serializer_class = UserAuthSerializer

    def get_token_nfts(self, request, id):
        try:
            if not TokenNFT.objects.filter(tid=id).exists():
                raise ValueError(f"No matching Token NFT's for id '{id}' found.")
        except Exception as e:
            print(f"Err: {e}")
            return Response([], status=status.HTTP_404_NOT_FOUND)

        tokenNFT = TokenNFT.objects.get(tid=id)
        return Response([{"token_name":tokenNFT.name}], status=status.HTTP_200_OK)

    def add_token_nfts(self, request):
        data = request.data

        KEYS = "tid,img_src,name,descr,attributes,quantity,links,claimable,img_src"
        
        error = None
        for k in data:
            found = False
            for validKey in KEYS.split(','):
                if k in validKey:
                    found = True
            if not found:
                error =f"Invalid json format."

        if error:
            print(f"Err: {error}")
            return Response([{"message": "Err: "+error}], status=status.HTTP_400_BAD_REQUEST)

        tokenNft_id = data['tid']
        tokenNft_name = data['name']
        tokenNft_descr = data['descr']
        tokenNft_attributes = data['attributes']
        tokenNft_quantity = data['quantity']
        tokenNft_links = data['links']
        tokenNft_claimable = data['claimable']
        tokenNft_img_src = data['img_src']

        duplicate = TokenNFT.objects.filter(tid=tokenNft_id).exists()
        if duplicate:
            return Response([{"message": "Err: Token already exists."}], status=status.HTTP_400_BAD_REQUEST)

        tokenNFT = TokenNFT(
            tid=tokenNft_id,
            name=tokenNft_name,
            descr=tokenNft_descr,
            attributes=tokenNft_attributes,
            quantity=tokenNft_quantity,
            links=tokenNft_links,
            claimable=tokenNft_claimable,
            img_src=tokenNft_img_src
        )
            
        try:
            tokenNFT.save()
        except Exception as e:
            print(f"Err: {e}")
            return Response([{"message": e}], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        print(f"Saved tokenNFT: {tokenNFT.tid}, {tokenNFT.name}, {tokenNFT.descr}, {tokenNFT.attributes}, {tokenNFT.quantity}, {tokenNFT.links}, {tokenNFT.claimable}")
        return Response(["add token"], status=status.HTTP_200_OK)

class TokenNFTPublicViewSet(viewsets.ViewSet):

    def get_token_nfts(self, request, id):
        try:
            if not TokenNFT.objects.filter(tid=id).exists():
                raise ValueError(f"No matching Token NFT's for id '{id}' found.")
        except Exception as e:
            print(f"Err: {e}")
            return Response([], status=status.HTTP_404_NOT_FOUND)

        tokenNFT = TokenNFT.objects.get(tid=id)
        serializer = TokenNFTSerializer(tokenNFT, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_all_token_nfts(self, request):
        tokenNFT = TokenNFT.objects.all()
        serializer = TokenNFTSerializer(tokenNFT, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def claim_request(self, request, c_addr=None):
        if c_addr is not None:
            # validate user
            if Account.validate_account(c_addr=c_addr):
                resp = Session.create_sign_message(c_addr=c_addr, message="signed_claim: ")
                return Response(resp, status=status.HTTP_200_OK)

        resp_err = {"addr": "", "sign_id": "", "message": "Unauthorized" }
        return Response(resp_err, status=status.HTTP_401_UNAUTHORIZED)

    def claim_token_nfts(self, request, id):
        jdata = request.data
        account = jdata['account']

        # Retrieve user from db
        user = Account.get_account(account)

        if user:
            # Get sign_message from cache by user addr
            sign_message_cache = str(cache.get(account))

            # Restore user credentials
            signature = jdata['signature']
            sign_message = sign_message_cache
            message = encode_defunct(text=sign_message)
            recovered = None
            try:
                recovered = w3.eth.account.recover_message(message, signature=signature)
            except:
                print("Err: Invalid signature")

            if recovered is not None:
                if str(account).lower() == str(recovered).lower():

                    # NOTE: Only generate jwt token after a successfull signed login
                    
                    # Serialize new token
                    token_serializer = MyTokenObtainPairSerializer()
                    jwtToken = token_serializer.get_user_token(user)
                    response = {"token": jwtToken, "message":"success"}

                    # Link user token claim
                    try:
                        if not TokenNFT.objects.filter(tid=id).exists():
                            raise ValueError(f"No matching Token NFT's for id '{id}' found.")
                    except Exception as e:
                        print(f"Err: {e}")
                        response = {"token": jwtToken, "message":e}
                        return Response(response, status=status.HTTP_404_NOT_FOUND)

                    tokenNFT = TokenNFT.objects.get(tid=id)
                    if not tokenNFT.claimable:
                        response = {"token": jwtToken, "message":"token not claimable"}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    tokenNFT.quantity = tokenNFT.quantity - 1
                    if tokenNFT.quantity == 0:
                        tokenNFT.claimable = False
                    tokenNFT.save()
                    
                    return Response(response, status=status.HTTP_200_OK)

        response = {"token": "", "message":"Unauthorized" }
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)