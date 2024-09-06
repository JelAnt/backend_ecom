from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Computer(models.Model):
    model = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cpu = models.CharField(max_length=100)
    cpu_cooler = models.CharField(max_length=100)
    motherboard = models.CharField(max_length=100)
    memory = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    warranty = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)


    def __str__(self):
        return f"{self.model} ({self.category.name} {self.price})"
