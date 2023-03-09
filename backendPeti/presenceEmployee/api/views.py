from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from presenceEmployee.models import PresenceEmployee
from .serializers import PresenceEmployeeSerializers
from django.db.models import Count, Sum, Q
from userapp.models import User

class PresenceAPIView(APIView):
    serializer_class = PresenceEmployeeSerializers

    def get_queryset(self):
        presens = PresenceEmployee.objects.all().order_by('-id')
        return presens

class PresenceAPIViewID(viewsets.ModelViewSet):
    serializer_class = PresenceEmployeeSerializers

    def get_queryset(self):
        presences = PresenceEmployee.objects.all().order_by('-id')
        return presences
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                presences = PresenceEmployee.objects(id=ids)
                serializer = PresenceEmployeeSerializers(presences)
        else:
            pett = self.get_queryset()
            serr = PresenceEmployeeSerializers(pett, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        presen = request.data
        wrkdt = presen.get("working_date")
        strfrom = presen.get("start_from")
        lmbrfrom = presen.get("lembur_from")
        if(wrkdt != None):
            if(strfrom or lmbrfrom != None):
                new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=presen["employee"]), working_date=presen["working_date"],
                                                            end_from=presen["end_from"], start_from=presen["start_from"], lembur_start=presen["lembur_start"], 
                                                            lembur_end=presen["lembur_end"],  ket=presen["ket"]
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

class PresenceSearch(APIView):
    serializer_class = PresenceEmployeeSerializers

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