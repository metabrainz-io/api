from ipaddress import ip_address
from json.tool import main
from django.http.request import QueryDict
from django.db import IntegrityError
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.renderers import JSONRenderer

from django.core.cache import cache

from eth_account.messages import encode_defunct
from web3 import Web3, HTTPProvider
from web3.auto import w3

from token_nfts.models import TokenNFT, TokenClaims
from token_nfts.serializer import TokenNFTSerializer

from accounts.accounts import Account, Session
from accounts.models import UserAccount
from accounts.serializers import (
    UserAuthSerializer,
    MyTokenObtainPairSerializer
)

import hashlib, json
from datetime import datetime, date
from random import Random

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

        KEYS = "tid,name,uri,mint_max,mint_limit,mint_cur,claimable_amount,claimable,claimable,links"
        
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
        duplicate = TokenNFT.objects.filter(tid=tokenNft_id).exists()

        if duplicate:
            return Response([{"message": "Err: Token already exists."}], status=status.HTTP_400_BAD_REQUEST)
        
        tokenNft_name = data['name']
        tokenNft_uri = data['uri']
        tokenNft_mint_max = data['mint_max']
        tokenNft_mint_limit = data['mint_limit']
        tokenNft_mint_cur = data['mint_cur']
        tokenNft_claimable = data['claimable']
        tokenNft_claimable_amount = data['claimable_amount']
        tokenNft_links = data['links']

        tokenNFT = TokenNFT(
            tid=tokenNft_id,
            name=tokenNft_name,
            uri=tokenNft_uri,
            mint_max=tokenNft_mint_max,
            mint_limit=tokenNft_mint_limit,
            mint_cur=tokenNft_mint_cur,
            claimable=tokenNft_claimable,
            claimable_amount=tokenNft_claimable_amount,
            links=tokenNft_links,
        )
            
        try:
            tokenNFT.save()
        except Exception as e:
            print(f"Err: {e}")
            return Response([{"message": e}], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(["add token"], status=status.HTTP_200_OK)

    def update_token_nfts(self, request):
        data = request.data
        KEYS = "tid,name,uri,mint_max,mint_limit,mint_cur,claimable_amount,claimable,claimable,links"
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

        try:
            if not TokenNFT.objects.filter(tid=tokenNft_id).exists():
                raise ValueError(f"No matching Token NFT's for id '{tokenNft_id}' found.")
        except Exception as e:
            print(f"Err: {e}")
            return Response([], status=status.HTTP_404_NOT_FOUND)
        tokenNFT = TokenNFT.objects.get(tid=tokenNft_id)

        tokenNFT.name = data['name']
        tokenNFT.uri = data['uri']
        tokenNFT.mint_max = data['mint_max']
        tokenNFT.mint_limit = data['mint_limit']
        tokenNFT.mint_cur = data['mint_cur']
        tokenNFT.claimable = data['claimable']
        tokenNFT.claimable_amount = data['claimable_amount']
        tokenNFT.links = data['links']
            
        try:
            tokenNFT.save()
        except Exception as e:
            print(f"Err: {e}")
            return Response([{"message": e}], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(["updated token"], status=status.HTTP_200_OK)


    def delete_token_nfts(self, request, id):
        try:
            if not TokenNFT.objects.filter(tid=id).exists():
                raise ValueError(f"No matching Token NFT's for id '{id}' found.")
        except Exception as e:
            print(f"Err: {e}")
            return Response([], status=status.HTTP_404_NOT_FOUND)

        tokenNFT = TokenNFT.objects.get(tid=id)
        tokenNFT.delete()
        return Response([], status=status.HTTP_200_OK)

class TokenNFTPublicViewSet(viewsets.ViewSet):
    # permission_classes = (AllowAny,)
    # serializer_class = MyTokenObtainPairSerializer

    # def generate_proof(self, request, id):
    #     return Response({}, status=status.HTTP_200_OK)
    
    def generate_proof(self, c_addr):
        jdata = None
        with open("/api/restapi/token_nfts/proof.json", "r") as f:
            jdata = json.loads(f.read())

        random = Random()
        questions = []
        last = []
        question = None

        # Get 3 questions from the list
        for i in range(3):
            while True:
                rnd = random.randint(0,11)
                data = jdata[rnd]
                if rnd not in last:
                    questions.append((rnd, data))
                    last.append(rnd)
                    break


        # Loop through questions
        mainQuestions = []
        for question in questions:

            i = question[1]['i']
            q = question[1]['q']
            a = question[1]['a']

            # 1
            # get crypto addr, gen 2 rnd nums
            # set addr to true, other false
            if i == 1:
                size = len(c_addr)
                last3 = c_addr[size-3:size]

                a[0]['answer']=last3    # Answer 1
                a[0]['valid']=1         # True
                for n in range(1,3):
                    rndstr =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0','1','2','3','4','5','6','7','8','9','0']
                    random.shuffle(rndstr)
                    last3_fake = rndstr[10:13]
                    if last3 is not last3_fake:
                        a[n]['answer']=''.join(last3_fake)  # Answer other
                        a[n]['valid']=0                     # False
                random.shuffle(a)
                mainQuestions.append((i,q,a))

            # 2
            # get weeknum, gen 2 rnd nums (between 1 and 51, exclude cur)
            # set weeknum to true, other false
            elif i == 2:
                dt = datetime.today()
                week = date(dt.year,dt.month,dt.day).isocalendar()[1]
                min, max = 1, 12
                before, after = 0,0
                if week-1 >= min and week+1 <= max:
                    before = week-1
                    after = week+1
                elif week-1 < min:
                    before = 53
                    after = week+1
                elif week+1 > max:
                    before = week-1
                    after = 1
                
                q = q.replace('<month><day>', f"{dt.month}-{dt.day}")
                a[0]['answer']=before
                a[0]['valid']=0
                a[1]['answer']=week     # Answer 2
                a[1]['valid']=1         # True
                a[2]['answer']=after
                a[2]['valid']=0
                random.shuffle(a)
                mainQuestions.append((i,q,a))

            # 7
            # No shuffle
            elif i == 7:
                mainQuestions.append((i,q,a))
            # Pick rnd month, find correct sign, gen 2 rnd signs (exclude cur)  
            elif i ==  10:
                all_zodiac_signs = [(120, 'capricorn'), (218, 'aquarius'), (320, 'pisces'), (420, 'aries'), (521, 'taurus'),
                    (621, 'gemini'), (722, 'cancer'), (823, 'leo'), (923, 'virgo'), (1023, 'libra'),
                    (1122, 'scorpio'), (1222, 'sagittarius'), (1231, 'capricorn')]
                
                history = []
                zodiac_sign = None
                for n in range(3):
                    found = False
                    while not found:
                        day, month = random.randint(1,28), random.randint(1,12)
                        date_number = int("".join((str(month), '%02d' % int(day))))
                        for z in all_zodiac_signs:
                            if date_number <= z[0]:
                                zodiac_sign = z[1]
                                if zodiac_sign not in history:
                                    if n == 0:
                                        a[n]['answer'] = zodiac_sign    # Answer n
                                        q = q.replace('<month><day>', f"{month}-{day}")
                                        a[n]['valid'] = 1           # True
                                    else:
                                        a[n]['answer'] = zodiac_sign    # Answer n
                                        a[n]['valid'] = 0
                                    history.append(zodiac_sign)
                                    found = True
                                    break
                random.shuffle(a)
                mainQuestions.append((i,q,a))

            # 11
            elif i == 11:
                num1 = random.randint(500,1000)
                num2 = random.randint(10,100)
                objs = ["protons", "neutrons", "electrons", "atoms"]
                math = "divided"
                solution = num1 / num2
                q = q.replace('<num1>', str(num1))
                q = q.replace('<num2>', str(num2))
                q = q.replace('<objs>', str(objs[random.randint(0, len(objs)-1)]))
                q = q.replace('<math>', math)
                a[0]['answer']="around "+str(int(solution))
                a[0]['valid']=1
                a[1]['answer']="around "+str(int(solution-(random.randint(1,4))))
                a[1]['valid']=0
                a[2]['answer']="around "+str(int(solution+(random.randint(1,8))))
                a[2]['valid']=0
                mainQuestions.append((i,q,a))

            # Other
            else:
                if i != 1 and i != 2:
                    random.shuffle(a)
                    mainQuestions.append((i,q,a))
        
        # List to send to user
        sendQuestions = []
        sendAnswers = []

        # List with correct answers to generate proof (not for user)
        validAnswers = []

        for question in mainQuestions:
            for ans in question[2]:
                sendAnswers.append(ans['answer'])
                if ans['valid'] == True:
                    validAnswers.append((question[0], ans['answer']))
            sendQuestions.append((question[1], sendAnswers))
            sendAnswers = []

        # Merge all valid answers + solver addr
        valid = f"{c_addr}{validAnswers[0][1]}{validAnswers[1][1]}{validAnswers[2][1]}".replace(" ", "")
        valid = ''.join(valid).strip()

        # Create proof
        crypt = hashlib.sha256()
        crypt.update(str.encode(valid))
        proof = crypt.hexdigest()

        return sendQuestions, proof

    def validate_proof(self, c_addr, proof_user, proof_cached):

        # Only exactly 3 questions, else proof might be invalid
        if len(proof_user) != 3:
            return False

        # Merge all valid answers + solver addr
        proof = f"{c_addr}{proof_user[0]}{proof_user[1]}{proof_user[2]}".replace(" ", "")
        proof = ''.join(proof).strip()

        # Create proof
        crypt = hashlib.sha256()
        crypt.update(str.encode(proof))
        proof = crypt.hexdigest()

        if proof != proof_cached:
            return False
        return True


    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

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

    def claim_request(self, request, id):
        account = self.request.data.get('account')
        if not isinstance(id, str):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        sign_message = f"Welcome to MetaBrainz!\n\n\
            Sign this message to collect your claim '{id}'\n\n\
            note: No blockchain transactions are triggered during this process.\n\n\
            subject: Claim token\n\
            token: {id}\n\
            sign_id: "
        if account is not None:
            # validate user
            if Account.validate_account(c_addr=account):

                sendQuestions, proof = self.generate_proof(account)
                response = Session.setup_claim_response(account, sign_message, proof, sendQuestions)
                return Response(response, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
   
    def claim_token_nfts(self, request, id):
        jdata = request.data
        account = jdata['account']

        response = {"message": "", "token": "" }

        # Retrieve user from db
        user = Account.get_account(account)
        if user:

            # Get from user request
            signature_user = jdata['signature']
            proof_user = jdata["proof"]

            # Get from cache
            setup_claim_cache = cache.get(account)
            signature_cached = setup_claim_cache["message"]
            proof_cached = setup_claim_cache["proof"]
            cache.delete(account)

            # Restore user credentials
            message = encode_defunct(text=signature_cached)
            recovered = None
            try:
                recovered = w3.eth.account.recover_message(message, signature=signature_user)
            except:
                print("Err: Invalid signature")

            if recovered is not None:
                if str(account).lower() == str(recovered).lower():
                    # NOTE: Only generate jwt token after a successfull signed login
                    
                    # Serialize new token
                    token_serializer = MyTokenObtainPairSerializer()
                    jwtToken = token_serializer.get_user_token(user)
                    response = {"token": jwtToken, "message":"success"}

                    # Check proof before further processing claim
                    if not self.validate_proof(account, proof_user, proof_cached):
                        response = { "message":"One of the answers were invalid!", "token": jwtToken}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)

                    # Link user token claim
                    try:
                        if not TokenNFT.objects.filter(tid=id).exists():
                            raise ValueError(f"No matching MetaGear for '{id}' found!")
                    except Exception as e:
                        response = { "message":e, "token": jwtToken}
                        return Response(response, status=status.HTTP_404_NOT_FOUND)

                    tokenNFT = TokenNFT.objects.get(tid=id)
                    if not tokenNFT.claimable:
                        err = f"MetaGear '{id}' not claimable!"
                        response = { "message":err, "token": jwtToken}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    tokenNFT.quantity = tokenNFT.quantity - 1
                    if tokenNFT.quantity == 0:
                        tokenNFT.claimable = False
                    tokenNFT.save()


                    unique_id = account+str(datetime.now())
                    crypt = hashlib.sha256()
                    crypt.update(str.encode(unique_id))
                    claim_id = crypt.hexdigest()
                    ip = self.get_client_ip(request)

                    tokenClaims = TokenClaims(
                        claim_id=claim_id,
                        token_id=tokenNFT,
                        c_addr=str(account).lower(),
                        ip_address=ip
                    )
                    
                    if user.claims:
                        claims = user.claims
                        claims.append(claim_id)
                        user.claims = claims
                    else:
                        user.claims = [claim_id]
                    
                    try:
                        tokenClaims.save()
                        user.save()
                    except IntegrityError:
                        response = { "message":"Token already claimed!", "token": jwtToken}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)

                    except Exception:
                        response = { "message":"Could not claim token!", "token": jwtToken}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    
                    response = { "message":"success", "token": jwtToken}
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {"message": "Expected account did not match!", "token": "" }
            else:
                response = {"message": "Could not recover account!", "token": "" }
        else:
            response = {"message": "No such user!", "token": "" }

        return Response(response, status=status.HTTP_401_UNAUTHORIZED)