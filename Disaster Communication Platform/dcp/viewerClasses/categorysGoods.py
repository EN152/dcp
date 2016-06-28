from django.views.generic import View
from django.views.static import loader
from dcp.customForms.categorysGoodsForms import CategorysGoodsForms
from django.http.response import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from dcp.models.categorysGoods import CategorysGoods


class CategorysGoodsMangerView(View):
    """description of class"""
    def get(self, request, create_new_form=None):
        templatePath = 'dcp/content/adminstrator/categorysGoodsManager.html'
        template = loader.get_template(templatePath)
        if create_new_form is None:
            create_new_form = CategorysGoodsForms
        user = request.user
        if not(user.is_authenticated() and user.is_active and user.is_superuser):
            raise HttpResponseForbidden()
        category_list = CategorysGoods.objects.all()

        context = {
            'create_new_form' : create_new_form,
            'category_list' : category_list
        }
        return HttpResponse(template.render(context, request))
        
    def post(self, request):
        user = request.user
        if not(user.is_authenticated() and user.is_active and user.is_superuser):
           raise HttpResponseForbidden()
        post_identifier = request.POST.get('post_identifier')
        if post_identifier == 'create':
            form = CategorysGoodsForms(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dcp:CategoryGoodManagerView')
            else:
                return self.get(request, create_new_form=form)
        if post_identifier == 'delete':
            category = get_object_or_404(CategorysGoods, name=request.POST.get('category_name'))
            category.delete()
            return redirect('dcp:CategoryGoodManagerView')
        raise HttpResponseBadRequest()