from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from presenceEmployee.models import PresenceEmployee
from .serializers import PresenceEmployeeSerializers
from django.db.models import Count, Sum, Q
from userapp.models import User
from rest_framework.pagination import LimitOffsetPagination
from django.db.models.functions import TruncMonth
from datetime import datetime

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
        presence_obj = self.get_object()
        data = request.data
        date = datetime.strptime(data['working_date'], '%Y-%m-%d').date()
       
        employee = User.objects.get(id=data["employee"])

        presence_obj.employee = employee
        presence_obj.working_date = date

        # presence_obj.working_date = datetime.strptime(data['working_date'], '%Y-%m-%d')
        if(presence_obj.start_from):
            presence_obj.start_from = int(data['start_from'])
            presence_obj.end_from = int(data['end_from'])
        if(presence_obj.lembur_start != None):
            presence_obj.lembur_start = data['lembur_start']
            presence_obj.lembur_end = data['lembur_end']
        if(presence_obj.ket != None):
            presence_obj.ket = data['ket']

        presence_obj.save()

        serializers = PresenceEmployeeSerializers(presence_obj)

        return Response(serializers.data)

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

class PresenceStatistik(APIView):
    def get(self, request, year):
        users = self.request.user
        user_dict = {}
        # if(users.roles == 'karyawan'):
        #     presences = PresenceEmployee.objects.filter(working_date__year=year).filter(employee=users.pk)
        # else:
        presences = PresenceEmployee.objects.filter(working_date__year=year)
        for presence in presences:
            user = presence.employee
            month = presence.working_date.strftime('%B')
            if user not in user_dict:
                user_dict[user] = {month: presence.working_hour}
            else:
                if month not in user_dict[user]:
                    user_dict[user][month] = presence.working_hour
                else:
                    if(presence.working_hour != None):
                        user_dict[user][month] += presence.working_hour
                    else:
                        user_dict[user][month] += 0

        total_per_month = {}
        total_asint = {}
        for user, months in user_dict.items():
            for month, working_hour in months.items():
                if month not in total_per_month:
                    total_per_month[month] = working_hour
                    total_asint[month] = working_hour
                else:
                    if(working_hour != None):
                        total_per_month[month] += working_hour
                        total_asint[month] += working_hour
                    else:
                        total_per_month[month] += 0
                        total_asint[month] += 0

        # Mengonversi total_per_month dari menit ke jam:menit
        for month, working_hour in total_per_month.items():
            jam = working_hour // 60
            menit = working_hour % 60
            total_per_month[month] = f"{jam} jam {menit} menit"
            total_asint[month] = jam

        chart_data = [{"month": month, "total_jam": value} for month, value in total_asint.items()]

        return Response({'year': year, 'data': total_per_month, 'chart': chart_data})

class statistikPreview(APIView):

  def get(self, request, year):
        employee_id = self.request.user
        data = []
        for month in range(1, 13):
            if(employee_id.roles == "karyawan"):
                presence_employee_query = PresenceEmployee.objects.filter(working_date__year=year).filter(employee=employee_id.pk).filter(working_date__month=month)
            else:
                presence_employee_query = PresenceEmployee.objects.filter(working_date__year=year).filter(working_date__month=month)
            total_working_hour = presence_employee_query.aggregate(Sum('working_hour'))['working_hour__sum'] or 0
            total_attendance = presence_employee_query.filter(~Q(working_hour=None)).count()
            
            if(employee_id.name != "Kunut Catur"):
                total_hour = 800*total_attendance
            else:
                total_hour = 900*total_attendance

            if total_working_hour % 100 >= 60:
                total_working_hour += 40

            data.append({
                "month": datetime(year, month, 1).strftime("%b"),
                "value": total_working_hour,
                "actual_value": total_hour
            })
        return Response(data)

# class statistikPreviewAktual(APIView):

#   def get(self, request, year):
#         employee_id = self.request.user
#         data = []
#         for month in range(1, 13):
#             if(employee_id.roles == "karyawan"):
#                 presence_employee_query = PresenceEmployee.objects.filter(working_date__year=year).filter(employee=employee_id.pk).filter(working_date__month=month)
#             else:
#                 presence_employee_query = PresenceEmployee.objects.filter(working_date__year=year).filter(working_date__month=month)

#             total_attendance = presence_employee_query.filter(~Q(working_hour=None)).count()
#             if(employee_id.name != "Kunut Catur"):
#                 total_hour = 800*total_attendance
#             else:
#                 total_hour = 900*total_attendance

#             data.append({
#                 "month": datetime(year, month, 1).strftime("%b"),
#                 "value": total_hour
#             })
#         return Response(data)

class PresenceStatistikUser(APIView):
    def get(self, request, year):
        user_attendance = PresenceEmployee.objects.filter(working_date__year=year).annotate(month=TruncMonth('working_date')).values('month', 'employee__name').annotate(total_attendance=Count('id'), total_working=Sum('working_hour')).order_by('month', '-total_working')
        data = {}
        for item in user_attendance:
            month = item['month'].strftime("%B")
            username = item['employee__name']
            total_attendance = item['total_attendance']
            total_working_minutes = item['total_working']
            total_working_hours = total_working_minutes // 60
            total_working_minutes_remainder = total_working_minutes % 60
            total_working_time = f"{total_working_hours} jam {total_working_minutes_remainder} menit"
            print(total_working_minutes) 
            if month in data:
                data[month].append({'employee_name': username, 'total_attendance': total_attendance, 'total_hour': total_working_time})
            else:
                data[month] = [{'employee_name': username, 'total_attendance': total_attendance, 'total_hour': total_working_time}]
        
        return Response(data)
