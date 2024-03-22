from django.shortcuts import render

from django.http import HttpResponse
from io import BytesIO
import inflect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, portrait,A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import HexColor
from datetime import datetime
from reportlab.lib.colors import Color
from reportlab.graphics.shapes import *
style = ParagraphStyle('center pragraph',
            fontName="arial-bold",            
            fontSize =9,
            textColor =Color.hexvala(HexColor(0x59DF2)),          
            leading =10,
            alignment=1,
        )
pdfmetrics.registerFont(TTFont('arial', 'static/fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('arial-bold', 'static/fonts/arial_bold.ttf'))

from .models import CashIn,CashOut,Interrest
# Create your views here.
def receipent(request,id):
    cash_in = CashIn.objects.filter(id=id).values(
        'id',
        'created_by__username',
        'sender',
        'recipient',
        'code',
        'amount',
        'created_at',
        'interrest_config__agency_liason__origin__firm__logo',
        'interrest_config__agency_liason__origin__firm__name',
        'interrest_config__agency_liason__origin__firm__email',
        'interrest_config__agency_liason__origin__phone',
        'interrest_config__agency_liason__origin__address',
        'interrest_config__agency_liason__origin__name',
        'interrest_config__agency_liason__destination__name',
        'interrest_config__agency_liason__destination__phone'
        )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+ id+'".pdf"'

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setPageSize(portrait(A4))
    pdf.drawImage('media/'+cash_in[0]['interrest_config__agency_liason__origin__firm__logo'], 60, 780, 50, 54,mask='auto') 
    pdf.setFillColor('black')
   
    pdf.setFont('arial-bold', 20)
    pdf.drawString(220,790,"RECEIPT".upper())
    pdf.setFont('arial-bold', 13)
    # firm name
    pdf.drawString(65,755,cash_in[0]["interrest_config__agency_liason__origin__firm__name"].upper())
    
    # icones
    pdf.drawInlineImage("static/icons/agency.png", 385,820, 10, 10) 
    pdf.drawInlineImage("static/icons/gps.png", 385,800, 10, 10) 
    pdf.drawInlineImage("static/icons/email.png", 385,780, 10, 10) 
    pdf.drawInlineImage("static/icons/phone.png", 385,760, 10, 10) 
    # icones text
    pdf.setFont('arial', 8)
    pdf.drawString(400,820,cash_in[0]['interrest_config__agency_liason__origin__name'].upper())
    pdf.drawString(400,800,cash_in[0]['interrest_config__agency_liason__origin__address'].upper())
    pdf.drawString(400,780,cash_in[0]['interrest_config__agency_liason__origin__firm__email'])
    pdf.drawString(400,760,cash_in[0]['interrest_config__agency_liason__origin__phone'].upper())
    # cash_in code
    pdf.setFont('arial', 12)
    pdf.drawString(65,720,"NO.")
    pdf.drawString(90,720,cash_in[0]['code'])
    pdf.setDash(0.1, 0.4)
    pdf.line(90, 718, 200, 718)

    # cash_in date
    pdf.setFont('arial', 12)
    pdf.drawString(400,720,"Date.")
    created_at =datetime.date(cash_in[0]['created_at'])
    pdf.drawString(432,720,created_at.strftime("%Y-%m-%d"))
    # pdf.setDash(0.1, 0.4)
    pdf.line(429, 718, 518, 718)

    # cash_in client
    pdf.setFont('arial', 12)
    pdf.drawString(65,695,"Receveid with thanks from")
    pdf.drawString(212,695,cash_in[0]['sender'])
    # pdf.setDash(0.1, 0.4)
    pdf.line(210, 693, 518, 693)

    # cash_in client
    pdf.setFont('arial', 12)
    pdf.drawString(65,665,"Amount of Tk(in word)")
    p = inflect.engine()
    pdf.drawString(191,665,p.number_to_words(cash_in[0]['amount'])+" usd")
    # pdf.setDash(0.1, 0.4)
    pdf.line(190, 663, 518, 663)
    # cash_in client
    pdf.setFont('arial', 12)
    pdf.drawString(65,640,"To")
    pdf.drawString(95,640,cash_in[0]['recipient'])
    # pdf.setDash(0.1, 0.4)
    pdf.line(85, 638, 250, 638)
    pdf.drawString(253,640,"at ")
    pdf.drawString(275,640,cash_in[0]['interrest_config__agency_liason__destination__name'])
    pdf.line(265, 638, 518, 638)

    # cash_in destination conact number
    pdf.setFont('arial', 12)
    pdf.drawString(65,613,"Contact NO.")
    pdf.drawString(150,613,cash_in[0]['interrest_config__agency_liason__destination__phone'])
    # pdf.setDash(0.1, 0.4)
    pdf.line(125, 610, 518, 610)

    # amount rect
    pdf.rect(365, 565, 150, 25,)
    pdf.drawString(340,570,"Tk.")
    pdf.drawString(390,570,str(cash_in[0]['amount']))

    # received by
    # pdf.line(125, 610, 518, 610)
    # pdf.drawString(340,535,"Receveid By")
    # pdf.drawString(390,570,str(cash_in[0]['amount']))
    

    pdf.save()

    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response 

def voucher_output(request,id):
    cash_in = CashOut.objects.filter(id=id).values(
        'id',
        'created_by__username',
        'recipient',
        'transaction__code',
        'amount',
        'created_at',
        'transaction__sender',
        'transaction__interrest__agency_liason__destination__firm__logo',
        'transaction__interrest__agency_liason__destination__firm__name',
        'transaction__interrest__agency_liason__destination__firm__email',
        'transaction__interrest__agency_liason__destination__phone',
        'transaction__interrest__agency_liason__destination__address',
        'transaction__interrest__agency_liason__destination__name',
        'transaction__interrest__agency_liason__origin__name',
        'transaction__interrest__agency_liason__origin__phone',
        )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+ id+'".pdf"'

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setPageSize(portrait(A4))
    pdf.drawImage('media/'+cash_in[0]['transaction__interrest__agency_liason__destination__firm__logo'], 60, 780, 50, 54,mask='auto') 
    pdf.setFillColor('black')
   
    pdf.setFont('arial-bold', 13)
    pdf.drawString(190,790,"withdrawal voucher".upper())
    pdf.setFont('arial-bold', 11)
    # firm name
    pdf.drawString(65,755,cash_in[0]["transaction__interrest__agency_liason__destination__firm__name"].upper())
    
    # icones
    pdf.drawInlineImage("static/icons/agency.png", 385,820, 10, 10) 
    pdf.drawInlineImage("static/icons/gps.png", 385,800, 10, 10) 
    pdf.drawInlineImage("static/icons/email.png", 385,780, 10, 10) 
    pdf.drawInlineImage("static/icons/phone.png", 385,760, 10, 10) 
    # icones text
    pdf.setFont('arial', 8)
    pdf.drawString(400,820,cash_in[0]['transaction__interrest__agency_liason__destination__name'].upper())
    pdf.drawString(400,800,cash_in[0]['transaction__interrest__agency_liason__destination__address'].upper())
    pdf.drawString(400,780,cash_in[0]['transaction__interrest__agency_liason__destination__firm__email'])
    pdf.drawString(400,760,cash_in[0]['transaction__interrest__agency_liason__destination__phone'].upper())
    # cash_in code
    pdf.setFont('arial', 12)
    pdf.drawString(65,720,"NO.")
    pdf.drawString(90,720,cash_in[0]['transaction__code'])
    pdf.setDash(0.1, 0.4)
    pdf.line(90, 718, 200, 718)

    # cash_in date
    pdf.setFont('arial', 12)
    pdf.drawString(400,720,"Date.")
    created_at =datetime.date(cash_in[0]['created_at'])
    pdf.drawString(432,720,created_at.strftime("%Y-%m-%d"))
    # pdf.setDash(0.1, 0.4)
    pdf.line(429, 718, 518, 718)

    # cash_in client
    pdf.setFont('arial', 12)
    # pdf.drawString(65,695,"Receveid with thanks from")
    pdf.drawString(65,695,"We return the money to")
    pdf.drawString(212,695,cash_in[0]['recipient'])
    # pdf.setDash(0.1, 0.4)
    pdf.line(210, 693, 518, 693)

    # cash_in client
    pdf.setFont('arial', 12)
    pdf.drawString(65,665,"Amount of Tk(in word)")
    p = inflect.engine()
    pdf.drawString(191,665,p.number_to_words(cash_in[0]['amount'])+" usd")
    # pdf.setDash(0.1, 0.4)
    pdf.line(190, 663, 518, 663)
    # cash_in client
    pdf.setFont('arial', 12)
    pdf.drawString(65,640,"From")
    pdf.drawString(95,640,cash_in[0]['transaction__sender'])
    # pdf.setDash(0.1, 0.4)
    pdf.line(85, 638, 250, 638)
    pdf.drawString(253,640,"at ")
    pdf.drawString(275,640,cash_in[0]['transaction__interrest__agency_liason__origin__name'])
    pdf.line(265, 638, 518, 638)

    # cash_in destination conact number
    pdf.setFont('arial', 12)
    pdf.drawString(65,613,"Contact NO.")
    pdf.drawString(150,613,cash_in[0]['transaction__interrest__agency_liason__origin__phone'])
    # pdf.setDash(0.1, 0.4)
    pdf.line(125, 610, 518, 610)

    # amount rect
    pdf.rect(365, 565, 150, 25,)
    pdf.drawString(340,570,"Tk.")
    pdf.drawString(390,570,str(cash_in[0]['amount']))

    # received by
    # pdf.line(125, 610, 518, 610)
    # pdf.drawString(340,535,"Receveid By")
    # pdf.drawString(390,570,str(cash_in[0]['amount']))
    

    pdf.save()

    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response 
    
def cashIn_report(request,id):
    pass