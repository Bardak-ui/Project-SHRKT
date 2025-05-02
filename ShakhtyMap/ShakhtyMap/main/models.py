from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Monument(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Panorama(models.Model):
    is_main = models.BooleanField(default=False, verbose_name="Главная панорама")
    monument = models.ForeignKey(Monument, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='panoramas/')
    
    # Параметры панорамы
    vaov = models.FloatField(default=55, verbose_name="Вертикальный угол обзора")
    haov = models.FloatField(default=360, verbose_name="Горизонтальный угол обзора")
    min_pitch = models.FloatField(default=-27, verbose_name="Минимальный наклон")
    max_pitch = models.FloatField(default=27, verbose_name="Максимальный наклон")
    min_yaw = models.FloatField(default=-130, verbose_name="Минимальный поворот")
    max_yaw = models.FloatField(default=130, verbose_name="Максимальный поворот")
    min_Hfov = models.FloatField(default=30,verbose_name="Минимальное увеличение")
    max_Hfov = models.FloatField(default=30,verbose_name="Максимальное увеличение")
    show_zoom_ctrl = models.BooleanField(default=True, verbose_name="Показывать зум")
    
    def __str__(self):
        return self.title
    
class HotSpot(models.Model):
    panorama = models.ForeignKey(
        Panorama, 
        on_delete=models.CASCADE, 
        related_name='hotspots',
        verbose_name="Исходная панорама"
    )
    
    # Координаты точки
    pitch = models.FloatField(
        help_text="Вертикальный угол (-90 до 90)",
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    yaw = models.FloatField(
        help_text="Горизонтальный угол (-180 до 180)",
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    
    # Информация о точке
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='hotspots/', blank=True, null=True)
    
    # Параметры перехода
    target_panorama = models.ForeignKey(
        Panorama, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='target_hotspots',
        verbose_name="Целевая панорама"
    )
    
    # Позиция камеры после перехода
    target_pitch = models.FloatField(
        "Наклон после перехода",
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    target_yaw = models.FloatField(
        "Поворот после перехода",
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    
    # Параметры анимации
    transition_duration = models.PositiveIntegerField(
        "Длительность перехода (мс)",
        default=2000,
        validators=[MinValueValidator(500), MaxValueValidator(5000)]
    )
    target_hfov = models.FloatField(
        "Увеличение при переходе",
        default=50,
        validators=[MinValueValidator(10), MaxValueValidator(120)]
    )
    
    # Дополнительные параметры
    css_class = models.CharField(
        "CSS класс точки",
        max_length=50,
        default="custom-hotspot",
        blank=True
    )
    
    # Для сложных переходов (если нужно указать конкретную точку входа)
    entry_hotspot = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Точка входа в целевую панораму",
        help_text="Если нужно перейти к конкретной точке в целевой панораме"
    )
    
    def __str__(self):
        return f"{self.title} (на {self.panorama.title})"
    
    def save(self, *args, **kwargs):
        # Если не указаны целевые pitch/yaw, используем текущие значения
        if self.target_panorama and not self.target_pitch:
            self.target_pitch = self.pitch
        if self.target_panorama and not self.target_yaw:
            self.target_yaw = self.yaw
            
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Точка интереса"
        verbose_name_plural = "Точки интереса"
        ordering = ['panorama', 'title']