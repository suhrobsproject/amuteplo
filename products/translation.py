from modeltranslation.translator import register, TranslationOptions
from .models import Boiler

@register(Boiler)
class BoilerTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'control_system', 'safety_system', 'automation', 'equipment_set',)

