from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from calendarDash.models import DashboardHRD, CalendarDashHRD
from .serializers import DashboardHrdSerializers, CalendarDashSerializers

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