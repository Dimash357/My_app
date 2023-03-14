from django.db import models


class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'ads'
        # ordering = ('-updated',)
        verbose_name = 'Ad'
        verbose_name_plural = 'Ads'
        # db_table = 'task_task_list_model_table'

    def __str__(self):
        return f"{self.title} | {self.description[0:30]}... | {self.price} | {self.date_created}"