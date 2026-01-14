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


class CarModel(models.Model):
    id_car_model = models.IntegerField(primary_key=True)
    id_car_make = models.IntegerField()
    name = models.CharField(max_length=255)
    date_create = models.IntegerField()
    date_update = models.IntegerField()
    id_car_type = models.IntegerField()

    class Meta:
        db_table = "car_model"
        managed = False
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarSpecification(models.Model):
    id_car_specification = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    id_parent = models.IntegerField(null=True)
    date_create = models.IntegerField()
    date_update = models.IntegerField()
    id_car_type = models.IntegerField()

    class Meta:
        db_table = "car_specification"
        managed = False
        ordering = ["name"]

    def __str__(self):
        return self.name
