from .imports import *

class Event(models.Model):
    title = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=5000, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    members = models.ManyToManyField(User)

    numberOfUsers = models.PositiveSmallIntegerField(default=2, validators=[MinValueValidator(2), MaxValueValidator(100)])
    numberOfCars = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    numberOfSpecials = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __unicode__(self):
        return self.title