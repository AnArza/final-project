from django.db import models
from django.core.validators import MinValueValidator


class Config(models.Model):
    auction_type_choices = [
        (1, 1),
        (2, 2),
    ]
    mode_choices = [
        ("fr", "free"),
        ("sc", "script")
    ]

    impression_total = models.IntegerField()
    auction_type = models.IntegerField(choices=auction_type_choices)
    mode = models.CharField(max_length=2, choices=mode_choices)
    budget = models.IntegerField()
    impression_revenue = models.IntegerField()
    click_revenue = models.IntegerField()
    conversion_revenue = models.IntegerField()
    frequency_capping = models.IntegerField()


class Creative(models.Model):
    external_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    # categories = models.ManyToOneRel(Category, on_delete=models.CASCADE, to=Category, field_name=id)


class Category(models.Model):
    code = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100)
    creative = models.ForeignKey(Creative, default=1, on_delete=models.CASCADE)


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    budget = models.IntegerField()


class Bid(models.Model):
    external_id = models.IntegerField()
    price = models.FloatField(validators=[MinValueValidator(0.01)])
    image_url = models.TextField()
    # cat = models.ForeignKey(Category, on_delete=models.CASCADE)
