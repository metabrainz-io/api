from rest_framework import serializers
from token_nfts.models import TokenNFT

class TokenNFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenNFT
        fields = (
            'tid',
            'name',
            'uri',
            'mint_max',
            'mint_limit',
            'mint_cur',
            'claimable',
            'claimable_amount',
            'links'
        )