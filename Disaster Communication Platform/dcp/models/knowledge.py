from .imports import *
from .catastrophe import *
from .profile import *
from .goods import *
import dcp.dcpSettings

"""
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
"""
class Knowledge(models.Model):
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
    #bumps = models.ForeignKey(Bump_Relation, on_delete=models.DO_NOTHING, null=True, blank=True)
    #reports = models.ForeignKey(Report_Relation, on_delete=models.DO_NOTHING, null=True, blank=True)
    visibility = models.BooleanField(default=True, blank=True)

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
#
  #  def getBumps(self):
 #       return Bump.objects.filter(relation = self.bumps)
#
 #   def getReports(self):
#        return Report.objects.filter(relation = self.reports)


    def getKnowledge(type, id):
        if type == 'News':
            return News.objects.get(id=id)
        if type == 'Danger':
            return Danger.objects.get(id=id)
        if type == 'Question':
            return Question.objects.get(id=id)
        return None

    def stringToKnowledgeClass(type):
        if type == 'News':
            return News
        if type == 'Danger':
            return Danger
        if type == 'Question':
            return Question
        return None

    def getAllKnowledge():
        listOfKnowledge = []
        for oneKnowledge in Post_News.objects.all():
            listOfKnowledge.append(oneKnowledge)
        for oneKnowledge in Post_Dangers.objects.all():
            listOfKnowledge.append(oneKnowledge)
        for oneKnowledge in Post_Questions.objects.all():
            listOfKnowledge.append(oneKnowledge)
        return listOfKnowledge

    def isSearchedForByString(self, searchString):
        if searchString.upper() in self.description.upper() or searchString.upper() in self.title.upper():
            return True
        else:
            return False

    class Meta:
        abstract = True

class Post_News(Knowledge):
    timeline_badge_color = models.CharField(max_length=100, null=False, default='yellow')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-bullhorn')

    def getGoodType(self):
        return 'News'

class Post_Dangers(Knowledge):
    timeline_badge_color = models.CharField(max_length=100, null=False, default='yellow')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-alert')

    def getGoodType(self):
        return 'Danger'

class Post_Questions(Knowledge):
    timeline_badge_color = models.CharField(max_length=100, null=False, default='yellow')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-question-sign')

    def getGoodType(self):
        return 'Question'