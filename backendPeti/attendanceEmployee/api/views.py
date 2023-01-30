from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from attendanceEmployee.models import AttendanceEmployee, PercentageAttendanceEmployee
from .serializers import AttendanceEmployeeSerializers, PercentageAttendanceEmployeeSerializers
from django.db.models import Count, Sum, Q

class AttendanceAPIView(APIView):
    serializer_class = AttendanceEmployeeSerializers

    def get_queryset(self):
        petitions = AttendanceEmployee.objects.all().order_by('-id')
        return petitions

class PercentageAttendanceAPIView(viewsets.ModelViewSet):
    serializer_class = PercentageAttendanceEmployeeSerializers

    def get_queryset(self):
        petitions = PercentageAttendanceEmployee.objects.all().order_by('-id')
        return petitions
    
class AttendanceAPIViewID(viewsets.ModelViewSet):
    serializer_class = AttendanceEmployeeSerializers

    def get_queryset(self):
        petitions = AttendanceEmployee.objects.all().order_by('-id')
        return petitions
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                petitions = AttendanceEmployee.objects(id=ids)
                serializer = AttendanceEmployeeSerializers(petitions)
        else:
            pett = self.get_queryset()
            serr = AttendanceEmployeeSerializers(pett, many=True)
        return Response(serializer.data)

class AttendanceAPISearch(APIView):
    serializer_class = AttendanceEmployeeSerializers

    def get_queryset(self):
        petitions = AttendanceEmployee.objects.all().order_by('-id')
        return petitions

    def get(self, request, *args, **kwargs):
        querySet = AttendanceEmployee.objects.all().order_by('-id')

        employee_name = self.request.query_params.get('employee_name', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)

        if employee_name:
            querySet=querySet.filter(employee_name__contains=employee_name)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=querySet.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        serializer = AttendanceEmployeeSerializers(querySet, many=True)

        return Response(serializer.data) 

class AttendanceAPICompare(APIView):
    serializer_class = AttendanceEmployeeSerializers

    def get_queryset(self):
        petitions = AttendanceEmployee.objects.all().order_by('working_date')
        return petitions

    def get(self, request, *args, **kwargs):
        querySet = AttendanceEmployee.objects.all().order_by('working_date')

        employee_name = self.request.query_params.get('employee_name', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)
        work_date = self.request.query_params.get('work_date', None)
        end_work_date = self.request.query_params.get('end_work_date', None)
        
        if work_date and end_work_date:
            querySet=querySet.filter(working_date__gte=work_date, working_date__lte=end_work_date)
        if employee_name:
            querySet=querySet.filter(employee_name=employee_name)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=querySet.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        serializer = AttendanceEmployeeSerializers(querySet, many=True)

        return Response(serializer.data) 

class TopAttendanceAPIView(APIView):
    serializer_class = AttendanceEmployeeSerializers

    def get(self, request):
        querySet = AttendanceEmployee.objects.values('working_hour').annotate(employee_name=Count('working_hour')).order_by('-employee_name')[:5]
        months = self.request.query_params.get('months', None)
        
        querySet = AttendanceEmployee.objects.all()
        employee_name = self.request.query_params.get('employee_name', None)
        if employee_name:
            querySet=querySet.filter(employee_name=employee_name)
        if months:
            querySet=querySet.filter(months=months)
        
        total_karyawan_all = querySet.count()
        total_karyawan = querySet.aggregate(
            employee_masuk=Count("employee_name", filter=Q(lembur_hour = None)),
            employee_lembur=Count("employee_name", filter=Q(working_hour = None)),
            employee_masuks=Count("employee_name", filter=Q(lembur_hour= None) | Q(working_hour = None)),
        )

        return Response({"Message" : "List Top 5 Employee", 
                         "data" : total_karyawan,
                         "cth" : total_karyawan_all,
                        #  "total" : mda,
                         })
