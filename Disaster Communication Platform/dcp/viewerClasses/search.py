# imports
from dcp.importUrls import *

class Suchen(View):
    template = 'dcp/content/suchen/suchen.html'

    def get(self, request):
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)

