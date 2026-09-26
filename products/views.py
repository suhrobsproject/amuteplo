from django.shortcuts import render
from django.views import View
from .models import Boiler

class HomeView(View):
    def get(self, request):
        coal_boilers = Boiler.objects.filter(fuel_type='coal')
        gas_boilers = Boiler.objects.filter(fuel_type='gas')
        
        context = {
            'coal_boilers': coal_boilers,
            'gas_boilers': gas_boilers,
        }
        return render(request, 'index.html', context)
        
    def post(self, request):
        # Hozircha POST so'rovlari orqali buyurtma yoki xabar yuborish imkoniyati qo'shishingiz mumkin
        # Misol uchun, contact form
        return render(request, 'index.html', {'message': "Post so'rovi qabul qilindi"})
from django.shortcuts import get_object_or_404

class BoilerDetailView(View):
    def get(self, request, pk):
        boiler = get_object_or_404(Boiler, pk=pk)
        return render(request, 'boiler_detail.html', {'boiler': boiler})
