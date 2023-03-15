from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from presenceEmployee.models import PresenceEmployee

from userapp.models import User
from .serializer import SubmissionSerializer, SubmissionCutiCalendarSerializer
from submisssion.models import Submission, CalendarCutiSubmission
from datetime import datetime, timedelta

class SubmissionAPIView(APIView):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        petitions = Submission.objects.all().order_by('-updated_at')
        return petitions
    
    def get(self, request, *args, **kwargs):
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
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        petitions = Submission.objects.all().order_by('-updated_at')
        employee = self.request.query_params.get('employee', None)
        permission_type = self.request.query_params.get('permission_type', None)
        permission_pil = self.request.query_params.get('permission_pil', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if employee:
            petitions=petitions.filter(employee__name__contains=employee)
        if end_date:
            petitions=petitions.filter(end_date__contains=end_date)
        if start_date:
            petitions=petitions.filter(start_date__contains=start_date)
        if permission_type:
            petitions=petitions.filter(permission_type__contains=permission_type)
        if permission_pil:
            petitions=petitions.filter(permission_pil__contains=permission_pil)

        # serializer = SubmissionSerializer(petitions, many=True)

        # return Response(serializer.data) 
        return petitions
    
    def get(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                petitions = Submission.objects(id=ids)
                serializer = SubmissionSerializer(petitions)
        else:
            pett = self.get_queryset()
            serr = SubmissionSerializer(pett, many=True)
        return Response(serializer.data)
    
    
    def create(self, request, *args, **kwargs):
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
        submission_obj.end_date = data['end_date']
        submission_obj.return_date = data['return_date']
        submission_obj.jumlah_hari = data['jumlah_hari']
        if(submission_obj.from_hour != None and submission_obj.end_hour != None):
            submission_obj.from_hour = data['from_hour']
            submission_obj.end_hour = data['end_hour']
        if(submission_obj.permission_pil != ''):
            submission_obj.permission_pil = data['permission_pil']
        if(submission_obj.reason_rejected != None and submission_obj.conditional_reasons != None):
            submission_obj.reason_rejected = data['reason_rejected']
            submission_obj.conditional_reasons = data['conditional_reasons']
        if(submission_obj.suspended_start != None and submission_obj.suspended_end != None):
            submission_obj.suspended_start = data['suspended_start']
            submission_obj.suspended_end = data['suspended_end']

        if(submission_obj.permission_pil == 'disetujui'):
             if(submission_obj.status_submission == False):
                 new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=data["employee"]), working_date= submission_obj.start_date,
                                                       lembur_end=data['end_hour'], lembur_start=data['from_hour']
                                                       )
                 new_presen.save()

        submission_obj.save()

        serializers = SubmissionSerializer(submission_obj)

        return Response({"message" : "Berhasil",
                                "data": serializers.data})


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
        pengajuan_data = request.data
        strd = pengajuan_data.get("start")
        edrd = pengajuan_data.get("end")
        new_pengajuan = CalendarCutiSubmission.objects.create(title=pengajuan_data['title'], division=pengajuan_data['division'], 
                        permission_type=pengajuan_data['permission_type'], reason=pengajuan_data['reason'],
                        start=pengajuan_data['start'], end=pengajuan_data['end'])
        if(edrd >= strd ):
            new_pengajuan.save()
            serializer = SubmissionCutiCalendarSerializer(new_pengajuan)
            response_message={"message" : "Berhasil Mengajukan pengajuan"}
        else:
            response_message={"message" : "data tanggal akhir tidak boleh kurang dari tanggal awal"}

        return Response(response_message)