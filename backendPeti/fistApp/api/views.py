from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from .serializer import PengajuansSerializer
from fistApp.models import  Pengajuans

@api_view()
@permission_classes([AllowAny])
# @permission_classes([IsAuthenticated]) //auth
def fistFunction(request):
    print(request.query_params)
    print(request.query_params['num'])
    number = request.query_params['num']
    new_number = int(number) * 2
    return Response({'message': 'We received ur request', 'result' : new_number})


class PengajuansViewset(viewsets.ModelViewSet):
    serializer_class = PengajuansSerializer

    def get_queryset(self):
        pengajuan_emp = Pengajuans.objects.all()
        return pengajuan_emp
    
    def gets(self, request, *args, **kwargs):
        try: 
            permission_type = request.query_params["permission_type"]
            if permission_type != '':
                petition  = Pengajuans.objects.get(permission_type=permission_type)
                serializer = PengajuansSerializer(petition)
        except:
            petitions = self.get_queryset()
            serializer = PengajuansSerializer(petitions, many=True)

        return Response(serializer.data)

    def get(self, request):
        id = request.query_params['id']
        if id != None:
            pengajuan = Pengajuans.objects(id=id)
            serializer = PengajuansSerializer
        else:
            pengajuan = self.get_queryset()
            serializer = PengajuansSerializer(pengajuan, many=True)

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        pengajuan_data = request.data
        new_pengajuan = Pengajuans.objects.create(employee_name=pengajuan_data['employee_name'], division=pengajuan_data['division'], 
                        permission_type=pengajuan_data['permission_type'], reason=pengajuan_data['reason'], 
                        start_date=pengajuan_data['start_date'], end_date=pengajuan_data['end_date'], return_date=pengajuan_data['return_date'])
        new_pengajuan.save()
        serializer = PengajuansSerializer(new_pengajuan)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        logedin_user = request.user
        # if(logedin_user == "admin"):
        pengajuan = self.get_object()
        pengajuan.delete()
            # response_message={"message" : "Petition has been deleted"}
        # else:
            # response_message={"message" : "Not Allowed"}

        return Response(pengajuan)
    # def retrieve(self, request, *args, **kwargs):
    #     params = kwargs
    #     print(params['pk'])
    #     employee = Pengajuans.objects.filter(permission_type = params['pk'])
    #     serializer = PengajuansSerializer(employee, many=True)
    #     return Response(serializer.data)

   

