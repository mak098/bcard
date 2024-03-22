from .serializers import *
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.db.models import QuerySet
from rest_framework import permissions
from Agency.models import InterrestRateConfig

class CashInViewSet(viewsets.ModelViewSet):
    
    queryset = CashIn.objects.all()
    class_serializer = CashInSerializer
    lookup_field = 'code'

    def create(self,request):
        user = self.request.user        
        if user.is_authenticated:
            amount = request.data.get('amount')
            sender = request.data.get('sender')
            sender_phone = request.data.get('sender_phone')
            recipient = request.data.get('recipient')
            recipient_phone = request.data.get('recipient_phone')
            comment = request.data.get('comment')
            origin = user.agency.id
            destination = request.data.get('destination')

            if not InterrestRateConfig.objects.filter(agency_liason__origin__id=origin,agency_liason__destination__id =destination,status=True).exists():
                detail = 'You are not allowed to make this aperation.'
                return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            interrest_config=InterrestRateConfig.objects.get(agency_liason__origin__id=origin,agency_liason__destination__id =destination,status=True)
            interrest ={}
            if amount<=interrest_config.threshold:
                interrest ={"interrest":interrest_config.forfait,"type":"forfaite"}
                amount = amount-interrest_config.forfait
            else:
                interrest ={"interrest":(interrest_config.rate*amount)/100,"type":"pourcentage"}
                amount = amount-((interrest_config.rate*amount)/100)
            cash_in =CashIn.objects.create(
                created_by=user,
                interrest_config=interrest_config,
                amount=amount,
                sender=sender,
                sender_phone=sender_phone,
                recipient=recipient,
                recipient_phone =recipient_phone,
                comment=comment,
                interrest=interrest
            )
            cash_in.save()
            user_id = user.id
            agency_id = user.agency.id
            cash_in.code =transaction_code(user_id,agency_id,cash_in.id)
            cash_in.save()
            serializer = CashInSerializer(cash_in,context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        

    
    def get_with_code(self,request):
        user = self.request.user        
        if user.is_authenticated:
            code = request.data.get("code")
            if not CashIn.objects.filter(code=code).exists():
                return Response({}, status=status.HTTP_202_ACCEPTED)
            cash_in =CashIn.objects.get(code=code) 
            serializer = CashInSerializer(cash_in,context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        


class cashOutViewSet(viewsets.ModelViewSet):
    class_serializer = CashOutSerializer
    
def transaction_code(user_id,agency_id,cashin_id):
    import datetime
    today = datetime.date.today()
    year = today.year
    
    return f'{format_number(user_id)}-{format_number(agency_id)}-{format_number(cashin_id)}-{year}'

def format_number(num):
    if num < 10:
        return "000" + str(num)
    elif num < 100:
        return "00" + str(num)
    elif num < 1000:
        return "0" + str(num)
    else:
        return str(num)
