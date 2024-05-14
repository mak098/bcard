from .serializers import *
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.db.models import QuerySet
from rest_framework import permissions
from Agency.models import InterrestRateConfig
from rest_framework.decorators import action
from datetime import datetime, timedelta,date
from django.utils import timezone
today_date = timezone.localdate()
from django.utils.timezone import make_aware
from django.core.paginator import Paginator

class CashInViewSet(viewsets.ModelViewSet):
    
    serializer_class = CashInSerializer
    queryset = CashIn.objects.all()

    def create(self,request):
       
        user = self.request.user              
        if user.is_authenticated:
            amount = request.data.get('amount')
            sender = request.data.get('sender')
            sender_phone = request.data.get('sender_phone')
            recipient = request.data.get('recipient')
            recipient_phone = request.data.get('recipient_phone')
            comment = request.data.get('comment')
            sender_id_or_passport = request.data.get('sender_id_or_passport')
            recipient_id_or_passport = request.data.get('recipient_id_or_passport')
            origin = user.agency.id
            destination = request.data.get('destination')
            if not isinstance(amount, (int, float, complex)) and not isinstance(amount, bool):
                detail = 'the amount must be a number.'
                return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)
            

            if not InterrestRateConfig.objects.filter(agency_liason__origin__id=origin,agency_liason__destination__id =destination,status=True).exists():
                detail = 'Transaction not authorized. Please check the destination agency.'
                return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            interrest_config=InterrestRateConfig.objects.get(agency_liason__origin__id=origin,agency_liason__destination__id =destination,status=True)
            distribution ={}
            if amount<=interrest_config.threshold:
                amount_to_be_received = amount-interrest_config.forfait
                distribution ={
                    "amount_to_be_received":amount_to_be_received,
                    "interrest":interrest_config.forfait,
                    "type":"forfaite"
                }
                
            else:
                amount_to_be_received = amount-((interrest_config.rate*amount)/100)
                distribution ={
                    "amount_to_be_received":amount_to_be_received,
                    "interrest":(interrest_config.rate*amount)/100,
                    "type":"pourcentage"
                }
                
            cash_in =CashIn.objects.create(
                created_by=user,
                interrest_config=interrest_config,
                amount=amount,
                sender=sender,
                sender_phone=sender_phone,
                recipient=recipient,
                recipient_phone =recipient_phone,
                comment=comment,
                sender_id_or_passport=sender_id_or_passport,
                recipient_id_or_passport=recipient_id_or_passport,
                distribution=distribution
            )
            cash_in.save()
            code = generer_code(origin,destination)
            cash_in.code =code
            cash_in.save()
            serializer = CashInSerializer(cash_in,context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        

    @action(detail=False, methods=['get'], url_path='get/(?P<code>\w+)')
    def get_with_code(self,request,code=None):        
        user = self.request.user        
        if user.is_authenticated:
            if not CashIn.objects.filter(code=code).exists():
                return Response({}, status=status.HTTP_202_ACCEPTED)
            cash_in =CashIn.objects.get(code=code) 
            serializer = CashInSerializer(cash_in,context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        

    
    @action(detail=False, methods=['get'], url_path='today')
    def today(self,request):
        user = self.request.user        
        if user.is_authenticated:
            user_agency = user.agency
            start_of_today = datetime.combine(today_date, datetime.min.time())
            end_of_today = datetime.combine(today_date, datetime.max.time())
            cashin = CashIn.objects.filter(created_at__range=[make_aware(start_of_today), make_aware(end_of_today)],created_by__agency=user_agency).order_by('created_at')
            page_position,limit=1,5
            if 'position' and 'limit'   in request.query_params:
                
                page_position = request.query_params.get('position')
                limit =request.query_params.get('limit')
                if page_position =='' or page_position==0 or page_position=="0":
                    page_position =1
                if limit =='' or limit==0 or limit=="0":
                    limit =5
            p = Paginator(cashin, int(limit))
            number_of_rows = p.count
            number_of_pages = p.num_pages
            if int(page_position)>number_of_pages:
                page_position =number_of_pages
            page_data = p.page(int(page_position))
            paginations ={
                'number_of_rows':number_of_rows,
                'number_of_pages':number_of_pages,
                'page_position':int(page_position),
                'limit':int(limit)
            }

            serializer = CashInSerializer(page_data,context={'request': request},many=True)
            return Response({"data":serializer.data,"paginator":paginations}, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        

    @action(detail=False, methods=['get'], url_path='week')
    def week(self,request):
        user = self.request.user        
        if user.is_authenticated:
            user_agency = user.agency
            today_date = datetime.now()
            # Calculate the start of the current week (assuming Monday is the start of the week)
            start_of_week = today_date - timedelta(days=today_date.weekday())
            # Calculate the end of the current week
            end_of_week = start_of_week + timedelta(days=6)
            cashin = CashIn.objects.filter(created_at__date__range=[make_aware(start_of_week), make_aware(end_of_week)],created_by__agency=user_agency).order_by('created_at')
            page_position,limit=1,5
            if 'position' and 'limit'   in request.query_params:
                
                page_position = request.query_params.get('position')
                limit =request.query_params.get('limit')
                if page_position =='' or page_position==0 or page_position=="0":
                    page_position =1
                if limit =='' or limit==0 or limit=="0":
                    limit =5
            p = Paginator(cashin, int(limit))
            number_of_rows = p.count
            number_of_pages = p.num_pages
            if int(page_position)>number_of_pages:
                page_position =number_of_pages
            page_data = p.page(int(page_position))
            paginations ={
                'number_of_rows':number_of_rows,
                'number_of_pages':number_of_pages,
                'page_position':int(page_position),
                'limit':int(limit)
            }


            serializer = CashInSerializer(page_data,context={'request': request},many=True)
            return Response({"data":serializer.data,"paginator":paginations}, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        

    @action(detail=False, methods=['get'], url_path='month')
    def month(self,request):
        user = self.request.user        
        if user.is_authenticated:
            user_agency =user.agency
            current_date = datetime.now()
            # Get the first day of the current month
            first_day_of_month = current_date.replace(day=1)
            # Get the last day of the current month
            last_day_of_month = first_day_of_month.replace(month=first_day_of_month.month % 12 + 1, day=1) - timedelta(days=1)

            cashin = CashIn.objects.filter(created_at__range=[make_aware(first_day_of_month), make_aware(last_day_of_month)],created_by__agency=user_agency).order_by('created_at')
            page_position,limit=1,5
            if 'position' and 'limit'   in request.query_params:
                
                page_position = request.query_params.get('position')
                limit =request.query_params.get('limit')
                if page_position =='' or page_position==0 or page_position=="0":
                    page_position =1
                if limit =='' or limit==0 or limit=="0":
                    limit =5
            p = Paginator(cashin, int(limit))
            number_of_rows = p.count
            number_of_pages = p.num_pages
            if int(page_position)>number_of_pages:
                page_position =number_of_pages
            page_data = p.page(int(page_position))
            paginations ={
                'number_of_rows':number_of_rows,
                'number_of_pages':number_of_pages,
                'page_position':int(page_position),
                'limit':int(limit)
            }

            serializer = CashInSerializer(page_data,context={'request': request},many=True)
            return Response({"data":serializer.data,"paginator":paginations}, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        

    @action(detail=False, methods=['get'], url_path='year')
    def year(self,request):

        user = self.request.user        
        if user.is_authenticated:
            user_agency=user.agency
            current_year = datetime.now().year
            # Get the first day of the current year
            first_day_of_year = datetime(current_year, 1, 1)
            # Get the last day of the current year
            last_day_of_year = datetime(current_year, 12, 31)
            cashin = CashIn.objects.filter(created_at__range=[make_aware(first_day_of_year), make_aware(last_day_of_year)],created_by__agency=user_agency).order_by('created_at')
            page_position,limit=1,5
            if 'position' and 'limit'   in request.query_params:
                
                page_position = request.query_params.get('position')
                limit =request.query_params.get('limit')
                if page_position =='' or page_position==0 or page_position=="0":
                    page_position =1
                if limit =='' or limit==0 or limit=="0":
                    limit =5
            p = Paginator(cashin, int(limit))
            number_of_rows = p.count
            number_of_pages = p.num_pages
            if int(page_position)>number_of_pages:
                page_position =number_of_pages
            page_data = p.page(int(page_position))
            paginations ={
                'number_of_rows':number_of_rows,
                'number_of_pages':number_of_pages,
                'page_position':int(page_position),
                'limit':int(limit)
            }

            serializer = CashInSerializer(page_data,context={'request': request},many=True)
            return Response({"data":serializer.data,"paginator":paginations}, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        

    @action(detail=False, methods=['get'], url_path='personalized_date')
    def personalized_date(self, request, start_date=datetime.now().date, end_date=datetime.now().date):
        user = self.request.user        
        if user.is_authenticated:
            user_agency = user.agency
            cashin={}
            if 'start_date' and 'end_date'  not in request.query_params:
                cashin = CashIn.objects.filter(created_by__agency=user_agency).order_by('created_at')               
            else:
                start_date =request.query_params.get('start_date')
                end_date =request.query_params.get('end_date')
            
                try:                
                    _start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))          
                    _end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
                    cashin = CashIn.objects.filter(created_at__range=[_start_date, _end_date],created_by__agency=user_agency).order_by('created_at')
                except Exception as e:
                    detail = 'Start  or end date arror'
                    return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)
            page_position,limit=1,5
            if 'position' and 'limit'   in request.query_params:
                
                page_position = request.query_params.get('position')
                limit =request.query_params.get('limit')
                if page_position =='' or page_position==0 or page_position=="0":
                    page_position =1
                if limit =='' or limit==0 or limit=="0":
                    limit =5
            p = Paginator(cashin, int(limit))
            number_of_rows = p.count
            number_of_pages = p.num_pages
            if int(page_position)>number_of_pages:
                page_position =number_of_pages
            page_data = p.page(int(page_position))
            paginations ={
                'number_of_rows':number_of_rows,
                'number_of_pages':number_of_pages,
                'page_position':int(page_position),
                'limit':int(limit)
            }

            serializer = CashInSerializer(page_data,context={'request': request},many=True)
            return Response({"data":serializer.data,"paginator":paginations}, status=status.HTTP_202_ACCEPTED)
            
            
            
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        

class cashOutViewSet(viewsets.ModelViewSet):
    serializer_class = CashOutSerializer
    queryset = CashOut.objects.all()
    def out(self,request):
        user = self.request.user        
        if user.is_authenticated:
            code = request.data.get('code')
            amount = request.data.get('amount')
            recipient = request.data.get("recipient")
            recipient_phone = request.data.get("recipient_phone")
            comment = request.data.get("comment")
            recipient_id_or_passport = request.data.get("recipient_id_or_passport")
            
            if not isinstance(amount, (int, float, complex)) and not isinstance(amount, bool):
                detail = 'the amount must be a number.'
                return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)
             
            if not CashIn.objects.filter(code=code).exists():
                detail = "Ce code de transaction n'existe pas"
                return Response({'detail': detail}, status=status.HTTP_400_ACCEPTED)
           
            cashin = CashIn.objects.get(code=code)

            load_transfer_distribution = cashin.distribution
            
            if load_transfer_distribution['amount_to_be_received'] < amount :
                detail = 'Le montant que vous voulez retirer est superieur a celui qui a été envoyé'
                return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if CashOut.objects.filter(cash_in__code=code).exists():
                
                if cashin.status==True:
                    detail ='Desolé le retrait est dèja effectué'
                    return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)
                
                get_cashout = CashOut.objects.filter(cash_in__code=code)
                out_amount = 0                
                for element in get_cashout:
                    out_amount += element.amount
                    
                
                if out_amount +amount> load_transfer_distribution['amount_to_be_received']:
                    detail =f"Desolé le retrait est dèja effectué a partie il reste un payement de "+str(load_transfer_distribution['amount_to_be_received']-out_amount)
                    return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)

                cashout = CashOut.objects.create(
                    cash_in=cashin,
                    amount= amount,
                    recipient=recipient,
                    recipient_phone=recipient_phone,
                    comment=comment,
                    recipient_id_or_passport=recipient_id_or_passport,
                    created_by = user
                )
                cashout.save()
                if amount == out_amount +amount:
                    cashin.status = True
                    cashin.save()
                serializer = CashOutSerializer(cashout,context={'request': request})
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            
            cashout = CashOut.objects.create(
                    cash_in=cashin,
                    amount= amount,
                    recipient=recipient,
                    recipient_phone=recipient_phone,
                    comment=comment,
                    recipient_id_or_passport=recipient_id_or_passport,
                    created_by = user
                )
            cashout.save()
            if amount == load_transfer_distribution['amount_to_be_received']:
                    cashin.status = True
                    cashin.save()
            
            serializer = CashOutSerializer(cashout,context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        
    
    @action(detail=False, methods=['get'], url_path='statement')
    def statement(self,request):
        user = self.request.user        
        if user.is_authenticated:
            if 'code' not in request.query_params:
                detail = 'The transaction code are obligatory'
                return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)
            code = request.query_params.get('code')
            get_cashout = CashOut.objects.filter(cash_in__code=code)
            page_position,limit=1,5
            if 'position' and 'limit'   in request.query_params:
                
                page_position = request.query_params.get('position')
                limit =request.query_params.get('limit')
                if page_position =='' or page_position==0 or page_position=="0":
                    page_position =1
                if limit =='' or limit==0 or limit=="0":
                    limit =5
            p = Paginator(get_cashout, int(limit))
            number_of_rows = p.count
            number_of_pages = p.num_pages
            if int(page_position)>number_of_pages:
                page_position =number_of_pages
            page_data = p.page(int(page_position))
            paginations ={
                'number_of_rows':number_of_rows,
                'number_of_pages':number_of_pages,
                'page_position':int(page_position),
                'limit':int(limit)
            }

            serializer = CashOutSerializer(page_data,context={'request': request},many=True)
            return Response({"data":serializer.data,"paginator":paginations}, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        
    
    @action(detail=False, methods=['get'], url_path='today')
    def today(self,request): 
        user = self.request.user        
        if user.is_authenticated:
            user_agency = user.agency
            start_of_today = datetime.combine(today_date, datetime.min.time())
            end_of_today = datetime.combine(today_date, datetime.max.time())            
            get_cashout = CashOut.objects.filter(created_at__range=[make_aware(start_of_today), make_aware(end_of_today)],created_by__agency=user_agency)
            
            page_position,limit=1,5
            if 'position' and 'limit'   in request.query_params:
                
                page_position = request.query_params.get('position')
                limit =request.query_params.get('limit')
                if page_position =='' or page_position==0 or page_position=="0":
                    page_position =1
                if limit =='' or limit==0 or limit=="0":
                    limit =5
            p = Paginator(get_cashout, int(limit))
            number_of_rows = p.count
            number_of_pages = p.num_pages
            if int(page_position)>number_of_pages:
                page_position =number_of_pages
            page_data = p.page(int(page_position))
            paginations ={
                'number_of_rows':number_of_rows,
                'number_of_pages':number_of_pages,
                'page_position':int(page_position),
                'limit':int(limit)
            }

           
            serializer = CashOutSerializer(page_data,context={'request': request},many=True)
            return Response({"data":serializer.data,"paginator":paginations}, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        
    
    @action(detail=False, methods=['get'], url_path='week')
    def week(self,request):
        user = self.request.user        
        if user.is_authenticated:
            user_agency = user.agency
            today_date = datetime.now().date()
            # Calculate the start of the current week (assuming Monday is the start of the week)
            start_of_week = today_date - timedelta(days=today_date.weekday())
            # Calculate the end of the current week
            end_of_week = start_of_week + timedelta(days=6)
            get_cashout = CashOut.objects.filter(created_at__date__range=[make_aware(start_of_week), make_aware(end_of_week)],created_by__agency=user_agency)
            page_position,limit=1,5
            if 'position' and 'limit'   in request.query_params:
                
                page_position = request.query_params.get('position')
                limit =request.query_params.get('limit')
                if page_position =='' or page_position==0 or page_position=="0":
                    page_position =1
                if limit =='' or limit==0 or limit=="0":
                    limit =5
            p = Paginator(get_cashout, int(limit))
            number_of_rows = p.count
            number_of_pages = p.num_pages
            if int(page_position)>number_of_pages:
                page_position =number_of_pages
            page_data = p.page(int(page_position))
            paginations ={
                'number_of_rows':number_of_rows,
                'number_of_pages':number_of_pages,
                'page_position':int(page_position),
                'limit':int(limit)
            }

            serializer = CashOutSerializer(page_data,context={'request': request},many=True)
            return Response({"data":serializer.data,"paginator":paginations}, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        

    @action(detail=False, methods=['get'], url_path='month')
    def month(self,request):
        user = self.request.user        
        if user.is_authenticated:
            user_agency =user.agency
            current_date = datetime.now()
            # Get the first day of the current month
            first_day_of_month = current_date.replace(day=1)
            # Get the last day of the current month
            last_day_of_month = first_day_of_month.replace(month=first_day_of_month.month % 12 + 1, day=1) - timedelta(days=1)

            get_cashout = CashOut.objects.filter(created_at__range=[make_aware(first_day_of_month), make_aware(last_day_of_month)],created_by__agency=user_agency)
            
            page_position,limit=1,5
            if 'position' and 'limit'   in request.query_params:
                
                page_position = request.query_params.get('position')
                limit =request.query_params.get('limit')
                if page_position =='' or page_position==0 or page_position=="0":
                    page_position =1
                if limit =='' or limit==0 or limit=="0":
                    limit =5
            p = Paginator(get_cashout, int(limit))
            number_of_rows = p.count
            number_of_pages = p.num_pages
            if int(page_position)>number_of_pages:
                page_position =number_of_pages
            page_data = p.page(int(page_position))
            paginations ={
                'number_of_rows':number_of_rows,
                'number_of_pages':number_of_pages,
                'page_position':int(page_position),
                'limit':int(limit)
            }
            
            serializer = CashOutSerializer(page_data,context={'request': request},many=True)
            return Response({"data":serializer.data,"paginator":paginations}, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        

    @action(detail=False, methods=['get'], url_path='year')
    def year(self,request):

        user = self.request.user        
        if user.is_authenticated:
            user_agency=user.agency
            current_year = datetime.now().year
            # Get the first day of the current year
            first_day_of_year = datetime(current_year, 1, 1)
            # Get the last day of the current year
            last_day_of_year = datetime(current_year, 12, 31)
            get_cashout = CashOut.objects.filter(created_at__range=[make_aware(first_day_of_year), make_aware(last_day_of_year)],created_by__agency=user_agency)
            page_position,limit=1,5
            if 'position' and 'limit'   in request.query_params:
                
                page_position = request.query_params.get('position')
                limit =request.query_params.get('limit')
                if page_position =='' or page_position==0 or page_position=="0":
                    page_position =1
                if limit =='' or limit==0 or limit=="0":
                    limit =5
            p = Paginator(get_cashout, int(limit))
            number_of_rows = p.count
            number_of_pages = p.num_pages
            if int(page_position)>number_of_pages:
                page_position =number_of_pages
            page_data = p.page(int(page_position))
            paginations ={
                'number_of_rows':number_of_rows,
                'number_of_pages':number_of_pages,
                'page_position':int(page_position),
                'limit':int(limit)
            }

            serializer = CashOutSerializer(page_data,context={'request': request},many=True)
            return Response({"data":serializer.data,"paginator":paginations}, status=status.HTTP_202_ACCEPTED)
            
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        

    @action(detail=False, methods=['get'], url_path='personalized_date')
    def personalized_date(self, request):
        user = self.request.user       
        if user.is_authenticated:
            user_agency = user.agency
            cashout = {}
            if 'start_date' and 'end_date'  not in request.query_params:
                CashOut.objects.filter(created_by__agency=user_agency)
            else:
                start_date =request.query_params.get('start_date')
                end_date =request.query_params.get('end_date')
            
                try:                
                    _start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))          
                    _end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
                    cashout = CashOut.objects.filter(created_at__range=[_start_date, _end_date],created_by__agency=user_agency)
                except Exception as e:
                    detail = 'Start  or end date arror'
                    return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)
            page_position,limit=1,5
            if 'position' and 'limit'   in request.query_params:                
                page_position = request.query_params.get('position')
                limit =request.query_params.get('limit')
                if page_position =='' or page_position==0 or page_position=="0":
                    page_position =1
                if limit =='' or limit==0 or limit=="0":
                    limit =5
            p = Paginator(cashout, int(limit))
            number_of_rows = p.count
            number_of_pages = p.num_pages
            if int(page_position)>number_of_pages:
                page_position =number_of_pages
            page_data = p.page(int(page_position))
            paginations ={
                'number_of_rows':number_of_rows,
                'number_of_pages':number_of_pages,
                'page_position':int(page_position),
                'limit':int(limit)
            }
            serializer = CashOutSerializer(page_data,context={'request': request},many=True)
            return Response({"data":serializer.data,"paginator":paginations}, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'You are not allowed to make this aperation.'
            return Response({'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)        


def generer_code(origine_agency,destination_agency):
    origin_agency_id_romaine = integer_to_roman(origine_agency)
    
    if len(origin_agency_id_romaine)==1:
        origin_agency_id_romaine = "0"+origin_agency_id_romaine        
    destination_agency_id_romaine = integer_to_roman(destination_agency)
    if len(destination_agency_id_romaine)==1:
        destination_agency_id_romaine = "0"+destination_agency_id_romaine
    now = datetime.now()
    code = "{}{:02d}{:02d}{:02d}.{}{:02d}{:02d}.{:02d}{:04d}".format(origin_agency_id_romaine,now.year % 100, now.month, now.day,destination_agency_id_romaine,now.hour, now.minute, now.second, now.microsecond // 1000)
    return code

def integer_to_roman(num):
    # Définition des symboles et de leurs valeurs
    symbols = {
        1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X',
        40: 'XL', 50: 'L', 90: 'XC', 100: 'C',
        400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'
    }
    
    # Création d'une liste des valeurs triées dans l'ordre décroissant
    sorted_symbols = sorted(symbols.keys(), reverse=True)
    
    roman_numeral = ''
    
    # Parcourir les symboles en ordre décroissant
    for value in sorted_symbols:
        # Diviser le nombre par la valeur actuelle du symbole
        quotient, num = divmod(num, value)
        # Ajouter le symbole autant de fois que nécessaire
        roman_numeral += symbols[value] * quotient
    
    return roman_numeral