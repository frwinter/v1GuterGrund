from django.core.cache import cache
from django.http import JsonResponse

def rate_limit(max_requests=3, timeout=3600):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            ip = request.META.get('REMOTE_ADDR')
            key = f"resend_activation_{ip}"
            
            count = cache.get(key, 0)
            if count >= max_requests:
                return JsonResponse(
                    {'error': 'Zu viele Anfragen. Bitte warten Sie 1 Stunde.'}, 
                    status=429
                )
                
            cache.set(key, count+1, timeout)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator