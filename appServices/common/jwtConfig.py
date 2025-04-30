from datetime import timedelta

JWT_SECRET_KEY = "django-insecure-w7q2=jy0k#82vt*uzbeotbz$b#8(u#crbn*uznh_36^-i5hv+p"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_LIFETIME = timedelta(minutes=30)
JWT_REFRESH_TOKEN_LIFETIME = timedelta(days=7) 