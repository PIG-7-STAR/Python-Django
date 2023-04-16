from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from presenceEmployee.models import PresenceEmployee
from submisssion.api.filters import filterhr, filteruser
from submisssion.utils.api_notification import sendNotificationEmployee, sendNotificationHR

from userapp.models import User
from .serializer import SubmissionEmployeeSerializer, SubmissionSerializer, SubmissionCutiCalendarSerializer
from submisssion.models import Submission, CalendarCutiSubmission
from datetime import datetime

from rest_framework.decorators import api_view
import requests


class SubmissionAPIView(APIView):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        petitions = Submission.objects.all().order_by('-updated_at')
        return petitions
    
    def get(self, request, *args, **kwargs):
        logedin_user = request.user.roles
        if(logedin_user == 'karyawan'):
            querySet = Submission.objects.all().filter(employee = request.user.id).order_by('-updated_at')
        else:
            querySet = Submission.objects.all().order_by('-updated_at')
        employee = self.request.query_params.get('employee', None)
        permission_type = self.request.query_params.get('permission_type', None)
        permission_pil = self.request.query_params.get('permission_pil', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if employee:
            querySet=querySet.filter(employee__name__contains=employee)
        if end_date:
            querySet=querySet.filter(end_date__contains=end_date)
        if start_date:
            querySet=querySet.filter(start_date__contains=start_date)
        if permission_type:
            querySet=querySet.filter(permission_type__contains=permission_type)
        if permission_pil:
            querySet=querySet.filter(permission_pil__contains=permission_pil)

        if(logedin_user == 'karyawan'):
            serializer = SubmissionEmployeeSerializer(querySet, many=True)
        else:
            serializer = SubmissionSerializer(querySet, many=True)
        return Response(serializer.data) 
    
    def post(self, request, *args, **kwargs):
        pengajuan_data = request.data
        start_dat = pengajuan_data.get("start_date")
        edrd = pengajuan_data.get("end_date")
        rdrd = pengajuan_data.get("return_date")
        reason = pengajuan_data.get("reason")
        divisi = pengajuan_data.get("division")
        juml = pengajuan_data.get("jumlah_hari")
        permiss = pengajuan_data.get("permission_type")
        if(edrd >= start_dat and rdrd >= edrd and rdrd >= start_dat ):
            if(reason != '' and divisi != '' and juml != ''):
                if(permiss != 'lembur'):

                    new_pengajuan = Submission.objects.create(employee=User.objects.get(id=pengajuan_data["employee"]), permission_type=pengajuan_data['permission_type'], 
                                                              reason=pengajuan_data['reason'],  jumlah_hari=pengajuan_data['jumlah_hari'], 
                                                                start_date=pengajuan_data['start_date'], end_date=pengajuan_data['end_date'], return_date=pengajuan_data['return_date'], 
                            )
                    serializer = SubmissionSerializer(new_pengajuan)
                    response_message={"message" : "Berhasil Membuat Pengajuan",
                                    "data": serializer.data
                    }
                  
                    new_pengajuan.save()
                    ressPon = Response(response_message)
                
                else:
                    new_pengajuan = Submission.objects.create(employee=User.objects.get(id=pengajuan_data["employee"]), permission_type=pengajuan_data['permission_type'], 
                            reason=pengajuan_data['reason'], start_date=pengajuan_data['start_date'], end_date=pengajuan_data['end_date'], 
                            from_hour=pengajuan_data['from_hour'], end_hour=pengajuan_data['end_hour'], 
                            
                            )
                    serializer = SubmissionSerializer(new_pengajuan)
                    response_message={"message" : "Berhasil Membuat Pengajuan",
                                    "data": serializer.data
                    }
                    new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=pengajuan_data["employee"]), working_date=start_dat,
                                                       end_from=pengajuan_data['end_hour'], start_from=pengajuan_data['from_hour']
                                                       )
                    new_presen.save()
                    new_pengajuan.save()
                    ressPon = Response(response_message)
            else:
                ressPon = Response({"message" : "Isi Semua data"}, status=status.HTTP_400_BAD_REQUEST)  
        else:
            ressPon = Response({"message" : "Data tanggal akhir dan tanggal kembali masuk tidak boleh kurang dari tanggal awal"}, status=status.HTTP_400_BAD_REQUEST)  
        
        return ressPon
    
    def update(self, request, *args, **kwargs):
        submission_obj = self.get_object()
        data = request.data

        employee = User.objects.get(id=data["employee"])

        submission_obj.employee = employee
        submission_obj.permission_type = data['permission_type']
        submission_obj.reason = data['reason']
        submission_obj.start_date = data['start_date']
        submission_obj.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')

        submission_obj.save()

        serializers = SubmissionSerializer(submission_obj)

        return Response(serializers.data)
    

