from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .token import account_verfication_token


def SendVerificationToken(request, user):
    
    domain = get_current_site(request=request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_verfication_token.make_token(user=user)

    url = f'http://{domain}/accounts/activate/{uidb64}/{token}'

    print('\n\n')
    print(url)
    print('\n\n')