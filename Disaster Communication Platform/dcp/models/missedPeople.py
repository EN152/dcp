from .imports import *

class MissedPeople(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    # catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    #bumps = models.ForeignKey(Bump_Relation, on_delete=models.DO_NOTHING, null=True)
    #reports = models.ForeignKey(Report_Relation, on_delete=models.DO_NOTHING, null=True)

    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=5000, null=False)
    gender = models.CharField(max_length=1, null=False)
    age = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    name = models.CharField(max_length=100, null=False)
    size = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(250)])
    eyeColor = models.CharField(max_length=50, null=False)
    hairColor = models.CharField(max_length=50, null=False)
    characteristics = models.CharField(max_length=500, null=False)
    picture = models.ImageField(upload_to='upload/people/', null=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def delete(self, using = None, keep_parents = False):
        if self.picture is not None:
            try:
                self.picture.delete()
            except Exception:
                pass
        return super().delete(using, keep_parents)