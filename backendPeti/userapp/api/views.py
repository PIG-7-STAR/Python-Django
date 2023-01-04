from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from userapp.serializer import UserDetailsSerializer
from userapp.models import User

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
        