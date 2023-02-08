from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from calendarDash.models import DashboardHRD, CalendarDashHRD
from .serializers import DashboardHrdSerializers, CalendarDashSerializers
from django.db.models import Count, Q, Sum

class DashboardTopAPIView(viewsets.ModelViewSet):
    serializer_class = DashboardHrdSerializers

    def get_queryset(self):
        dashboards = DashboardHRD.objects.all().order_by('-id')
        return dashboards

    def get(self, request):
        id = request.query_params['id']
        if id != None:
            dash = DashboardHRD.objects(id=id)
            serializer = DashboardHrdSerializers
        else:
            dash = self.get_queryset()
            serializer = DashboardHrdSerializers(dash, many=True)

        return Response(serializer.data)

class CalendarAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarDashSerializers

    def get_queryset(self):
        calendarHr = CalendarDashHRD.objects.all().order_by('-id')
        return calendarHr
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                calendarHr = CalendarDashHRD.objects(id=ids)
                serializer = CalendarDashSerializers(calendarHr)
        else:
            pett = self.get_queryset()
            serr = CalendarDashSerializers(pett, many=True)
        return Response(serializer.data)

class CalendarAPIView(APIView):
    serializer_class = DashboardHrdSerializers

    def get_queryset(self):
        petitions = CalendarDashHRD.objects.all().order_by('-id')
        return petitions

    def get(self, request, *args, **kwargs):
        querySet = CalendarDashHRD.objects.all().order_by('-id')
        
        employee_name = self.request.query_params.get('employee_name', None)
        working_date = self.request.query_params.get('working_date', None)
        months = self.request.query_params.get('months', None)
        years = self.request.query_params.get('years', None)

        if employee_name:
            querySet=querySet.filter(employee_name=employee_name)
        if years:
            querySet=querySet.filter(years=years)
        if months:
            querySet=months.filter(months=months)
        if working_date:
            querySet=querySet.filter(working_date=working_date)

        serializer = DashboardHrdSerializers(querySet, many=True)

        return Response(serializer.data) 

class WeekTotals(APIView):
    serializer_class = CalendarDashSerializers

    def get(self, request):
        # total_karyawan = CalendarDashHRD.objects.values('is_active').annotate(count=Count('is_active')).order_by('pk')
        week = CalendarDashHRD.objects.all()
        day_of_total = week.count()
        week_of_total = CalendarDashHRD.objects.aggregate(
            weekend=Count("day_of", filter=Q(day_of='weekend')),
            weekday=Count("day_of", filter=Q(day_of='weekday')),
        )

        # case = CalendarDashHRD.objects.aggregate(
        #     weekend=filter(day_of='weekend'),
        #     weekday=filter(day_of='weekday'),
        # )
        case_weekend = CalendarDashHRD.objects.filter(day_of__contains='weekend')
        serializer_weekend = CalendarDashSerializers(case_weekend, many=True)

        case_weekday = CalendarDashHRD.objects.filter(day_of__contains='weekday')
        serializer_weekday = CalendarDashSerializers(case_weekday, many=True)
                # return Response(serializer.data) 

        # case = CalendarDashHRD.objects.all().aggregate(Sum('working_hour'))

        return Response({"message" : "WeekDay and WeekEnd", 
                         "weeks" : week_of_total,
                         "day_of_total" : day_of_total,
                         "weekday" : serializer_weekday.data,
                         "weekend" : serializer_weekend.data,
                         })
                         