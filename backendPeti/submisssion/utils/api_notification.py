from datetime import datetime, timedelta
from django.conf import settings
import requests
from submisssion.api.filters import filterhr, filteruser, formatDate

def sendNotificationEmployee(name, permission, jumlahHari, startDate ):
    if(permission != 'lembur'):
        messages = f'Pengajuan {name} perizinan {permission} selama {jumlahHari} hari pada tanggal {formatDate(startDate)}'
    else:
        messages = f'Pengajuan {permission} pada tanggal {formatDate(startDate)}'
    
    user_filter = filterhr(atasan='atasan', hrd='hrd')
    url = 'https://onesignal.com/api/v1/notifications'
    payload = {
        'app_id': settings.ONESIGNAL_APP_ID,
        'headings': {'en':  f'Pengajuan {permission}'},
        'contents': {'en': messages},
        'included_segments': ['Active Users', 'Subscribed Users'],
        "filters": user_filter,
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Basic "+settings.ONESIGNAL_REST_API_KEY,
        "content-type": "application/json"
    }

    responses = requests.post(url, json=payload, headers=headers)
    return responses

def sendNotificationHR(roles, permission, jumlahHari, startDate, employee_id ):
    if(permission != 'lembur'):
        messages = f'Update terbaru dari {roles} untuk Pengajuan perizinan {permission} selama {jumlahHari} hari '
    else:
        messages = f'Update terbaru dari {roles} untuk Pengajuan {permission} pada tanggal {formatDate(startDate)}'
    
    user_filter = filteruser(id=employee_id)
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


def to_365_years(time_today):
    today = datetime.strptime(time_today, '%Y-%m-%d')
    to_365 = today + timedelta(days=365)
    return to_365.strftime('%Y-%m-%d')