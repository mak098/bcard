from django.contrib import admin
from .models import CashIn,CashOut,Interrest
from Agency.models import InterrestRateConfig
from django.forms import TextInput, Textarea
from django.db import models
from django.utils.html import format_html
from .report_controlers import receipent,voucher_output
class CashOutInlines(admin.TabularInline):
    model = CashOut
    extra = 1
   
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    

@admin.register(CashIn)
class CashInAdmin(admin.ModelAdmin):
    list_display = ("code","sender","amount","status","generate_pdf_preview_html")
    fields = ("interrest_config","amount","sender","sender_phone","recipient","recipient_phone","comment")
    search_fields =("code","sender")
    list_filter = ("interrest_config__agency_liason__origin","interrest_config__agency_liason__destination","status","created_at")
    inlines = (CashOutInlines,)
    # raw_id_fields = ('interrest',)
    # readonly_fields =['interrest']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

    
    def save_model(self, request, obj, form, change):
        # get agence id 
        
        obj.created_by = request.user
        # obj.agence_origin =request.user.agency
        obj.save()

        Interrest.objects.create(
            created_by = request.user,
            cash_in= obj,
            amount = (obj.amount * obj.interrest.rate)/100
        ).save()

    #autocomplete interseter filter
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user =request.user
        if db_field.name == 'interrest':
            kwargs["queryset"] = InterrestRateConfig.objects.filter(agency_liason__origin=user.agency,status=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        user =request.user        
        if user.is_superuser:
            return super().get_queryset(request)
        else:                      
            return super().get_queryset(request).filter(interrest__agency_liason__origin= user.agency)

    #pdf code cash_in generator
        
    def generate_pdf_preview_html(self, obj):
        return format_html('<a class="button" href="%s/gen_pdf_preview/">print note</a>' % obj.id)

    generate_pdf_preview_html.short_description = 'print code'
    generate_pdf_preview_html.allow_tags = True

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls= [
            path('<path:id>/gen_pdf_preview/', self.admin_site.admin_view(receipent),
                name='vision_questionarioistituzionescolastica_generatepdf')
        ]       
        return custom_urls + urls

    # also tried this way, but it does not work either
    def generatepdf_view(self, request, obj, form_url='', extra_context=None):
        print("generatepdf_view {0}".format(str(obj.id)))
        pass

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(CashInAdmin, self).get_form(request, obj, **kwargs)
    #     field = form.base_fields["interrest"]
    #     field.widget.can_add_related = False
    #     field.widget.can_change_related = False
    #     field.widget.can_delete_related = False
    #     field.widget.can_view_related = False
    #     return form
@admin.register(CashOut)
class CashOutAdmin(admin.ModelAdmin):
    list_display = ("amount","recipient","recipient_phone","generate_pdf_preview_html")
    fields = ("cash_in","amount","recipient","recipient_phone","comment")
    search_fields =("transaction__code","recipient")
    
    # autocomplete_fields =("cash_in",)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()
    
    def get_queryset(self, request):
        user =request.user        
        if user.is_superuser:
            return super().get_queryset(request)
        else:                      
            return super().get_queryset(request).filter(transaction__interrest__agency_liason__destination= user.agency)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user =request.user
        if db_field.name == 'cash_in':
            kwargs["queryset"] = CashIn.objects.filter(interrest_config__agency_liason__destination=user.agency,status=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
     #pdf code cash_in generator
        
    def generate_pdf_preview_html(self, obj):
        return format_html('<a class="button" href="%s/gen_pdf_preview/">print note</a>' % obj.id)

    generate_pdf_preview_html.short_description = 'print code'
    generate_pdf_preview_html.allow_tags = True

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls= [
            path('<path:id>/gen_pdf_preview/', self.admin_site.admin_view(voucher_output),
                name='vision_questionarioistituzionescolastica_generatepdf')
        ]       
        return custom_urls + urls

    # also tried this way, but it does not work either
    def generatepdf_view(self, request, obj, form_url='', extra_context=None):
        print("generatepdf_view {0}".format(str(obj.id)))
        pass

@admin.register(Interrest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ("created_by","cash_in","amount")
    search_fields =("transaction__code","created_by__username")
    list_filter = ("cash_in__interrest_config__agency_liason__origin","created_by","created_at")
   