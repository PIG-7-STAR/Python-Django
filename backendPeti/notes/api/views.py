from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .serializer import NotesSerializer
from notes.models import NotesHrd

class NotesAPIView(APIView):
    serializer_class = NotesSerializer

    def get_queryset(self):
        notes = NotesHrd.objects.all()
        return notes
    
    # def get(self, request, *args, **kwargs):
    #     try: 
    #         sisa_cuti = request.query_params["sisa_cuti"]
    #         if sisa_cuti != ' ':
    #             petition  = NotesHrd.objects.get(sisa_cuti=sisa_cuti)
    #             serializer = NotesSerializer(petition)
    #     except:
    #         notes = self.get_queryset()
    #         serializer = NotesSerializer(notes, many=True)

    #     return Response(serializer.data)
    
    # def get_ids(self, request, *args, **kwargs):
    #     ids = request.query_params["id"]
    #     try:
    #         if ids != None:
    #             notes = NotesHrd.objects(id=ids)
    #             serializer = NotesSerializer(notes)
    #     except:
    #         pett = self.get_queryset()
    #         serr = NotesSerializer(pett, many=True)
    #     return Response(serializer.data)
    
    # def post(self, request, *args, **kwargs):
    #     notes_data = request.data
    #     new_notes = NotesHrd.objects.create(employee_name=notes_data['employee_name'], jatah_cuti=notes_data['jatah_cuti'], 
    #                     sisa_cuti=notes_data['sisa_cuti'], tanggal_cuti=notes_data['tanggal_cuti'], 
    #                     start_date=notes_data['start_date'], end_date=notes_data['end_date'])
    #     new_notes.save()
    #     serializer = NotesSerializer(new_notes)
    #     return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        querySet = NotesHrd.objects.all()
        
        employee_name = self.request.query_params.get('employee_name', None)
        jatah_cuti = self.request.query_params.get('jatah_cuti', None)
        tanggal_cuti = self.request.query_params.get('tanggal_cuti', None)
        sisa_cuti = self.request.query_params.get('sisa_cuti', None)

        if employee_name:
            querySet=querySet.filter(employee_name=employee_name)
        if sisa_cuti:
            querySet=querySet.filter(sisa_cuti=sisa_cuti)
        if tanggal_cuti:
            querySet=querySet.filter(tanggal_cuti=tanggal_cuti)
        if jatah_cuti:
            querySet=querySet.filter(jatah_cuti=jatah_cuti)
    
        serializer = NotesSerializer(querySet, many=True)

        return Response(serializer.data) 
    

class NotesAPIVIEWID(viewsets.ModelViewSet):
    serializer_class = NotesSerializer

    def get_queryset(self):
        notes = NotesHrd.objects.all()
        return notes
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                notes = NotesHrd.objects(id=ids)
                serializer = NotesSerializer(notes)
        else:
            pett = self.get_queryset()
            serr = NotesSerializer(pett, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        notes_data = request.data
        new_notes = NotesHrd.objects.create(employee_name=notes_data['employee_name'], jatah_cuti=notes_data['jatah_cuti'], 
                        sisa_cuti=notes_data['sisa_cuti'], tanggal_cuti=notes_data['tanggal_cuti'], 
                        start_date=notes_data['start_date'], end_date=notes_data['end_date'])
        new_notes.save()
        serializer = NotesSerializer(new_notes)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        logedin_user = request.user
        # if(logedin_user == "admin"):
        pengajuan = self.get_object()
        pengajuan.delete()
        response_message={"message" : "Notes has been deleted"}
        # else:
            # response_message={"message" : "Not Allowed"}

        return Response(response_message)