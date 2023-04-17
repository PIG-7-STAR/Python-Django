from django.conf import settings
import requests
from submisssion.api.filters import filterhr, filteruser, formatDate


def sendNotificationEmployee(permission, jumlahHari, startDate ):
    if(permission != 'lembur'):
            messages = f'Pengajuan perizinan untuk {permission} selama {jumlahHari} hari'
    else:
        messages = f'Pengajuan untuk {permission} pada tanggal {formatDate(startDate)}'
    
    user_filter = filterhr(atasan='atasan', hrd='hrd')
    url = 'https://onesignal.com/api/v1/notifications'
    payload = {
        'app_id': settings.ONESIGNAL_APP_ID,
        'headings': {'en':  f'Pengajuan {permission}'},
        'contents': {'en': messages},
        'included_segments': ['Active Users'],
        "filters": user_filter,
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Basic "+settings.ONESIGNAL_REST_API_KEY,
        "content-type": "application/json"
    }

    responses = requests.post(url, json=payload, headers=headers)
    return responses

def sendNotificationHR(permission, jumlahHari, startDate, employee_id, name ):
    if(permission != 'lembur'):
            messages = f'Update terbaru Pengajuan untuk perizinan {permission} selama {jumlahHari} hari '
    else:
        messages = f'Update terbaru untuk Pengajuan {permission} pada tanggal {formatDate(startDate)}'
    
    user_filter = filteruser(pk=employee_id, name=name)
    url = 'https://onesignal.com/api/v1/notifications'
    payload = {
        'app_id': settings.ONESIGNAL_APP_ID,
        'headings': {'en':  f'Pengajuan {permission}'},
        'contents': {'en': messages},
        'included_segments': ['Active Users'],
        "filters": user_filter,
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Basic "+settings.ONESIGNAL_REST_API_KEY,
        "content-type": "application/json"
    }

    responses = requests.post(url, json=payload, headers=headers)
    return responses