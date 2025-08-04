from django import forms

class FavoriteRepoForm(forms.Form):
    repo_name = forms.CharField(widget=forms.HiddenInput)
    repo_owner = forms.CharField(widget=forms.HiddenInput)
    repo_url = forms.URLField(widget=forms.HiddenInput)
    description = forms.CharField(widget=forms.HiddenInput, required=False)