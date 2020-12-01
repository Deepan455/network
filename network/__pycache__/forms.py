from django import forms

class Postform(forms.Form):
	content = forms.CharField(label='content',widget=forms.TextInput(attrs={'placeholder':'Your text here...'}))
	image = forms.ImageField(upload_to='media/',null=True)