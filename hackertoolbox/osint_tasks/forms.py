from django import forms

class ConfigForm(forms.Form):
    google_api = forms.CharField(label='Google developper api', max_length=100, initial='class')
    google_cse_id = forms.CharField(label='Google custom search engine id', max_length=100, initial='class')
    shodan_api_key = forms.CharField(label='Shodan api key', max_length=100, initial='class')
