from django.core.cache import cache

from accounts.models import Roles, UserAccount
from accounts.serializers import UserAccountSerializer

import os, re, uuid, hashlib, time
from random import Random

class Account:

    def validate_account(c_addr):
        try:
            if(not UserAccount.objects.filter(c_addr=c_addr).exists()):
                raise ValueError(f"validate_account(): Could not find user: '{c_addr}'")
        except Exception as e:
            print(f"Err: {e}")
            return False
        return True

    def create_account(c_addr):
        try:
            roles = Roles.objects.all()
            for role in roles:
                if not role.is_admin:
                    random = Random()
                    rnd = random.randint(0, 109)
                    user_img_src = f"user_img_{rnd}.png" 
                    UserAccount.objects.create_user(c_addr=c_addr, role_id=role.role_id, img_path=user_img_src)
                    print("Successfully added user.")
        except:
            print("Err: create_account(): Something went wrong, could not create the user.")
            return False
        return True

    def get_account(c_addr):
        # Retrieve user from db
        # FIXME: Catch errs
        try:
            user = UserAccount.objects.get(c_addr=c_addr)
            return user
        except:
            print("Err: get_account(): Could not find user")
        return None

    def destroy_account(c_addr):
        UserAccount.objects.get(c_addr=c_addr).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update_profile(self):
        return "Updated user profile"


class Session:
    def setup_connection_response(c_addr, sign_message):
        # Generate sign sign_message
        sign_id = uuid.uuid1().hex
        sign_message = sign_message+sign_id
        response_data = {"addr": c_addr, "sign_id": sign_message }
        # Tmp store sign_message in cache using the user addr (c_addr)
        cache.set(c_addr, sign_message, 30)
        return response_data

    def setup_claim_response(c_addr, sign_message, proof, sendQuestions):
        # Generate sign sign_message
        sign_id = uuid.uuid1().hex
        sign_message = sign_message+sign_id

        # NOTE: Do NOT send proof back, proof only in cache
        response_data = {"addr": c_addr, "sign_id": sign_message, "questions": sendQuestions }
        
        # Tmp store sign_message in cache for N seconds
        # using the user addr (c_addr)
        MAX_TIME = 60 # 1 Minute to answer 3 questions 
        store = {"proof": proof, "message": sign_message }
        cache.set(c_addr, store, MAX_TIME)
        return response_data

class Profile:
    def create_profile(c_addr):
        pass

    def update_profile(c_addr):
        pass

    def delete_profile(c_addr):
        pass
