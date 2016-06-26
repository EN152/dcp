from django.forms import CharField, TextInput, ModelForm
from dcp.models.categorysGoods import CategorysGoods

class CategorysGoodsForms(ModelForm):
    """description of class"""
    name = CharField(required=True, label='Name', widget=TextInput(attrs={'placeholder': 'Lebensmittel'}))
    glyphiconString = CharField(required=True, label='Glyphicon String', help_text = 'Wähle ein Glyphicon aus den o.g. Elementen.', widget=TextInput(attrs={'placeholder': 'glyphicon glyphicon-cutlery'}))
    class Meta:
        model = CategorysGoods
        fields =["name", "glyphiconString"]