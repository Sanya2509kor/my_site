from django.db import models
from django.urls import reverse


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
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ForeignKey(to=SubCategories, on_delete=models.CASCADE, verbose_name='Подкатегория', blank=True, null=True)

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
        ordering = ("id", )

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
    