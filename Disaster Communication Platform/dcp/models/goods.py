from .imports import *
from .catastrophe import *
from .profile import *
from .categorysGoods import *

import dcp.dcpSettings

class Bump_Relation(models.Model):
    pass

class Report_Relation(models.Model):
    pass

class Bump(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    relation = models.ForeignKey(Bump_Relation, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(default=timezone.now)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    relation = models.ForeignKey(Report_Relation, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(default=timezone.now)

class Goods(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
    catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    locationString = models.CharField(default='', max_length=200, null=True)
    location_x = models.FloatField(null=True)
    location_y = models.FloatField(null=True)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    image = models.ImageField(upload_to=dcp.dcpSettings.GOODS_IMAGE_UPLOADPATH, null=True, blank=True)
    comments = models.ForeignKey(Comment_Relation, on_delete=models.DO_NOTHING, null=True, blank=True)
    bumps = models.ForeignKey(Bump_Relation, on_delete=models.DO_NOTHING, null=True, blank=True)
    reports = models.ForeignKey(Report_Relation, on_delete=models.DO_NOTHING, null=True, blank=True)
    visibility = models.BooleanField(default=True, blank=True)
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
        if type == 'Post_News':
            return Post_News.objects.get(id=id)
        if type == 'Post_Danger':
            return Post_Danger.objects.get(id=id)
        if type == 'Post_Question':
            return Post_Question.objects.get(id=id)
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
        if type == 'Post_News':
            return Post_News
        if type == 'Post_Danger':
            return Post_Danger
        if type == 'Post_Question':
            return Post_Question
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
        for oneGood in Post_News.objects.all():
            listOfGoods.append(oneGood)
        for oneGood in Post_Dangers.objects.all():
            listOfGoods.append(oneGood)
        for oneGood in Post_Questions.objects.all():
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
    category = models.ForeignKey(CategorysGoods, on_delete=models.CASCADE, null=True)

    def getCategoryGlyphiconAsString(self):
        return self.category.glyphiconString

    def getCategoryNameAsString(self):
        return self.category.name

    class Meta:
        abstract = True

class Immaterial_Goods(Goods):
    pass

class Search_Material(Material_Goods):
    radius = models.PositiveSmallIntegerField(default=0, choices=dcp.dcpSettings.RADIUS_CHOICES_GOODS)
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
    radius = models.PositiveSmallIntegerField(default=0, choices=dcp.dcpSettings.RADIUS_CHOICES_GOODS)
    timeline_badge_color = models.CharField(max_length=100, null=False, default='blue')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-search')

    def getGoodType(self):
        return 'Search_Immaterial'

class Offer_Immaterial(Immaterial_Goods):
    timeline_badge_color = models.CharField(max_length=100, null=False, default='red')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-transfer')

    def getGoodType(self):
        return 'Offer_Immaterial'

class Post_News(Goods):
    timeline_badge_color = models.CharField(max_length=100, null=False, default='yellow')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-info-sign')

    def getGoodType(self):
        return 'Post_News'

class Post_Dangers(Goods):
    timeline_badge_color = models.CharField(max_length=100, null=False, default='yellow')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-info-sign')

    def getGoodType(self):
        return 'Post_Danger'

class Post_Questions(Goods):
    timeline_badge_color = models.CharField(max_length=100, null=False, default='yellow')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-info-sign')

    def getGoodType(self):
        return 'Post_Question'