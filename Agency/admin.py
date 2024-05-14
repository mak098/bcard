from django.contrib import admin
from .models import Firm,Agency, LiasonAgency,InterrestRateConfig

class AgencyInline(admin.TabularInline):

	model = Agency
	extra = 0
	fields =('name', 'address','phone','email')
	
	def save_related(self, request, obj, form, change):
		obj.created_by = request.user
		obj.save()

class InterrestRateConfigInline(admin.TabularInline):
	model = InterrestRateConfig
	extra = 0
	fields =('agency_liason', 'rate','forfait','threshold','status')
	

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		obj.save()


@admin.register(Firm)
class FirmAdmin(admin.ModelAdmin):
	list_display = ('name','email','phone', 'address')
	fields = ('logo','name','email','phone', 'address')
	# list_filter = ('is_active', )
	search_fields = ('name','created_by')
	inlines = (AgencyInline, )
	# verbose_name  = 'Firmes'

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		obj.save()
	

@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
	
	list_display = ('name', 'phone')
	fields = ('name', 'address','phone','email')
	# list_filter = ('is_active', )
	search_fields = ('name','created_by')
	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		obj.save()
	

@admin.register(LiasonAgency)
class LiasonAgencyAdmin(admin.ModelAdmin):

	list_display = ('origin', 'destination')
	fields = ('origin', 'destination')
	# list_filter = ('is_active', )
	search_fields = ('origin', 'destination')
	# autocomplete_fields = ('origin', 'destination')
	inlines =(InterrestRateConfigInline,)

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		obj.save()

@admin.register(InterrestRateConfig)
class InterrestRateConfig(admin.ModelAdmin):
	list_display = ('agency_liason', 'rate','forfait','threshold','status')
	fields = ('agency_liason', 'rate','forfait','threshold','status')
	list_filter = ('status',"agency_liason__origin" )
	search_fields = ('agency_liason','status')
	autocomplete_fields = ("agency_liason",)

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		obj.save()


