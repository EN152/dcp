# imports
from dcp.importUrls import *
from django.http import Http404
import dcp.dcpSettings
from django.template.context_processors import request
from django.template.backends.django import Template
from django.forms import *
from geopy.geocoders import Nominatim
from dcp.models.knowledge import *

class TimelineView(View):
    def getCreateNew(self, request, create_new_glyphicon, create_new_button, page_title, create_new_form, good_type, knowledge_type):
        templatePath = 'dcp/content/createNewGood.html'
        goods_list = sorted(Goods.getAllGoods(), key=lambda g: g.created_date, reverse=True)
       # goods_list = filter(lambda x: type(x) is eval(good_type), goods_list)
        
        knowledge_list = sorted(Knowledge.getAllKnowledge(), key=lambda g: g.created_date, reverse=True)
        knowledge_list = filter(lambda x: type(x) is eval(knowledge_type), knowledge_list)

        template = loader.get_template(templatePath)
        context = {
            'create_new_glyphicon': create_new_glyphicon,
            'create_new_button' : create_new_button,
            'page_title': page_title,
            'create_new_form' : create_new_form,
            'goods_list' : goods_list,
            'knowledge_list' : knowledge_list
        }
        return HttpResponse(template.render(context,request))
    
    def getTemplate(self,request):
        goodtype = request.POST.get('good_type')
        knowledgetype = request.POST.get('knowledge_type')         
        if(goodtype == 'Search_Material'):
            goodTemplate = "/suchen/materielles/"
        if(goodtype == 'Offer_Material'):
            goodTemplate = "/bieten/materielles/"
        if(goodtype == 'Search_Immaterial'):
            goodTemplate = "/suchen/immaterielles/"
        if(goodtype == 'Offer_Immaterial'):
            goodTemplate = "/bieten/immaterielles/"
        if(knowledgetype == 'Post_News'):
            knowledgeTemplate = "/wissen/neuigkeiten/"
        if(knowledgetype == 'Post_Dangers'):
            knowledgeTemplate ="/wissen/gefahren/"
        if(knowledgetype == 'Post_Questions'):
            knowledgeTemplate = "/wissen/fragen/"
        else:
            goodTemplate = ''
            knowledgeTemplate = ''
        return goodTemplate, knowledgeTemplate

    def get_good_or_404(self, request):
        good = Goods.getGood(request.POST.get('good_type'), request.POST.get('good_id'))
        if good is None:
           raise Http404
        return good

    def get_knowledge_or_404(self, request):
        knowledge = Knowledge.getKnowledge(request.POST.get('knowledge_type'), request.POST.get('knowledge_id'))
        if knowledge is None:
            raise Http404
        return knowledge

    def createNewGood(self, request, form):
        if form.is_valid():
            newGood = form.save(commit=False)
            newGood.user = request.user
            if newGood.location_x == 0 and newGood.location_y == 0:
                newGood.location_x = None
                newGood.location_y = None
            else:
                geolocator = Nominatim()
                location = geolocator.reverse(str(newGood.location_x) + " , " + str(newGood.location_y))
                newGood.locationString = location.address
            newGood.save()
            return HttpResponseRedirect('')
        raise Http404

    def post(self, request):
        user = request.user
        if user.is_authenticated() and user.is_active:
            postIdentifier = request.POST.get('post_identifier')
            if postIdentifier == 'comment':
                form = Comment_Form(request.POST)
                if form.is_valid():
                    text = request.POST.get('text')
                    if text is None or len(text) <= dcp.dcpSettings.MIN_COMMENT_LENGTH:
                        template = self.getTemplate(request)
                        return HttpResponseRedirect(template)
                    good = self.get_good_or_404(request)
                    knowledge = self.get_knowledge_or_404(request)
                    if good:
                        if good.comments is None:
                            good.comments = Comment_Relation.objects.create()
                            good.save()
                        good_relation = good.comments
                        Comment.objects.create(text=text,user=user,relation=good_relation)
                    else:
                        if knowledge.comments is None:
                            knowledge.comments = Comment_Relation.objects.create()
                            knowledge.save()
                        knowledge_relation = knowledge.comments
                        Comment.objects.create(text=text,user=user,relation=knowledge_relation)
                    
                    template = self.getTemplate(request)
                    return HttpResponseRedirect(template)

            if postIdentifier == 'contact_form':
                good = self.get_good_or_404(request)
                goodOwner =  good.user
                user = request.user
                # Schaue nach, ob schon eine Conv besteht..
                conv = Conversation.getConversationOrNone(userOne=user, userTwo=goodOwner)
                if conv is None: # Wenn noch keine Conversation da ist
                    Conversation.objects.create(Starter=user,Receiver=goodOwner)
                # Jetzt: Redirect
                url = '/chat/?userid='
                url += str(goodOwner.id)
                return HttpResponseRedirect(url)

            if postIdentifier == 'delete':
                good = self.get_good_or_404(request)
                if user.is_superuser or user == good.user:
                    good.delete()
                    template = self.getTemplate(request)
                    return HttpResponseRedirect(template)

            if postIdentifier == 'bump':
                good = self.get_good_or_404(request)
                if good.bumps is None:
                    good.bumps = Bump_Relation.objects.create()
                    good.save()
                else:
                    already_exists = Bump.objects.filter(relation = good.bumps, user = user)
                    if already_exists:
                        template = self.getTemplate(request)
                        return HttpResponseRedirect(template)
                relation = good.bumps
                Bump.objects.create(user=user,relation=relation)
                template = self.getTemplate(request)
                return HttpResponseRedirect(template)

            if postIdentifier == 'report':
                good = self.get_good_or_404(request)
                if user == good.user:
                    return HttpResponseForbidden('You cannot report yourself')
                relation = None
                if good.reports is None:
                    good.reports = Report_Relation.objects.create()
                    good.save()
                else:
                    already_exists = Report.objects.filter(relation = good.reports, user = user)
                    if already_exists:
                        template = self.getTemplate(request)
                        return HttpResponseRedirect(template)
                relation = good.reports
                Report.objects.create(user=user,relation=relation)
                template = self.getTemplate(request)
                return HttpResponseRedirect(template)

        return HttpResponse(status=403)
