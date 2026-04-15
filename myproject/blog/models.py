from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name="заголовок")
    content = models.TextField(verbose_name="содержимое")
    preview = models.ImageField(
        upload_to="blog/",
        verbose_name="изображение",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    is_published = models.BooleanField(default=True, verbose_name="признак публикации")
    views_count = models.PositiveIntegerField(default=0, verbose_name="количество просмотров")

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блог"
        ordering = ["title"] # Сортировка по наименованию

    def __str__(self):
        return self.title