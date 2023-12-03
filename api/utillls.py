import requests
from django.http import JsonResponse
import socket
import geolite as geolite

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location(request):
    ip = get_client_ip(request)
    response = requests.get(f'http://ip-api.com/json/{ip}')
    data = response.json()
    return JsonResponse(data)

def is_ip_from_iran(ip_address):
    reader = geolite.reader()
    location = reader.get(ip_address)
    geolite.close()
    if location is not None:
        return location['country']['iso_code']
    return None