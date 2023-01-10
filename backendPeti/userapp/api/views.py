from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from userapp.serializer import UserDetailsSerializer, UserRolesSerializers
from userapp.models import User, UserRoles

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
                    roles=users['roles'])
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