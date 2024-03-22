from .models import Agency,LiasonAgency,Firm,InterrestRateConfig
from .serializers import *
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.db.models import QuerySet
from rest_framework import permissions

class InterrestRateConfigViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated, )
    def get_destination(self,request):

        user = self.request.user        
        if user.is_authenticated:
            origin = user.agency.id
            destination = request.data.get('destination')
            interest=InterrestRateConfig.objects.filter(agency_liason__origin__id=origin,agency_liason__destination__id =destination,status=True)
            # interest=InterrestRateConfig.objects.filter(id=1)
            serializer = InterrestRateConfigSerializer(interest,context={'request': request},many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        
    
    def get_all_destination(self,request):

        user = self.request.user        
        if user.is_authenticated:
            origin = user.agency.id
            interest=InterrestRateConfig.objects.filter(agency_liason__origin__id=origin,status=True)
            # interest=InterrestRateConfig.objects.filter(id=1)
            serializer = InterrestRateConfigSerializer(interest,context={'request': request},many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        