from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import SaldoCutiSerializer
from saldoCuti.models import SaldoCuti

class SaldoApiView(APIView):
    serializer_class = SaldoCutiSerializer

    def get_queryset(self):
        petitions = SaldoCuti.objects.all()
        return petitions
    
    def get(self, request, *args, **kwargs):
        querySet = SaldoCuti.objects.all()
        
        saldo_cuti = self.request.query_params.get('saldo_cuti', None)
        sisa_cuti = self.request.query_params.get('sisa_cuti', None)
      
        if saldo_cuti:
            querySet=querySet.filter(saldo_cuti=saldo_cuti)
        if sisa_cuti:
            querySet=querySet.filter(sisa_cuti=sisa_cuti)

        serializer = SaldoCutiSerializer(querySet, many=True)

        return Response(serializer.data) 
    
    def put(self, request, *args, **kwargs):
        pengajuan_data = request.data
        new_pengajuan = SaldoCuti.objects.create(saldo_cuti=pengajuan_data['saldo_cuti'], sisa_cuti=pengajuan_data['sisa_cuti'] )
        new_pengajuan.save()
        serializer = SaldoCutiSerializer(new_pengajuan)
        return Response(serializer.data)