
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.



class Boiler(models.Model):
    FUEL_CHOICES = (
        ('coal', _("Ko'mir")),
        ('gas', _("Gaz")),
    )
    name = models.CharField(max_length=255, verbose_name="Nomi")
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES, default='coal', verbose_name="Yoqilg'i turi")
    image = models.ImageField(upload_to='boilers/', verbose_name="Rasm")
    power = models.CharField(max_length=50, verbose_name="Quvvati (kVt)", blank=True, null=True)
    heating_area = models.CharField(max_length=50, verbose_name="Isitish maydoni (kv.m)", blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi", blank=True, null=True)
    description = models.TextField(verbose_name="Qo'shimcha ma'lumot", blank=True, null=True)
    # TEXNIK XUSUSIYATLARI
    working_pressure = models.CharField(max_length=50, verbose_name="Ish bosimi", blank=True, null=True, help_text="Faqat son kiriting (masalan: 2)")
    power_supply = models.CharField(max_length=50, verbose_name="Elektr ta'minoti", blank=True, null=True, help_text="Faqat son (masalan: 220)")
    dimensions = models.CharField(max_length=100, verbose_name="O'lchami (U × E × B)", blank=True, null=True, help_text="Masalan: 640 x 500 x 720")
    weight = models.CharField(max_length=50, verbose_name="Og'irligi", blank=True, null=True, help_text="Faqat son (masalan: 700)")
    chamber_volume = models.CharField(max_length=50, verbose_name="Yonish kamerasi hajmi", blank=True, null=True, help_text="Faqat son (masalan: 120)")
    bunker_volume = models.CharField(max_length=50, verbose_name="Bunker hajmi", blank=True, null=True, help_text="Faqat son (masalan: 100)")

    # ISHLASH XUSUSIYATLARI
    working_time = models.CharField(max_length=50, verbose_name="Bir marta yuklashda ishlash vaqti", blank=True, null=True, help_text="Faqat son (masalan: 12)")
    fuel_consumption = models.CharField(max_length=50, verbose_name="Yoqilg'i sarfi", blank=True, null=True, help_text="Faqat son (masalan: 6)")
    control_system = models.CharField(max_length=255, verbose_name="Boshqaruv tizimi", blank=True, null=True)
    safety_system = models.CharField(max_length=255, verbose_name="Xavfsizlik tizimi", blank=True, null=True)

    # AVTOMATIKA / KOMPLEKTATSIYA
    automation = models.TextField(verbose_name="Avtomatika / Aqilli boshqaruv", blank=True, null=True)
    equipment_set = models.TextField(verbose_name="Komplektatsiya", blank=True, null=True)

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

    class Meta:
        verbose_name = "Qozon"
        verbose_name_plural = "Qozonlar"

    def __str__(self):
        return self.name

class BoilerImage(models.Model):
    boiler = models.ForeignKey(Boiler, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='boilers/extra/', verbose_name="Rasm")

    class Meta:
        verbose_name = "Qo'shimcha rasm"
        verbose_name_plural = "Qo'shimcha rasmlar"
        ordering = ['id']
