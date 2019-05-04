from django.core.signing import TimestampSigner,SignatureExpired,BadSignature

signer = TimestampSigner(salt='extra') # 加盐