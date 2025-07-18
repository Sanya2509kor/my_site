from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')



    class Meta:
        db_table = 'Category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ("id",)

    def __str__(self):
        return self.name

    # def has_subcategories(category):
    #     return category.subcategories_set.exists()
    
    @property
    def has_subcategories(self):
        return self.subcategories_set.exists()  # Используем related_name
    
    def get_absolute_url(self):
        return reverse("catalog:index", kwargs={"category_slug": self.slug})



class SubCategories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')


    class Meta:
        db_table = 'Subcategory'
        verbose_name = 'Подкатегорию'
        verbose_name_plural = 'Подкатегории'
        ordering = ("id",)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("catalog:index", kwargs={
            "category_slug": self.category.slug,
            "subcategory_slug": self.slug
        })



class Products(models.Model):
    COLOR = [
        ('Без покраски', 'Без покраски'),
        ('Белый','Белый'),
        ('Черный', 'Черный'),
        ('Белый глянец','Белый глянец'),
        ('Белый мат.','Белый мат.'),
        ('Черный мат.', 'Черный мат.'),
        ('Белый муар', 'Белый муар'),
        ('Черный муар', 'Черный муар'),
    ]
    
    SIZES = [
        ('2м.', '2м.'),
        ('2,2м.', '2,2м.'),
        ('2,5м.', '2,5м.'),
        ('3м.', '3м.'),
        ('3.2м.', '3.2м.'),
        ('3.6м.', '3.6м.'),
        ('3м.', '3м.'),
        ('2000 мм.', '2000 мм.'),
        ('40x40', '40x40'),
        ('60x40', '60x40'),
        ('120x80', '120x80'),
    ]

    WATT = [
        ('6W', '6W'),
        ('9W', '9W'),
        ('10W', '10W'),
        ('12W', '12W'),
        ('18W', '18W'),
        ('20W', '20W'),
        ('24W', '24W'),
        ('30W', '30W'),
        ('40W', '40W'),
    ]

    BRIGHTNESS = [
        ('3000K', '3000K'),
        ('4000K', '4000K'),
    ]



    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    color = models.CharField(max_length=30, choices=COLOR, verbose_name="Цвет детали", blank=True, null=True)
    size = models.CharField(max_length=30, choices=SIZES, verbose_name='Размер детали', blank=True, null=True)
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    image_schem = models.ImageField(upload_to='goods_images_schems', blank=True, null=True, verbose_name='Изображение_схемы')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ForeignKey(to=SubCategories, on_delete=models.CASCADE, verbose_name='Подкатегория', blank=True, null=True)
    
    #для света
    bright = models.CharField(max_length=30, choices=BRIGHTNESS, verbose_name='Яркость', blank=True, null=True)
    power = models.CharField(max_length=30, choices=WATT, verbose_name='Мощность', blank=True, null=True)

    related_products = models.ManyToManyField(
        'self',
        through='ProductRelationship',
        through_fields=('from_product', 'to_product'),
        blank=True,
        verbose_name='Сопутствующие товары',
        symmetrical=False
    )

    class Meta:
        db_table = 'Product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("name", "color", "size")

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    


    def display_id(self):
        return f"{self.id:05}"
    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        
        return self.price
    
    def get_color(self):
        if self.color:
            return self.color
        return False
    
    def get_size(self):
        if self.size:
            return self.size
        return False
    
    def get_power(self):
        if self.power:
            return self.power
        return False
    
    def get_bright(self):
        if self.bright:
            return self.bright
        return False
    
    def get_full_name(self):
        full_name = self.name
        if self.color:
            full_name += ' ' + self.color
        if self.size:
            full_name += ' ' + self.size
        if self.bright:
            full_name += ' ' + self.bright
        if self.power:
            full_name += ' ' + self.power
        return full_name
            
    
    
    # создает уникальный URL
    def save(self, *args, **kwargs):
        if not self.slug:  # Если slug не задан, генерируем его
            base_slug = slugify(self.name)
            color_slug = slugify(self.color) if self.color else ''
            size_slug = slugify(self.size) if self.size else ''
            
            self.slug = f"{base_slug}-{color_slug}-{size_slug}" if (color_slug or size_slug) else base_slug
            
            # Убедимся, что slug уникален (если уже есть такой, добавим число в конец)
            original_slug = self.slug
            counter = 1
            while Products.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)
    


class ProductRelationship(models.Model):
    from_product = models.ForeignKey(
        Products, 
        related_name='from_products',
        on_delete=models.CASCADE
    )
    to_product = models.ForeignKey(
        Products, 
        related_name='to_products',
        on_delete=models.CASCADE
    )
    # дополнительные поля связи, если нужно
    # например: relation_type = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = ('from_product', 'to_product')
    