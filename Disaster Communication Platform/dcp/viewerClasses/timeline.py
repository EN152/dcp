# imports
from dcp.importUrls import *



class TimelineView(View):
    def getCreateNew(self, request, good_typ, show_radius, create_new_glyphicon, page_title):
        templatePath = 'dcp/content/createNewGood.html'
        goods_list = sorted(Goods.getAllGoods(), key=lambda g: g.created_date, reverse=True)
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
            'page_title': page_title
        }

        return HttpResponse(template.render(context,request))

    def get_good_or_404(self, request):
        good = Goods.getGood(request.POST['good_type'], request.POST['good_id'])
        #if good is None:
         #   raise Http404
        return good

    def post(self, request):
        user = request.user
        if user.is_authenticated() and user.is_active:
            postIdentifier = request.POST.get('post_identifier')
            if postIdentifier == 'comment':
                form = Comment_Form(request.POST)
                if form.is_valid():
                    text = request.POST['text']
                    good = self.get_good_or_404(request)
                    if good.comments is None:
                        good.comments = Comment_Relation.objects.create()
                        good.save()
                    relation = good.comments
                    Comment.objects.create(text=text,user=user,relation=relation)
                    return HttpResponseRedirect('')

            if postIdentifier == 'contact_form':
                good = self.get_good_or_404(request)
                creatingUser =  good.user
                requestingUser = request.user
                # Schaue nach, ob schon eine Conv besteht..
                conv = Conversation.getConversationOrNone(userOne=self.currentUser, userTwo=self.otherUser)
                if conv is None: # Wenn noch keine Conversation da ist
                    Conversation.objects.create(Starter=creatingUser,Receiver=requestingUser)
                # Jetzt: Redirect
                url = url_with_querystring(reverse('dcp:Chat'), userid=creatingUser.id)
                return HttpResponseRedirect(url)

            if postIdentifier == 'create':
                # TODO form.vaild oder eine art der Sicherung, dass die Daten korrekt sind
                radius = None
                if radius in request.POST:
                    radiusSplit = request.POST['radius'].split(' ')
                    radius = radiusSplit[0]
                good_type = Goods.stringToGoodClass(request.POST.get('good_typ', None))
                if good_type is None :
                    return HttpResponse(status=404)
                title = request.POST['title']
                description = request.POST['description']
                catastrophe = get_object_or_404(Catastrophe, id=request.POST['catastrophe'])
                location_x = request.POST['location_x']
                location_y = request.POST['location_y']
                categoryString = request.POST['category']
                if categoryString == '':
                    return HttpResponse(code=400) # TODO Einen Fehler zurueckgeben, der makiert, dass eine Option gewählt werden muss
                category = Categorys.stringToCategoryTypeAsNumber(categoryString)
                if radius is not None:
                    good_type.objects.create(title=title, description=description, radius=radius, catastrophe=catastrophe, location_x=location_x, location_y=location_y, category=category, user=user)
                else:
                    good_type.objects.create(title=title, description=description, catastrophe=catastrophe, location_x=location_x, location_y=location_y, category=category, user=user)
                return HttpResponseRedirect('')
                # else:
                    # return HttpResponse(status=500)

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
                    return HttpResponse(status=403)
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
