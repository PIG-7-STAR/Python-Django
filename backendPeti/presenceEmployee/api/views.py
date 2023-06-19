from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from presenceEmployee.models import PresenceEmployee
from .serializers import PresenceEmployeeSerializers
from django.db.models import Count, Q, Sum
from userapp.models import User
from rest_framework.pagination import LimitOffsetPagination
from django.db.models.functions import TruncMonth
from datetime import datetime
import calendar
from collections import defaultdict


class PresenceAPIView(APIView):
    serializer_class = PresenceEmployeeSerializers
 
    def get_queryset(self):
        presens = PresenceEmployee.objects.all().order_by('-id')
        return presens

class PresenceAPIViewID(viewsets.ModelViewSet):
    serializer_class = PresenceEmployeeSerializers
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        users = self.request.user
        if(users.roles == "hrd"):
            querySet = PresenceEmployee.objects.all().order_by('-id')
        else:
            querySet = PresenceEmployee.objects.all().filter(employee=users.pk).order_by('-id')
        employee = self.request.query_params.get('employee', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)

        if employee:
            querySet=querySet.filter(employee__name__icontains=employee)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=querySet.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        # serializer = PresenceEmployeeSerializers(querySet)

        # return serializer.data
        return querySet
    
    def get_id(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                presences = PresenceEmployee.objects(id=ids)
                serializer = PresenceEmployeeSerializers(presences)
        else:
            pett = self.get_queryset()
            serr = PresenceEmployeeSerializers(pett, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        presen = request.data
        wrkdt = presen.get("working_date")
        strfrom = presen.get("start_from")
        lmbrstr = presen.get("lembur_start")
        employee = User.objects.get(id=presen["employee"])
        date = datetime.strptime(wrkdt, '%Y-%m-%d').date()

        if PresenceEmployee.objects.filter(Q(employee=employee) & Q(working_date=wrkdt)).exists():
            res = Response({"message" : "Sudah ada data absensi yang sama"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if(wrkdt != None):
                if(strfrom and lmbrstr != None):
                    new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=presen["employee"]), working_date=date,
                                                                end_from=int(presen["end_from"]), start_from=int(presen["start_from"]), lembur_start=int(presen["lembur_start"]), 
                                                                lembur_end=int(presen["lembur_end"]),  ket=presen["ket"]
                                                                )
                    serializer = PresenceEmployeeSerializers(new_presen)
                    response_message={"message" : "Berhasil membuat data",
                                        "data": serializer.data
                        }
                    new_presen.save()
                    res = Response(response_message)
                elif(strfrom != None):
                    new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=presen["employee"]), working_date=date,
                                                                end_from=int(presen["end_from"]), start_from=int(presen["start_from"]),  ket=presen["ket"]
                                                                )
                    serializer = PresenceEmployeeSerializers(new_presen)
                    response_message={"message" : "Berhasil membuat data",
                                        "data": serializer.data
                        }
                    new_presen.save()
                    res = Response(response_message)
                elif(lmbrstr != None):
                    new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=presen["employee"]), working_date=date,
                                                                lembur_start=int(presen["lembur_start"]), lembur_end=int(presen["lembur_end"]),  ket=presen["ket"]
                                                                )
                    serializer = PresenceEmployeeSerializers(new_presen)
                    response_message={"message" : "Berhasil membuat data",
                                        "data": serializer.data
                        }
                    new_presen.save()
                    res = Response(response_message)
                else:
                    res = Response({"message" : "Isi Semua data"}, status=status.HTTP_400_BAD_REQUEST)
        return res
    
    def update(self, request, *args, **kwargs):
        logged_in = request.user.roles
        if(logged_in == 'hrd'):
            data = request.data
            if data:
                presence_obj = self.get_object()
                date = datetime.strptime(data['working_date'], '%Y-%m-%d').date()

                employee = User.objects.get(id=data["employee"])

                presence_obj.employee = employee
                presence_obj.working_date = date

                if 'start_from' in data:
                    presence_obj.start_from = int(data.get('start_from'))
                    presence_obj.end_from = int(data.get('end_from'))

                if 'lembur_start' in data:
                    presence_obj.lembur_start = int(data.get('lembur_start'))
                    presence_obj.lembur_end = int(data.get('lembur_end'))
                    print(presence_obj.lembur_start)

                if 'ket' in data:
                    presence_obj.ket = data.get('ket')

                print("hi")
                print(presence_obj.lembur_end)
                presence_obj.save()
                res = Response({'message' : 'Data berhasil disimpan'})
            else:
                res = Response({'message' : 'Isikan data yang di perlukan'})
        else:
            res = Response({'message' : 'Anda bukan HR, untuk mengeditnya silahkan ke HR terlebih dahulu'})

        return res

class PresenceSearch(APIView):
    serializer_class = PresenceEmployeeSerializers
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        presence_emp = PresenceEmployee.objects.all().order_by('-id')
        return presence_emp

    def get(self, request, *args, **kwargs):
        querySet = PresenceEmployee.objects.all().order_by('-id')
        employee = self.request.query_params.get('employee', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)

        if employee:
            querySet=querySet.filter(employee__name__contains=employee)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=querySet.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        serializer = PresenceEmployeeSerializers(querySet, many=True)

        return Response(serializer.data) 

