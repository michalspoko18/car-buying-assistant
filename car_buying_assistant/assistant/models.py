from django.db import models


class CarType(models.Model):
    id_car_type = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "car_type"
        managed = False
        ordering = ["name"]

    def __str__(self):
        return self.name


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


class CarGeneration(models.Model):
    id_car_generation = models.IntegerField(primary_key=True)
    id_car_model = models.IntegerField()
    name = models.CharField(max_length=255)
    year_begin = models.IntegerField(null=True)
    year_end = models.IntegerField(null=True)
    date_create = models.IntegerField()
    date_update = models.IntegerField()
    id_car_type = models.IntegerField()

    class Meta:
        db_table = "car_generation"
        managed = False
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarSerie(models.Model):
    id_car_serie = models.IntegerField(primary_key=True)
    id_car_model = models.IntegerField()
    id_car_generation = models.IntegerField()
    name = models.CharField(max_length=255)
    date_create = models.IntegerField()
    date_update = models.IntegerField()
    id_car_type = models.IntegerField()

    class Meta:
        db_table = "car_serie"
        managed = False
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarTrim(models.Model):
    id_car_trim = models.IntegerField(primary_key=True)
    id_car_serie = models.IntegerField()
    id_car_model = models.IntegerField()
    name = models.CharField(max_length=255)
    start_production_year = models.IntegerField(null=True)
    end_production_year = models.IntegerField(null=True)
    date_create = models.IntegerField()
    date_update = models.IntegerField()
    id_car_type = models.IntegerField()

    class Meta:
        db_table = "car_trim"
        managed = False
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarEquipment(models.Model):
    id_car_equipment = models.IntegerField(primary_key=True)
    id_car_trim = models.IntegerField()
    name = models.CharField(max_length=255)
    year = models.IntegerField(null=True)
    date_create = models.IntegerField()
    date_update = models.IntegerField()
    id_car_type = models.IntegerField()

    class Meta:
        db_table = "car_equipment"
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


class CarSpecificationValue(models.Model):
    id_car_specification_value = models.IntegerField(primary_key=True)
    id_car_trim = models.IntegerField()
    id_car_specification = models.IntegerField()
    value = models.CharField(max_length=255)
    unit = models.CharField(max_length=255, null=True)
    date_create = models.IntegerField()
    date_update = models.IntegerField()
    id_car_type = models.IntegerField()

    class Meta:
        db_table = "car_specification_value"
        managed = False

    def __str__(self):
        return f"{self.value} {self.unit}".strip()


class CarOption(models.Model):
    id_car_option = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    id_parent = models.IntegerField(null=True)
    date_create = models.IntegerField()
    date_update = models.IntegerField()
    id_car_type = models.IntegerField()

    class Meta:
        db_table = "car_option"
        managed = False
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarOptionValue(models.Model):
    id_car_option_value = models.IntegerField(primary_key=True)
    id_car_option = models.IntegerField()
    id_car_equipment = models.IntegerField()
    is_base = models.IntegerField()
    date_create = models.IntegerField()
    date_update = models.IntegerField()
    id_car_type = models.IntegerField()

    class Meta:
        db_table = "car_option_value"
        managed = False
