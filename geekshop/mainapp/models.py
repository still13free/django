from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            verbose_name='название')
    description = models.TextField(verbose_name='описание')
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('-id',)


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(max_length=128, verbose_name='название продукта')
    image = models.ImageField(upload_to='products_images',
                              blank=True, verbose_name='картинка')
    short_desc = models.CharField(
        max_length=255, blank=True, verbose_name='краткое описание продукта')
    description = models.TextField(
        blank=True, verbose_name='описание продукта')
    price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name='цена продукта')
    quantity = models.PositiveSmallIntegerField(
        default=0, verbose_name='количество')
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.category.name})'

    def delete(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()
