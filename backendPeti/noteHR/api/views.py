from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializer import NotesSerializer
from noteHR.models import NotesApp
from userapp.models import User
from presenceEmployee.models import PresenceEmployee
from datetime import datetime


class NotesAPIView(APIView):
    serializer_class = NotesSerializer

    def get_queryset(self):
        notes = NotesApp.objects.all().order_by('-id')
        return notes
    
    def get(self, request, *args, **kwargs):
        querySet = NotesApp.objects.all().order_by('-id')
        
        employee_name = self.request.query_params.get('employee_name', None)
        employee_id = self.request.query_params.get('employee_id', None)
        notes = self.request.query_params.get('notes', None)
        date_note = self.request.query_params.get('date_note', None)
        hari = self.request.query_params.get('hari', None)
        bulan = self.request.query_params.get('bulan', None)
        tahun = self.request.query_params.get('tahun', None)

        if employee_name:
            querySet=querySet.filter(employee__name__icontains=employee_name)
        if employee_id:
            querySet=querySet.filter(employee__id__contains=employee_id)
        if date_note:
            querySet=querySet.filter(date_note=date_note)
        if notes:
            querySet=querySet.filter(notes=notes)
        if hari:
            querySet=querySet.filter(hari=hari)
        if bulan:
            querySet=querySet.filter(bulan=bulan)
        if tahun:
            querySet=querySet.filter(tahun=tahun)

        serializer = NotesSerializer(querySet, many=True)

        return Response(serializer.data) 
    

class NotesAPIVIEWID(viewsets.ModelViewSet):
    serializer_class = NotesSerializer

    def get_queryset(self):
        notes = NotesApp.objects.all().order_by('-id')
        return notes
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                notes = NotesApp.objects(id=ids)
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
    
    def create(self, request, *args, **kwargs):
        notes_data = request.data
        empl = notes_data.get("employee")
        datn = notes_data.get("date_note")
        noted = notes_data.get("notes")
        typ = notes_data.get("type_notes")

        if(empl != '' and datn != '' and noted != ''):
            new_notes = NotesApp.objects.create(employee=User.objects.get(id=notes_data['employee']), notes=notes_data['notes'], type_notes=notes_data['type_notes'],
                            date_note=notes_data['date_note'])
            new_notes.save()
            if(typ == 'masuk'):
                new_presen = PresenceEmployee.objects.create(employee=User.objects.get(id=notes_data["employee"]), working_date=datn,
                                                       end_from=1700, start_from=900, ket=noted
                                                       )
                new_presen.save()
            serializer = NotesSerializer(new_notes)
            response_message={"message" : "Catatan Berhasil dibuat",
                                "data": serializer.data
                }
            return Response(response_message)
        else:
            return Response({"error" : "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        note_object = self.get_object()
        data = request.data

        employee = User.objects.get(id=data["employee"])

        note_object.employee = employee
        note_object.notes = data['notes']
        note_object.type_notes = data['type_notes']
        note_object.date_note = data['date_note']
        note_object.date_notes = datetime.strptime(data['date_note'], '%Y-%m-%d')

        note_object.save()

        serializers = NotesSerializer(note_object)

        return Response(serializers.data)

    def destroy(self, request, *args, **kwargs):
        logedin_user = request.user.roles
        if(logedin_user == "hrd"):
            notesed = self.get_object()
            notesed.delete()
            response_message={"message" : "Notes has been deleted"}
        else:
            response_message={"message" : "Not Allowed"}

        return Response(response_message)