class PresenceAPICompare(APIView):
    serializer_class = PresenceEmployeeSerializers
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        petitions = PresenceEmployee.objects.all().order_by('working_date')
        return petitions

    def get(self, request, *args, **kwargs):
        querySet = PresenceEmployee.objects.all().order_by('working_date')

        employee = self.request.query_params.get('employee', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)
        work_date = self.request.query_params.get('work_date', None)
        end_work_date = self.request.query_params.get('end_work_date', None)
        
        if work_date and end_work_date:
            querySet=querySet.filter(working_date__gte=work_date, working_date__lte=end_work_date)
        if employee:
            querySet=querySet.filter(employee__pk=employee)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=querySet.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        serializer = PresenceEmployeeSerializers(querySet, many=True)

        return Response(serializer.data) 

class PresenceAPIAnalisis(APIView):
    serializer_class = PresenceEmployeeSerializers

    def get_queryset(self):
        petitions = PresenceEmployee.objects.all().order_by('working_date')
        return petitions

    def get(self, request, *args, **kwargs):
        users = request.user
        if(users.roles == "hrd"):
            querySet = PresenceEmployee.objects.all().order_by('working_date')
        else:
            querySet = PresenceEmployee.objects.all().filter(employee=users.pk).order_by('working_date')

        employee = self.request.query_params.get('employee', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)

        if employee:
            querySet=querySet.filter(employee__pk=employee)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=querySet.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        serializer = PresenceEmployeeSerializers(querySet, many=True)

        return Response(serializer.data) 

class TopPresenceAPIView(APIView):
    serializer_class = PresenceEmployeeSerializers

    def get(self, request):
        querySet = PresenceEmployee.objects.values('working_hour').annotate(employee__pk=Count('working_hour')).order_by('-employee__pk')[:5]
        months = self.request.query_params.get('months', None)
        
        querySet = PresenceEmployee.objects.all()
        employee = self.request.query_params.get('employee', None)
        if employee:
            querySet=querySet.filter(employee__pk=employee)
        if months:
            querySet=querySet.filter(months=months)
        
        total_karyawan_all = querySet.count()
        total_karyawan = querySet.aggregate(
            employee_masuk=Count("employee__pk", filter=Q(lembur_hour = None)),
            employee_lembur=Count("employee__pk", filter=Q(working_hour = None)),
            employee_masuks=Count("employee__pk", filter=Q(lembur_hour= None) | Q(working_hour = None)),
        )

        return Response({ 
                         "data" : total_karyawan,
                         "cth" : total_karyawan_all,
                         })

class PresenceStatistikUser(APIView):
    def get(self, request, month, year, *args, **kwargs):
        user_attendance = (
            PresenceEmployee.objects
            .filter(working_date__year=year, working_date__month=month, working_hour__isnull=False)
            .values('employee__name')
            .annotate(total_attendance=Count('id'))
            .order_by('total_attendance')
        )
        
        result = [
            {item['employee__name']: item['total_attendance']}
            for item in user_attendance
        ]
        
        return Response(result)

class StatistikPresenceInMonth(APIView):
    def get(self, request, year):
        log_user = self.request.user
        if log_user.roles == 'hrd':
            presence_data = PresenceEmployee.objects.annotate(
                month=TruncMonth('working_date')
            ).filter(working_hour__isnull=False, working_date__year=year).values('month').annotate(
                count=Count('id')
            ).order_by('month')
        else:
            presence_data = PresenceEmployee.objects.annotate(
                month=TruncMonth('working_date')
            ).filter(employee=log_user.pk, working_hour__isnull=False, working_date__year=year).values('month').annotate(
                count=Count('id')
            ).order_by('month')
        
        result = [
            {item['month'].strftime('%b'): item['count']} for item in presence_data
        ]
        
        return Response(result)


class StatistikSubmissionEmployeeInMonth(APIView):
    def get(self, request, year):
        user_log = self.request.user
        if user_log.roles == 'hrd':
            presence_data = PresenceEmployee.objects.all().filter(working_date__year=year)
        else:
            presence_data = PresenceEmployee.objects.all().filter(working_date__year=year, employee=user_log.pk)
        
        # if user_log.roles == 'hrd':
        #     result = {
        #         month_abbr: {
        #                 "masuk": PresenceEmployee.objects.filter(working_date__year=year, working_date__month=month_num, working_hour__isnull=False).count(),
        #                 "tidak masuk": 0,
        #                 "sakit": 0,
        #                 "izin": 0,
        #                 "cuti": 0
        #             } for month_num, month_abbr in enumerate(calendar.month_abbr[1:], start=1)
        #         }
        # else:
        #     result = {
        #         month_abbr: {
        #                 "masuk": PresenceEmployee.objects.filter(employee=user_log.pk, working_date__year=year, working_date__month=month_num, working_hour__isnull=False).count(),
        #                 "tidak masuk": 0,
        #                 "sakit": 0,
        #                 "izin": 0,
        #                 "cuti": 0
        #             } for month_num, month_abbr in enumerate(calendar.month_abbr[1:], start=1)
        #         }
        result = {
            month_abbr: {
                "tidak masuk": 0,
                "sakit": 0,
                "izin": 0,
                "cuti": 0
            } for month_abbr in calendar.month_abbr[1:]
        }
        
        for presence in presence_data:
            month = calendar.month_abbr[presence.working_date.month]  
            ket = presence.ket
            
            if ket in result[month]:
                result[month][ket] += 1
        
        return Response(result)