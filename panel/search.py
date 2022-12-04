from django.contrib.auth.models import User

def searchUser(param):
	if param is not None:
		if User.objects.filter(first_name__icontains=param).exists():
			data=User.objects.filter(first_name__icontains=param).order_by("-id")
			return data
		elif User.objects.filter(last_name__icontains=param).exists():
			data=User.objects.filter(last_name__icontains=param).order_by("-id")
			return data
		elif  User.objects.filter(email__icontains=param).exists():
			data=User.objects.filter(email__icontains=param).order_by("-id")
			return data
		elif User.objects.filter(username__icontains=param).exists():
			data=User.objects.filter(username__icontains=param).order_by("-id")
			return data
		elif User.objects.filter(extendedauthuser__phone__icontains=param).exists():
			data=User.objects.filter(extendedauthuser__phone__icontains=param).order_by("-id")
			return data
		else:
			return None
	return None