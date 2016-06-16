# imports
from dcp.importUrls import *
from django.http import Http404
import dcp.dcpSettings



class TimelineView(View):
    def getCreateNew(self, request, good_typ, show_radius, show_categorys, create_new_glyphicon, page_title):
        templatePath = 'dcp/content/createNewGood.html'
        goods_list = sorted(Goods.getAllGoods(), key=lambda g: g.created_date, reverse=True)
        goods_list = filter(lambda x: type(x) is eval(good_typ), goods_list)

        category_glyphicon_list = Categorys.getCategoryListAsGlyphiconString()
        category_name_list = Categorys.getCategoryListAsNameString()

        category_list = zip(category_glyphicon_list, category_name_list)
            
        template = loader.get_template(templatePath)
        context = {
            'goods_list': goods_list,
            'category_list' : category_list,
            'show_radius' : show_radius,
            'create_new_good_typ' : good_typ,
            'create_new_glyphicon': create_new_glyphicon,
            'page_title': page_title,
            'show_categorys' : show_categorys,
        }

        return HttpResponse(template.render(context,request))

    def get_good_or_404(self, request):
        good = Goods.getGood(request.POST.get('good_type'), request.POST.get('good_id'))
        if good is None:
           raise Http404
        return good

    def post(self, request):
        user = request.user
        if user.is_authenticated() and user.is_active:
            postIdentifier = request.POST.get('post_identifier')
            if postIdentifier == 'comment':
                form = Comment_Form(request.POST)
                if form.is_valid():
                    text = request.POST.get('text')
                    if text is None or len(text) <= dcp.dcpSettings.MIN_COMMENT_LENGTH:
                        return HttpResponseRedirect('')
                    good = self.get_good_or_404(request)
                    if good.comments is None:
                        good.comments = Comment_Relation.objects.create()
                        good.save()
                    relation = good.comments
                    Comment.objects.create(text=text,user=user,relation=relation)
                    return HttpResponseRedirect('')

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
                    if good.comments is not None:
                        good.comments.delete()
                    if good.bumps is not None:
                        good.bumps.delete()
                    if good.reports is not None:
                        good.reports.delete()
                    good.delete()
                    return HttpResponseRedirect('')

            if postIdentifier == 'bump':
                good = self.get_good_or_404(request)
                if good.bumps is None:
                    good.bumps = Bump_Relation.objects.create()
                    good.save()
                else:
                    already_exists = Bump.objects.filter(relation = good.bumps, user = user)
                    if already_exists:
                        return HttpResponseRedirect('')
                relation = good.bumps
                Bump.objects.create(user=user,relation=relation)
                return HttpResponseRedirect('')

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
                        return HttpResponseRedirect('')
                relation = good.reports
                Report.objects.create(user=user,relation=relation)
                return HttpResponseRedirect('')

        return HttpResponse(status=403)
