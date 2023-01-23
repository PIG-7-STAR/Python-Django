from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.db.models import Count, Q
from userapp.serializer import UserDetailsSerializer, UserRolesSerializers, UserTotalDataIOSerializers, UserDivisionSerializers
from userapp.models import User, UserRoles, UserDivision
import json
from django.http import HttpResponse
from django.db.models import Sum
from attendanceEmployee.models import AttendanceEmployee

class UserApiView(APIView):
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users
    
    def get(self, request):
        id = request.query_params['id']
        if id != None:
            userprofiles = User.objects(id=id)
            serializer = UserDetailsSerializer
        else:
            userprofiles = self.get_queryset()
            serializer = UserDetailsSerializer(userprofiles, many=True)

        return Response(serializer.data)

class UserViewId(viewsets.ModelViewSet):
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        notes = User.objects.all()
        return notes
    
    def get_ids(self, request, *args, **kwargs):
        ids = request.query_params["id"]
        if ids != None:
                notes = User.objects(id=ids)
                serializer = UserDetailsSerializer(notes)
        else:
            pett = self.get_queryset()
            serr = UserDetailsSerializer(pett, many=True)
        return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        users = request.data
        password1 = users.get("password1")
        password2 = users.get("password2")

        if(password1 == password2 ):
            user_regist = User.objects.create(username=users['username'], first_name=users['first_name'], 
                    last_name=users['last_name'], name=users['name'],  sisa_cuti=users['sisa_cuti'], 
                    roles=users['roles'], division=users['division'])
            serializer = UserDetailsSerializer(user_regist)
            response_message={"message" : "User Berhasil dibuat",
                            "data": serializer.data
            }
            user_regist.save()
            ressPon = Response(response_message)
        else:
            ressPon = Response({"message" : "password harus sama"}, status=status.HTTP_400_BAD_REQUEST)  
        
        return ressPon

class UserRole(viewsets.ModelViewSet):
    serializer_class = UserRolesSerializers

    def get_queryset(self):
        notes = UserRoles.objects.all()
        return notes

class UserDivisionView(viewsets.ModelViewSet):
    serializer_class = UserDivisionSerializers

    def get_queryset(self):
        division = UserDivision.objects.all()
        return division


class UserTotal(APIView):
    serializer_class = UserTotalDataIOSerializers

    def get(self, request):
        # total_karyawan = User.objects.values('is_active').annotate(count=Count('is_active')).order_by('pk')
        userAct = User.objects.all()
        total_karyawan_all = userAct.count()
        total_karyawan = User.objects.aggregate(
            active_employee=Count("is_active", filter=Q(is_active=True)),
            inactive_employee=Count("is_active", filter=Q(is_active=False)),
        )

        case = AttendanceEmployee.objects.all().aggregate(Sum('working_hour'))

        return Response({"Message" : "List Employee", 
                         "employee" : total_karyawan,
                         "total_employee" : total_karyawan_all,
                         "total_work_hour_all" : case,
                         })

class UserSearch(APIView):
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        users = User.objects.all().order_by('-id')
        return users
    
    def get(self, request, *args, **kwargs):
        querySet = User.objects.all().order_by('-id')
        
        name = self.request.query_params.get('name', None)
        roles = self.request.query_params.get('roles', None)
        division = self.request.query_params.get('division', None)

        if name:
            querySet=querySet.filter(name__contains=name)
        if roles:
            querySet=querySet.filter(roles__contains=roles)
        if division:
            querySet=querySet.filter(division__contains=division)

        serializer = UserDetailsSerializer(querySet, many=True)

        return Response(serializer.data) 

class UserSearchView(APIView):
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        users = User.objects.all().order_by('username')
        return users
    
    def get(self, request, *args, **kwargs):
        querySet = User.objects.all().order_by('username')
        
        name = self.request.query_params.get('name', None)

        if name:
            querySet=querySet.filter(name__contains=name)

        serializer = UserDetailsSerializer(querySet, many=True)

        return Response(serializer.data) 