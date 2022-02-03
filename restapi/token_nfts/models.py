from enum import unique
from django.db import models
from jsonfield import JSONField

from accounts.models import UserAccount


class TokenNFT(models.Model):
    
    tid = models.IntegerField(
        verbose_name='the token id',
        unique=True,
        null=False
    )
    name = models.CharField(
        verbose_name='name of the nft',
        max_length=128,
        unique=False,
        null=True
    )
    uri =  models.CharField(
        verbose_name='metadata',
        max_length=128,
        unique=False,
        null=True
    )
    mint_max = models.IntegerField(
        verbose_name='max in existence',
        null=True
    )
    mint_limit = models.IntegerField(
        verbose_name='whats the mint limit',
        null=True
    )
    mint_cur = models.IntegerField(
        verbose_name='how many are already minted',
        null=True
    )
    claimable = models.BooleanField(
        verbose_name='is the token claimable? (e.g. airdrop)',
        default=False
    )
    claimable_amount = models.IntegerField(
        verbose_name='how many there are available for claim',
        null=True        
    )
    links = models.JSONField(
        verbose_name='references to other nft source if uri fails',
        unique=False,
        null=True
    )

# class Claim(models.Model):
#     claim

class TokenClaims(models.Model):
    class Meta:
        unique_together = (('token_id', 'c_addr'),)
    claim_id = models.CharField(
        verbose_name='the claim id',
        unique=True,
        null=False,
        max_length=64
    )
    token_id = models.ForeignKey(
        TokenNFT,
        on_delete=models.CASCADE,
    )
    c_addr = models.CharField(
        verbose_name='crypto address',
        max_length=42,
        unique=False,
    )
    ip_address = models.CharField(
        verbose_name='logged user ip address',
        max_length=45,
        unique=False,
        null=True
    )