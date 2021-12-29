from enum import unique
from django.db import models
from jsonfield import JSONField


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
    descr = models.CharField(
        verbose_name='description of the nft',
        max_length=256,
        unique=False,
        null=True
    )
    attributes =  models.JSONField(
        verbose_name='attributes of the nft',
        unique=False,
        null=True
    )
    quantity = models.IntegerField(
        verbose_name='how many there are available for claim or sale'
    )
    links = models.JSONField(
        verbose_name='references to online sources of the nft',
        unique=False,
        null=True
    )
    img_src =  models.CharField(
        verbose_name='location of the tmp image',
        max_length=128,
        unique=False,
        null=True
    )
    claimable = models.BooleanField(
        verbose_name='is the token claimable? (e.g. airdrop)',
        default=False
    )