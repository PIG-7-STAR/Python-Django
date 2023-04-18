from datetime import datetime

def filteruser(id):
    filters_to_user = [
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
        "key": "employeeRoles", 
        "relation": "=", 
        "value": hrd},
        {
        "operator": "OR"
        }, 
        {
        "field": "tag", 
        "key": "employeeRoles", 
        "relation": "=", 
        "value": atasan
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