from datetime import datetime

def filteruser(id, name):
    filters_to_user = [
        {
            "field": "tag",
            "key": "name",
            "relation": "=",
            "value": name
        },
        {
            "operator": "AND"
        },
        {
            "field": "tag",
            "key": "employeeId",
            "relation": "=",
            "value": id
        }
    ]
    return filters_to_user

def filterhr(hrd, atasan):
    filters_to_hrd = [
        {
            "field": "tag",
            "key": "roles",
            "relation": "=",
            "value": atasan
        },
        {
            "operator": "OR"
        },
        {
            "field": "tag",
            "key": "roles",
            "relation": "=",
            "value": hrd
        }
    ]
    return filters_to_hrd

def formatDate(tanggal):
    dt = datetime.strptime(tanggal, '%Y-%m-%d')
    hari = dt.strftime('%A')
    nama_bulan = dt.strftime('%B')
    tahun = dt.strftime('%Y')
    tanggal_hasil = f"{hari} {nama_bulan} {tahun}"
    return tanggal_hasil