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
from accounts.serializers import (
    UserAccountSerializer,
    MyTokenObtainPairSerializer
)



from accounts.producer import *


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
        if c_addr is not None:
            # validate user
            if Account.validate_account(c_addr=c_addr):
                resp = Session.create_sign_message(c_addr=c_addr, message="signed_login: ")
                return Response(resp, status=status.HTTP_200_OK)

            # no users found, try create user
            else:
                if Account.create_account(c_addr=c_addr):
                    # re-validate user
                    if Account.validate_account(c_addr=c_addr):
                        resp = Session.create_sign_message(c_addr=c_addr, message="signed_login: ")
                        return Response(resp, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def login_authenticate(self, request, c_addr=None):
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
                    print("SERIALIZE TOKEN")
                    token_serializer = MyTokenObtainPairSerializer()
                    jwtToken = token_serializer.get_user_token(user)
                    print("MY TOKEN")
                    print(jwtToken)
                    response = {"token": jwtToken }
                    return Response(response, status=status.HTTP_200_OK)

        response = {"token": "" }
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

class LogoutViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"}, status=status.HTTP_200_OK)