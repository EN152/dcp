from django.forms import CharField, TextInput, ModelForm
from dcp.models.categorysGoods import CategorysGoods

class CategorysGoodsForms(ModelForm):
    """description of class"""
    name = CharField(required=True, label='Name', widget=TextInput(attrs={'palcehoder': 'Lebensmittel'}))
    glyphiconString = CharField(required=True, label='Glyphicon String', widget=TextInput(attrs={'placeholder': 'glyphicon glyphicon-cutlery', 'helptext:': 'Wähle eine Glyphicon aus den Bootstrap Elementen'}))
    class Meta:
        model = CategorysGoods
        fields =["name", "glyphiconString"]