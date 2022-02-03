from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import UserAuthSerializer

from django.core.cache import cache

from eth_account.messages import encode_defunct
from web3 import Web3, HTTPProvider
from web3.auto import w3

from accounts.accounts import Account, Session
from accounts.models import UserAccount
from token_nfts.models import TokenNFT, TokenClaims
from accounts.serializers import (
    UserAccountSerializer,
    MyTokenObtainPairSerializer
)

from restapi import settings

from accounts.producer import *

import os, io
from os.path import exists


class SomeActionView(viewsets.ViewSet):

    # # NOTE: Permissions based on JWT
    # permission_classes = (IsAuthenticated,)
    # serializer_class = UserAuthSerializer

    def get_account(self, _):
        user_id = 3
        user = UserAccount.objects.get(id=user_id)
        response = {
            "id": user.id,
            "email": user.email,
            "c_addr": user.c_addr,
            "is_admin": user.is_admin
        }
        return Response(response, status=status.HTTP_200_OK)

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    
class LoginViewSet(viewsets.ViewSet):

    def login_request(self, request, c_addr=None):
        c_addr = str(c_addr).lower()
        if settings.T_REFRESH_TOKEN >= 60:
            duration = f"{int(settings.T_REFRESH_TOKEN / 60)} hours"
        else:
            duration = f"{int(settings.T_REFRESH_TOKEN)} minute(s)"
        
        sign_message = f"Welcome to MetaBrainz IO!\n\n\
            Sign this message to connect to MetaBrainz.io\n\n\
            note: \n\
            No blockchain transactions are triggered during this process. Your authentication status will reset after {duration}.\n\n\
            subject: Sign In\n\
            sign_id: "
            
        if c_addr is not None:
            # validate user
            if Account.validate_account(c_addr=c_addr):
                response = Session.setup_connection_response(c_addr, sign_message)
                return Response(response, status=status.HTTP_200_OK)

            # no users found, try create user
            else:
                if Account.create_account(c_addr=c_addr):
                    # re-validate user
                    if Account.validate_account(c_addr=c_addr):
                        response = Session.setup_connection_response(c_addr,sign_message)
                        return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def login_authenticate(self, request, c_addr=None):
        c_addr = str(c_addr).lower()
        jdata = request.data
        account = jdata['account']

        response = {"userdata":{}, "message":"", "token": "" }

        # Retrieve user from db
        user = Account.get_account(account)
        sig, sigcached = None, None
        if user:
            # Get userclaim info
            tokenIdclaims = []
            
            claims = user.claims
            if claims is not None:
                for i in range(len(claims)):
                    try:
                        tokenNFT = TokenClaims.objects.get(claim_id=claims[i])
                        if tokenNFT:
                            claim_token_id = tokenNFT.token_id.tid
                            claim_token_name = tokenNFT.token_id.name
                            tokenIdclaims.append({"tid": claim_token_id, "name":claim_token_name})
                    except:
                        print("Err")
            
            # Get from user request
            signature = jdata['signature']

            # Get from cache
            sign_message_cache = str(cache.get(account))
            cache.delete(account)

            # Restore user credentials
            message = encode_defunct(text=sign_message_cache)
            recovered = None
            try:
                recovered = w3.eth.account.recover_message(message, signature=signature)
            except:
                response = {"userdata":{}, "message": "Invalid signature", "token": "" }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)

            if recovered is not None:
                if str(account).lower() == str(recovered).lower():

                    # NOTE: Only generate jwt token after a successfull signed login 
                    token_serializer = MyTokenObtainPairSerializer()
                    jwtToken = token_serializer.get_user_token(user)
                    
                    
                    # usr_img_src = f"./static/user/{user.image}"
                    # file_contents,filebytes = None, ""
                    # FILE = None
                    # if exists(usr_img_src):
                    #     FILE = open(usr_img_src)
                    #     if not FILE.closed:
                    #         with open(usr_img_src, 'rb') as fbytes:
                    #             file_contents = fbytes.read()
                    #     FILE.close()

                    # if file_contents:
                    #     filebytes = io.BytesIO(file_contents)
                    # data = {
                    #     "profile_img":filebytes,
                    #     "userdata":{"claims": tokenIdclaims}, 
                    #     "message": "success", "token": jwtToken 
                    # }

                    response = {
                        "userdata":{"claims": tokenIdclaims}, 
                        "message": "success", "token": jwtToken 
                    }

                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {"userdata":{}, "message": "Expected account did not match!", "token": "" }
            else:
                response = {"userdata":{}, "message": "Could not recover account!", "token": "" }
        else:
            response = {"userdata":{}, "message": "No such user!", "token": "" }

        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

class LogoutViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"message": "Server: Ok, goodbye :) (cleared backend session)"})

        response = {"message": "Server: Ok, goodbye :)"}
        try:
            refresh_token = self.request.data.get('refresh_token')
            token = RefreshToken(token=refresh_token)
            token.blacklist()
        except Exception as e:
            # TODO: Log this as err
            print(e)
        return Response(response, status=status.HTTP_200_OK)