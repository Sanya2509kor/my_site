from django.db import models

class Examples(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255, blank=False, null=False)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Пример'
        verbose_name_plural = 'Примеры'

    def __str__(self):
        return self.name

class ListImages(models.Model):
    product = models.ForeignKey(
        Examples,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Пример работы'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='examples_images/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'Изображение #{self.id} для {self.product.name}'