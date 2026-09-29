
from django.db import models

# Create your models here.



class Boiler(models.Model):
    FUEL_CHOICES = (
        ('coal', "Ko'mir"),
        ('gas', "Gaz"),
    )
    name = models.CharField(max_length=255, verbose_name="Nomi")
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES, default='coal', verbose_name="Yoqilg'i turi")
    image = models.ImageField(upload_to='boilers/', verbose_name="Rasm")
    power = models.CharField(max_length=50, verbose_name="Quvvati (kVt)", blank=True, null=True)
    heating_area = models.CharField(max_length=50, verbose_name="Isitish maydoni (kv.m)", blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi", blank=True, null=True)
    description = models.TextField(verbose_name="Qo'shimcha ma'lumot", blank=True, null=True)
    youtube_link = models.URLField(verbose_name="YouTube video havolasi (linki)", blank=True, null=True)

    def get_youtube_embed_url(self):
        import re
        if self.youtube_link:
            # Handle standard, short, embed, and shorts urls
            match = re.search(r'(?:v=|youtu\.be/|embed/|shorts/)([^&?]+)', self.youtube_link)
            if match:
                video_id = match.group(1)[:11]
                
                return f"https://www.youtube-nocookie.com/embed/{video_id}"
        return None

    def __str__(self):
        return self.name