class SubmissionAPIViewID(viewsets.ModelViewSet):
    
    def get_serializer_class(self):
        user = self.request.user
        if user.roles == 'karyawan':
            return SubmissionEmployeeSerializer
        else:
            return SubmissionSerializer
            
    def get_queryset(self):
        users = self.request.user
        if(users.roles == 'karyawan'):
            petitions = Submission.objects.all().filter(employee=users.pk).order_by('-updated_at')
        else:
            petitions = Submission.objects.all().order_by('-updated_at')
        employee_name = self.request.query_params.get('employee_name', None)
        permission_type = self.request.query_params.get('permission_type', None)
        permission_pil = self.request.query_params.get('permission_pil', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if employee_name:
            petitions=petitions.filter(employee__name__contains=employee_name)
        if end_date:
            petitions=petitions.filter(end_date__contains=end_date)
        if start_date:
            petitions=petitions.filter(start_date__contains=start_date)
        if permission_type:
            petitions=petitions.filter(permission_type__contains=permission_type)
        if permission_pil:
            petitions=petitions.filter(permission_pil__contains=permission_pil)

        return petitions
    
    def get(self, request, *args, **kwargs):
        logedin_user = request.user.roles
        if(logedin_user == 'karyawan'):
            querySet = Submission.objects.all().filter(employee = request.user.id).order_by('-updated_at')
        else:
            querySet = Submission.objects.all().order_by('-updated_at')
        employee = self.request.query_params.get('employee', None)
        permission_type = self.request.query_params.get('permission_type', None)
        permission_pil = self.request.query_params.get('permission_pil', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if employee:
            querySet=querySet.filter(employee__name__contains=employee)
        if end_date:
            querySet=querySet.filter(end_date__contains=end_date)
        if start_date:
            querySet=querySet.filter(start_date__contains=start_date)
        if permission_type:
            querySet=querySet.filter(permission_type__contains=permission_type)
        if permission_pil:
            querySet=querySet.filter(permission_pil__contains=permission_pil)

        if(logedin_user == 'karyawan'):
            serializer = SubmissionEmployeeSerializer(querySet, many=True)
        else:
            serializer = SubmissionSerializer(querySet, many=True)
        return Response(serializer.data) 
    
    
    def create(self, request, *args, **kwargs):

        employee_id = request.user.pk
        employee_sc = request.user.sisa_cuti

        pengajuan_data = request.data
        start_dat = pengajuan_data.get("start_date")
        edrd = pengajuan_data.get("end_date")
        rdrd = pengajuan_data.get("return_date")
        reason = pengajuan_data.get("reason")
        juml = pengajuan_data.get("jumlah_hari")
        permiss = pengajuan_data.get("permission_type")
        fromH = pengajuan_data.get("from_hour")
        endH = pengajuan_data.get("end_hour")
        
        responses = sendNotificationEmployee(permission=permiss, jumlahHari=juml, startDate=start_dat)

        if(permiss != 'lembur'):
            if(reason != '' and  juml != ''):
                if(edrd >= start_dat and rdrd >= edrd and rdrd >= start_dat ):
                    validator_submiss = int(employee_sc)-int(juml)
                    if(validator_submiss < 0 and permiss != 'sakit'):
                        ressPon = Response({"message" : "Sisa Cuti Anda tidak mencukupi"}, status=status.HTTP_400_BAD_REQUEST)  
                    else:
                        new_pengajuan = Submission.objects.create(employee=User.objects.get(id=employee_id), permission_type=pengajuan_data['permission_type'], 
                                                              reason=pengajuan_data['reason'],  jumlah_hari=pengajuan_data['jumlah_hari'], 
                                                              start_date=pengajuan_data['start_date'], end_date=pengajuan_data['end_date'], return_date=pengajuan_data['return_date'],
                            )
                        serializer = SubmissionSerializer(new_pengajuan)
                        response_message={"message" : "Berhasil Membuat Pengajuan",
                                        "data": serializer.data, 
                                        'res' : responses.status_code
                        }
                    
                        new_pengajuan.save()
                        ressPon = Response(response_message)    
                else:
                    ressPon = Response({"message" : "Data tanggal akhir dan tanggal kembali masuk tidak boleh kurang dari tanggal awal"}, status=status.HTTP_400_BAD_REQUEST)  
            else:
                ressPon = Response({"message" : "Isi Semua datas"}, status=status.HTTP_400_BAD_REQUEST)  
        else:
            if(reason != '' and fromH != None and endH != None):
                new_pengajuan = Submission.objects.create(employee=User.objects.get(id=employee_id), permission_type=pengajuan_data['permission_type'], 
                        reason=pengajuan_data['reason'], start_date=pengajuan_data['start_date'], end_date=pengajuan_data['start_date'], 
                        from_hour=pengajuan_data['from_hour'], end_hour=pengajuan_data['end_hour'], 
                        
                        )
                serializer = SubmissionSerializer(new_pengajuan)
                response_message={"message" : "Berhasil Membuat Pengajuan",
                                "data": serializer.data,
                                 'res' : responses.status_code
                }
                new_pengajuan.save()
                ressPon = Response(response_message)
            else:
                ressPon = Response({"message" : "Isi Semua data"}, status=status.HTTP_400_BAD_REQUEST)  
        
        return ressPon
    
    def update(self, request, *args, **kwargs):
        logged_user = request.user.roles

        if(logged_user == "hrd" or logged_user == "atasan"):
            submission_obj = self.get_object()
            data = request.data

            permiss = submission_obj.permission_type = data['permission_type']
            juml =  submission_obj.jumlah_hari = data['jumlah_hari']
            start_dat = submission_obj.start_date = data['start_date']

            employee = User.objects.get(id=data["employee"])

            submission_obj.employee = employee
            submission_obj.permission_type = data['permission_type']
            submission_obj.reason = data['reason']
            submission_obj.start_date = data['start_date']
            submission_obj.end_date = data['end_date']
            submission_obj.return_date = data['return_date']
            submission_obj.jumlah_hari = data['jumlah_hari']

            if(submission_obj.from_hour != None and submission_obj.end_hour != None and submission_obj.permission_type == 'lembur'):
                submission_obj.from_hour = data['from_hour']
                submission_obj.end_hour = data['end_hour']
            if(submission_obj.permission_pil != ''):
                submission_obj.permission_pil = data['permission_pil']
                if(submission_obj.permission_pil == 'ditolak'):
                    if(submission_obj.reason_rejected != None and submission_obj.conditional_reasons != None):
                        submission_obj.reason_rejected = data['reason_rejected']
                        submission_obj.conditional_reasons = data['conditional_reasons']
                elif(submission_obj.permission_pil == 'ditangguhkan'):
                    if(submission_obj.suspended_start != None and submission_obj.suspended_end != None):
                        submission_obj.suspended_start = data['suspended_start']
                        submission_obj.suspended_end = data['suspended_end']
                elif(submission_obj.permission_pil == 'disetujui'):
                    if(submission_obj.status_submission == False):
                        if(submission_obj.permission_type == 'lembur'):
                            new_presen = PresenceEmployee.objects.create(employee=employee, working_date= submission_obj.start_date,
                                                            lembur_end=data['end_hour'], lembur_start=data['from_hour']
                                                            )
                            new_presen.save()
                        elif(submission_obj.permission_type == 'cuti'):
                            submiss_object = CalendarCutiSubmission.objects.create(employee=employee, 
                                permission_type=data['permission_type'], reason=data['reason'],
                                start=datetime.strptime(data['start_date'], '%Y-%m-%d') , end=datetime.strptime(data['end_date'], '%Y-%m-%d'))
                            users_obj = User.objects.get(id=data["employee"])
                            users_obj.sisa_cuti = int(users_obj.sisa_cuti) - int(submission_obj.jumlah_hari)
                            users_obj.save()
                            submiss_object.save()

            submission_obj.save()
            serializers = SubmissionSerializer(submission_obj)
            responses = sendNotificationHR(permission=permiss, jumlahHari=juml, startDate=start_dat, username=employee.username, name=employee.name)

            res =  Response({"message" : "Berhasil",
                             "response" : responses.status_code, 
                                "data": serializers.data})
        else:
            res = Response({"message" : "Anda tidak dapat melakukannya perizinan ini. silahkan hubungi hrd atau atasan anda",
                                })
        return res
    
    def destroy(self, request, *args, **kwargs):
        logedin_user = request.user
        pengajuan = self.get_object()

        if(pengajuan.permission_pil == 'disetujui'):
            if(logedin_user.roles == "hrd"):
                if(pengajuan.permission_type == 'cuti' or pengajuan.permission_type == 'ijin'):
                    users_obj = User.objects.get(id=pengajuan.employee.pk)
                    users_obj.sisa_cuti = int(users_obj.sisa_cuti) + int(pengajuan.jumlah_hari)
                    users_obj.save()
                pengajuan.delete()
                response_message = Response({"message" : "Berhasil menghapus pengajuan"}, status=status.HTTP_200_OK)  
            else:
                response_message = Response({"message" : "Hanya HRD yang diperbolehkan menghapus"}, status=status.HTTP_400_BAD_REQUEST)  
        else:
            if(logedin_user.pk == pengajuan.employee.pk):
                if(pengajuan.permission_pil == None):
                    pengajuan.delete()
                    response_message = Response({"message" : "Berhasil menghapus pengajuan"}, status=status.HTTP_200_OK)  
                else:
                    response_message = Response({"message" : "Tidak dapat menghapus pengajuan"}, status=status.HTTP_400_BAD_REQUEST)  

        return response_message


class SubmissionCalendarAPI(viewsets.ModelViewSet):
    serializer_class = SubmissionCutiCalendarSerializer

    def get_queryset(self):
        petitions = CalendarCutiSubmission.objects.all().order_by('-id')
        return petitions
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                petitions = CalendarCutiSubmission.objects(id=ids)
                serializer = SubmissionCutiCalendarSerializer(petitions)
        else:
            pett = self.get_queryset()
            serr = SubmissionCutiCalendarSerializer(pett, many=True)
        return Response(serializer.data)
    
    def get_name(self, request, *args, **kwargs):
        ids = request.query_params["title"]
        if ids != None:
                petitions = CalendarCutiSubmission.objects(title=ids)
                serializer = SubmissionCutiCalendarSerializer(petitions)
        else:
            pett = self.get_queryset()
            serr = SubmissionCutiCalendarSerializer(pett, many=True)
        return Response(serializer.data)

    
    def post(self, request, *args, **kwargs):
        submiss_data = request.data
        strd = submiss_data.get("start")
        edrd = submiss_data.get("end")
        submiss_obj = CalendarCutiSubmission.objects.create(title=submiss_data['title'], division=submiss_data['division'], 
                        permission_type=submiss_data['permission_type'], reason=submiss_data['reason'],
                        start=submiss_data['start'], end=submiss_data['end'])
        if(edrd >= strd ):
            submiss_obj.save()
            serializer = SubmissionCutiCalendarSerializer(submiss_obj)
            response_message={"message" : "Berhasil Mengajukan pengajuan"}
        else:
            response_message={"message" : "data tanggal akhir tidak boleh kurang dari tanggal awal"}

        return Response(response_message)
    
@api_view(['POST'])
def send_notification_api(request):

    user_type = request.user.roles
    if(user_type == 'karyawan'):
        user_filter = filterhr(atasan='atasan', hrd='hrd')
    else:
        username = request.user.username
        name = request.user.name
        user_filter = filteruser(username=username, name=name)

    try:
        title = request.data['title']
        message = request.data['message']
        url = 'https://onesignal.com/api/v1/notifications'
        
        payload = {
            'app_id': settings.ONESIGNAL_APP_ID,
            'contents': {'en': message},
            'headings': {'en': title},
            'included_segments': ['Active Users'],
            "filters": user_filter,
        }

        headers = {
            "accept": "application/json",
            "Authorization": "Basic "+settings.ONESIGNAL_REST_API_KEY,
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            print(response)
            return Response({
                "message" : "Notifikasi Berhasil dikirim",
                "data" : {
                    "title_notification" : title,
                    "message_notification" : message,
                }}, status=status.HTTP_200_OK)  
        else:
            return HttpResponse('Gagal mengirim notifikasi')

    except Exception as e:
        return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)