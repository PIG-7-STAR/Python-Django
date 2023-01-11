from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializer import PetitionsSerializer, PetitionsCalendarSerializer
from pengajuanEmp.models import Petitions, PetitionsCalendar
from datetime import datetime, timedelta

class PengajuanAPIView(APIView):
    serializer_class = PetitionsSerializer

    def get_queryset(self):
        petitions = Petitions.objects.all().order_by('-id')
        return petitions
    
    def get(self, request, *args, **kwargs):
        querySet = Petitions.objects.all().order_by('-id')
        
        employee_name = self.request.query_params.get('employee_name', None)
        permission_type = self.request.query_params.get('permission_type', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if employee_name:
            querySet=querySet.filter(employee_name=employee_name)
        if end_date:
            querySet=querySet.filter(end_date=end_date)
        if start_date:
            querySet=querySet.filter(start_date=start_date)
        if permission_type:
            querySet=querySet.filter(permission_type=permission_type)

        serializer = PetitionsSerializer(querySet, many=True)

        return Response(serializer.data) 
    
    def post(self, request, *args, **kwargs):
        pengajuan_data = request.data
        start_dat = pengajuan_data.get("start_date")
        edrd = pengajuan_data.get("end_date")
        rdrd = pengajuan_data.get("return_date")
        reason = pengajuan_data.get("reason")
        divisi = pengajuan_data.get("division")
        juml = pengajuan_data.get("jumlah_hari")

        if(edrd >= start_dat and rdrd >= edrd and rdrd >= start_dat ):
            if(reason != '' and divisi != '' and juml != ''):
                new_pengajuan = Petitions.objects.create(employee_name=pengajuan_data['employee_name'], employee_id=pengajuan_data['employee_id'], division=pengajuan_data['division'], 
                        permission_type=pengajuan_data['permission_type'], reason=pengajuan_data['reason'],  jumlah_hari=pengajuan_data['jumlah_hari'], 
                        start_date=pengajuan_data['start_date'], end_date=pengajuan_data['end_date'], return_date=pengajuan_data['return_date'])
                serializer = PetitionsSerializer(new_pengajuan)
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
    

class PengajuanAPIViewID(viewsets.ModelViewSet):
    serializer_class = PetitionsSerializer

    def get_queryset(self):
        petitions = Petitions.objects.all().order_by('-id')
        return petitions
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                petitions = Petitions.objects(id=ids)
                serializer = PetitionsSerializer(petitions)
        else:
            pett = self.get_queryset()
            serr = PetitionsSerializer(pett, many=True)
        return Response(serializer.data)
    
    def get_name(self, request, *args, **kwargs):
        ids = request.query_params["employee_name"]
        if ids != None:
                petitions = Petitions.objects(employee_name=ids)
                serializer = PetitionsSerializer(petitions)
        else:
            pett = self.get_queryset()
            serr = PetitionsSerializer(pett, many=True)
        return Response(serializer.data)

    
    def post(self, request, *args, **kwargs):
        pengajuan_data = request.data
        strd = pengajuan_data.get("start_date")
        edrd = pengajuan_data.get("end_date")
        rdrd = pengajuan_data.get("return_date")
        new_pengajuan = Petitions.objects.create(employee_name=pengajuan_data['employee_name'], employee_id=pengajuan_data['employee_id'], division=pengajuan_data['division'], 
                        permission_type=pengajuan_data['permission_type'], reason=pengajuan_data['reason'], jumlah_hari=pengajuan_data['jumlah_hari'], 
                        start_date=pengajuan_data['start_date'], end_date=pengajuan_data['end_date'], return_date=pengajuan_data['return_date'])
        if(edrd >= strd & edrd >= rdrd ):
            new_pengajuan.save()
            serializer = PetitionsSerializer(new_pengajuan)
            response_message={"message" : "Berhasil Mengajukan pengajuan"}
        else:
            response_message={"message" : "data tanggal akhir tidak boleh kurang dari tanggal awal"}

        return Response(response_message)


        # else:
        #     new_pengajuan.save()
        #     serializer = PetitionsSerializer(new_pengajuan)
        #     return Response(serializer.data)
    
    # def put(self, request, *args, **kwargs):
    #     pengajuan_data = request.data
    #     new_pengajuan = Petitions.objects.update( permission_pil= pengajuan_data['permission_pil'], jumlah_hari=pengajuan_data['jumlah_hari'], 
    #                     start_date=pengajuan_data['start_date'], end_date=pengajuan_data['end_date'], return_date=pengajuan_data['return_date'])
    #     new_pengajuan.update()
    #     serializer = PetitionsSerializer(new_pengajuan)
    #     return Response(serializer.data)
    
    # def destroy(self, request, delete_id, *args, **kwargs):
    #     # logedin_user = request.user
    #     response_message={"message" : "Petition has been deleted"}
    #     peng_data = request.data
    #     petti = Petitions.objects.filter(id=delete_id)
    #     petti.delete()
    #     # if(logedin_user == "admin"):
    #     #     pengajuan = self.get_object()
    #     #     pengajuan.delete()
    #     # else:
    #     #     response_message={"message" : "Not Allowed"}

    #     return Response(response_message)

class PengajuanCalendarAPI(viewsets.ModelViewSet):
    serializer_class = PetitionsCalendarSerializer

    def get_queryset(self):
        petitions = PetitionsCalendar.objects.all().order_by('-id')
        return petitions
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                petitions = PetitionsCalendar.objects(id=ids)
                serializer = PetitionsCalendarSerializer(petitions)
        else:
            pett = self.get_queryset()
            serr = PetitionsCalendarSerializer(pett, many=True)
        return Response(serializer.data)
    
    def get_name(self, request, *args, **kwargs):
        ids = request.query_params["title"]
        if ids != None:
                petitions = PetitionsCalendar.objects(title=ids)
                serializer = PetitionsCalendarSerializer(petitions)
        else:
            pett = self.get_queryset()
            serr = PetitionsCalendarSerializer(pett, many=True)
        return Response(serializer.data)

    
    def post(self, request, *args, **kwargs):
        pengajuan_data = request.data
        strd = pengajuan_data.get("start_date")
        edrd = pengajuan_data.get("end_date")
        rdrd = pengajuan_data.get("return_date")
        new_pengajuan = PetitionsCalendar.objects.create(title=pengajuan_data['title'], employee_id=pengajuan_data['employee_id'], division=pengajuan_data['division'], 
                        permission_type=pengajuan_data['permission_type'], reason=pengajuan_data['reason'], jumlah_hari=pengajuan_data['jumlah_hari'], 
                        start_date=pengajuan_data['start_date'], end_date=pengajuan_data['end_date'], return_date=pengajuan_data['return_date'])
        if(edrd >= strd & edrd >= rdrd ):
            new_pengajuan.save()
            serializer = PetitionsCalendarSerializer(new_pengajuan)
            response_message={"message" : "Berhasil Mengajukan pengajuan"}
        else:
            response_message={"message" : "data tanggal akhir tidak boleh kurang dari tanggal awal"}

        return Response(response_message)