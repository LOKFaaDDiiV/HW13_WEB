from django.forms import SelectDateWidget, DateField, ModelForm, CharField, TextInput, Textarea, ModelChoiceField, MultipleChoiceField, Select, SelectMultiple, TextInput, ModelMultipleChoiceField
from .models import Tag, Quote, Author
from datetime import datetime


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    quote_text = CharField(max_length=200, widget=Textarea)
    author = ModelChoiceField(queryset=Author.objects.all(), widget=Select())
    # tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), required=True, widget=SelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].label_from_instance = lambda obj: obj.fullname

    class Meta:
        model = Quote
        fields = ['quote_text', 'author']
        exclude = ['tags']


class AuthorForm(ModelForm):
    fullname = CharField(max_length=50)
    born_date = DateField(widget=SelectDateWidget(years=[str(i) for i in range(1600, int(datetime.now().year)+1)]))
    born_location = CharField(max_length=35)
    description = CharField(max_length=5000, widget=Textarea)

    class Meta:
        model = Author
        fields = '__all__'
