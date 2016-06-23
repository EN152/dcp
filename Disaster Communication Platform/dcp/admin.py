from django.contrib import admin

# Register models here.

from .models import Catastrophe, MissedPeople, Event, Car, Special
from .models import Search_Material, Search_Immaterial, Offer_Material, Offer_Immaterial

admin.site.register(Catastrophe)
admin.site.register(Search_Material)
admin.site.register(Search_Immaterial)
admin.site.register(Offer_Material)
admin.site.register(Offer_Immaterial)

admin.site.register(MissedPeople)
admin.site.register(Event)
admin.site.register(Car)
admin.site.register(Special)
