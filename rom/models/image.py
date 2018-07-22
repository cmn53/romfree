from django.contrib.gis.db import models
from .hotel import Hotel

class Image(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    path = models.CharField(max_length=50)
    image_type = models.CharField(max_length=3, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.path

    class Meta:
        ordering = ['order']
