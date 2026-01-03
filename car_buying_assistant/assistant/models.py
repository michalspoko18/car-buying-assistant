from django.db import models

class CarMake(models.Model):
    id_car_make = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    date_create = models.IntegerField()
    date_update = models.IntegerField()
    id_car_type = models.IntegerField()

    class Meta:
        db_table = "car_make"
        managed = False
        ordering = ["name"]

    def __str__(self):
        return self.name
