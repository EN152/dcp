from .imports import *
from .catastrophe import *
from .profile import *

class Bump_Relation(models.Model):
    class Meta:
        abstract = False

class Report_Relation(models.Model):
    class Meta:
        abstract = False

class Bump(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    relation = models.ForeignKey(Bump_Relation, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(default=timezone.now)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    relation = models.ForeignKey(Report_Relation, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(default=timezone.now)

class Goods(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=500, null=True)
    location_x = models.FloatField(null=True)
    location_y = models.FloatField(null=True)
    created_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="upload/goods/")
    comments = models.ForeignKey(Comment_Relation, on_delete=models.DO_NOTHING, null=True)
    bumps = models.ForeignKey(Bump_Relation, on_delete=models.DO_NOTHING, null=True)
    reports = models.ForeignKey(Report_Relation, on_delete=models.DO_NOTHING, null=True)
    visibility = models.BooleanField(default=True)
    # Timelinevariablen müssen in jeder Subklasse neu gesetzt werden

    def delete(self, using = None, keep_parents = False):
        if self.comments is not None:
            self.comments.delete()
        if self.bumps is not None:
            self.bumps.delete()
        if self.reports is not None:
            self.reports.delete()
        if self.image is not None:
            try:
                self.image.delete()
            except Exception:
                pass
        return super().delete(using, keep_parents)

    def __unicode__(self):
        return self.title

    def getComments(self):
        return Comment.objects.filter(relation = self.comments)

    def getBumps(self):
        return Bump.objects.filter(relation = self.bumps)

    def getReports(self):
        return Report.objects.filter(relation = self.reports)

    def getGood(type, id):
        if type == 'Search_Material':
            return Search_Material.objects.get(id=id)
        if type == 'Search_Immaterial':
            return Search_Immaterial.objects.get(id=id)
        if type == 'Offer_Material':
            return Offer_Material.objects.get(id=id)
        if type == 'Offer_Immaterial':
            return Offer_Immaterial.objects.get(id=id)
        return None

    def stringToGoodClass(type):
        if type == 'Search_Material':
            return Search_Material
        if type == 'Search_Immaterial':
            return Search_Immaterial
        if type == 'Offer_Material':
            return Offer_Material
        if type == 'Offer_Immaterial':
            return Offer_Immaterial
        return None

    def getAllGoods():
        listOfGoods = []
        for oneGood in Search_Material.objects.all():
            listOfGoods.append(oneGood)
        for oneGood in Offer_Immaterial.objects.all():
            listOfGoods.append(oneGood)
        for oneGood in Offer_Material.objects.all():
            listOfGoods.append(oneGood)
        for oneGood in Search_Immaterial.objects.all():
            listOfGoods.append(oneGood)
        return listOfGoods

    def isSearchedForByString(self, searchString):
        if searchString.upper() in self.description.upper() or searchString.upper() in self.title.upper():
            return True
        else:
            return False


    class Meta:
        abstract = True

class Material_Goods(Goods):
    category = models.CharField(max_length=1, choices=Categorys.CATEGORY_TYPES)

    def getCategoryGlyphiconAsString(self):
        return Categorys.getCategoryGlyphiconAsString(self.category)

    def getCategoryNameAsString(self):
        return Categorys.getCategoryNameAsString(self.category)

    def getCategoryFilterClassAsString(self):
        return Categorys.getCategoryFilterClassAsString(self.category)

    class Meta:
        abstract = True

class Immaterial_Goods(Goods):
    class Meta:
        abstract = True

class Search_Material(Material_Goods):
    radius = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    timeline_badge_color = models.CharField(max_length=100, null=False, default='blue')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-search')

    def getGoodType(self):
        return 'Search_Material'

class Offer_Material(Material_Goods):
    timeline_badge_color = models.CharField(max_length=100, null=False, default='red')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-transfer')

    def getGoodType(self):
        return 'Offer_Material'

class Search_Immaterial(Immaterial_Goods):
    radius = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    timeline_badge_color = models.CharField(max_length=100, null=False, default='blue')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-search')

    def getGoodType(self):
        return 'Search_Immaterial'

class Offer_Immaterial(Immaterial_Goods):
    timeline_badge_color = models.CharField(max_length=100, null=False, default='red')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-transfer')

    def getGoodType(self):
        return 'Offer_Immaterial'