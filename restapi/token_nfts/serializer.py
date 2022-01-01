from rest_framework import serializers
from token_nfts.models import TokenNFT

class TokenNFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenNFT
        fields = (
            'tid',
            'name', 
            'descr',
            'attributes', 
            'quantity',
            'img_src',
            'claimable',
            'links'
        )