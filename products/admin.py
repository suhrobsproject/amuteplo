from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import Boiler, BoilerImage

class BoilerImageInline(admin.TabularInline):
    model = BoilerImage
    extra = 1

class BoilerAdmin(TranslationAdmin):
    list_display = ('name', 'fuel_type', 'formatted_price', 'delete_button')
    list_filter = ('fuel_type',)
    inlines = [BoilerImageInline]
    
    fieldsets = (
        ("1. ASOSIY MA'LUMOTLAR", {
            'fields': ('name', 'fuel_type', 'image', 'power', 'heating_area', 'price', 'description')
        }),
        ("2. TEXNIK XUSUSIYATLARI", {
            'fields': ('working_pressure', 'power_supply', 'dimensions', 'weight', 'chamber_volume', 'bunker_volume')
        }),
        ("3. ISHLASH XUSUSIYATLARI", {
            'fields': ('working_time', 'fuel_consumption', 'control_system', 'safety_system')
        }),
        ("4. AVTOMATIKA / AQILLI BOSHQARUV", {
            'fields': ('automation',)
        }),
        ("5. KOMPLEKTATSIYA", {
            'fields': ('equipment_set',)
        }),
        ("VIDEO", {
            'fields': ('youtube_link',)
        }),
    )

    def formatted_price(self, obj):
        if obj.price is not None:
            return "{:,.0f}".format(obj.price).replace(',', ' ')
        return "-"
    formatted_price.short_description = "Narxi"
    
    def delete_button(self, obj):
        delete_url = reverse('admin:products_boiler_delete', args=[obj.pk])
        return format_html(
            '<a href="{}" style="background-color: #dc3545; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 14px;"><i class="fas fa-trash"></i></a>',
            delete_url
        )
    delete_button.short_description = "Harakat"

admin.site.register(Boiler, BoilerAdmin)
