from modeltranslation.translator import register, TranslationOptions
from .models import Boiler

@register(Boiler)
class BoilerTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

