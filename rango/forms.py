from django import forms
from rango.models import Category, Page

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length = 50, help_text = 'Please enter the category name.')
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length = 100, help_text = 'Please enter the title of the page.')
    url = forms.URLField(max_length = 200, help_text = 'Please enter the URL of the page.')
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)

    def clean(self):
        # We should call the parent class' clean() method because we have a unique field
        super(PageForm, self).clean()
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        print url
        if url and not url.startswith('http://'):
            url += 'http://'

        cleaned_data['url'] = url
        return cleaned_data

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some field may allow NULL values, so we may not want to include them...
        # Here we are hiding the foreign key.
        fields = ('title', 'url', 'views')
