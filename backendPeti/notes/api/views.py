from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializer import NotesSerializer, EmployeeCutiSerializer
from notes.models import NotesHrd, EmployeeCuti
from userapp.models import User

class NotesAPIView(APIView):
    serializer_class = NotesSerializer

    def get_queryset(self):
        notes = NotesHrd.objects.all().order_by('-id')
        return notes
    
    def get(self, request, *args, **kwargs):
        querySet = NotesHrd.objects.all().order_by('-id')
        
        employee_name = self.request.query_params.get('employee_name', None)
        notes = self.request.query_params.get('notes', None)
        date_note = self.request.query_params.get('date_note', None)
        day = self.request.query_params.get('day', None)
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)

        if employee_name:
            querySet=querySet.filter(employee_name=employee_name)
        if date_note:
            querySet=querySet.filter(date_note=date_note)
        if notes:
            querySet=querySet.filter(notes=notes)
        if day:
            querySet=querySet.filter(day=day)
        if month:
            querySet=querySet.filter(month=month)
        if year:
            querySet=querySet.filter(year=year)

        serializer = NotesSerializer(querySet, many=True)

        return Response(serializer.data) 
    

class NotesAPIVIEWID(viewsets.ModelViewSet):
    serializer_class = NotesSerializer

    def get_queryset(self):
        notes = NotesHrd.objects.all().order_by('-id')
        return notes
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                notes = NotesHrd.objects(id=ids)
                serializer = NotesSerializer(notes)
        else:
            pett = self.get_queryset()
            employee_name = self.request.query_params.get('employee_name', None)
            notes = self.request.query_params.get('notes', None)
            date_note = self.request.query_params.get('date_note', None)
            if employee_name:
                querySet=querySet.filter(employee_name=employee_name)
            if date_note:
                querySet=querySet.filter(date_note=date_note)
            if notes:
                querySet=querySet.filter(notes=notes)
            serializer = NotesSerializer(pett, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        notes_data = request.data
        empl = notes_data.get("employee_name")
        datn = notes_data.get("date_note")
        noted = notes_data.get("notes")

        if(empl != '' and datn != '' and noted != ''):
            new_notes = NotesHrd.objects.create(employee_name=notes_data['employee_name'], notes=notes_data['notes'], 
                            date_note=notes_data['date_note'])
            new_notes.save()
            serializer = NotesSerializer(new_notes)
            response_message={"message" : "Catatan Berhasil dibuat",
                                "data": serializer.data
                }
            return Response(response_message)
        else:
            return Response({"error" : "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)
            
    
    def destroy(self, request, *args, **kwargs):
        logedin_user = request.user.roles
        if(logedin_user == "hrd"):
            pengajuan = self.get_object()
            pengajuan.delete()
            response_message={"message" : "Notes has been deleted"}
        else:
            response_message={"message" : "Not Allowed"}

        return Response(response_message)

class NotesEmployeeCuti(viewsets.ModelViewSet):
    serializer_class = EmployeeCutiSerializer

    def get_queryset(self):
        notes = EmployeeCuti.objects.all().order_by('-id')
        return notes

    def get(self, request, *args, **kwargs):
        querySet = EmployeeCuti.objects.all().order_by('-id')
        
        employee_name = self.request.query_params.get('employee_name', None)
        date_note = self.request.query_params.get('date_note', None)
        notes = self.request.query_params.get('notes', None)

        if employee_name:
            querySet=querySet.filter(employee_name=employee_name)
        if notes:
            querySet=querySet.filter(notes=notes)
        if date_note:
            querySet=querySet.filter(date_note=date_note)
    
        serializer = EmployeeCutiSerializer(querySet, many=True)

        return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        notes_data = request.data
        new_notes = EmployeeCuti.objects.create(employee_name=User.objects.get(id=notes_data['employee_name']), jatah_cuti=notes_data['jatah_cuti'], 
                        date_note=notes_data['date_note'], notes=notes_data['notes'])
        if not new_notes :
            return Response({"error" : "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            new_notes.save()
        serializer = EmployeeCutiSerializer(new_notes)
        return Response(serializer.data)
    
    # def put(self, request, *args, **kwargs):
    #     notes_object = EmployeeCuti.objects.get()
    #     data = request.data

    #     notes_object.employee_name = User.objects.get(id=data['employee_name'])
    #     notes_object.jatah_cuti = data['jatah_cuti']
    #     notes_object.sisa_cuti = data['sisa_cuti']
    #     notes_object.tanggal_cuti = data['tanggal_cuti']
    #     notes_object.start_date = data['start_date']
    #     notes_object.end_date = data['end_date']
    #     notes_object.catatan = data['catatan']

    #     notes_object.save()

    #     serializer = EmployeeCutiSerializer(notes_object)
    #     return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        logedin_user = request.user.roles
        if(logedin_user == "hrd"):
            pengajuan = self.get_object()
            pengajuan.delete()
            response_message={"message" : "Data has been deleted"}
        else:
            response_message={"message" : "Not Alloweds"}

        return Response(response_message)