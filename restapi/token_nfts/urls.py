from django.urls import path
from token_nfts.views import(
    TokenNFTPrivateViewSet,
    TokenNFTPublicViewSet,
)

urlpatterns = [
    path('p/asset/<str:id>', TokenNFTPrivateViewSet.as_view({
        'get': 'get_token_nfts',
    })),
    path('p/del_asset/<str:id>', TokenNFTPrivateViewSet.as_view({
        'delete': 'delete_token_nfts',
    })),
    path('p/add_asset', TokenNFTPrivateViewSet.as_view({
        'post': 'add_token_nfts',
    })),
    path('asset/<str:id>', TokenNFTPublicViewSet.as_view({
        'get': 'get_token_nfts',
    })),
    path('all_assets', TokenNFTPublicViewSet.as_view({
        'get': 'get_all_token_nfts',
    })),
    path('claim_request/<str:c_addr>', TokenNFTPublicViewSet.as_view({
        'get': 'claim_request',
    })),
    path('claim_asset/<str:id>', TokenNFTPublicViewSet.as_view({
        'post': 'claim_token_nfts',
    })),
]