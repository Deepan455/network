from django import forms

class Postform(forms.Form):
	content = forms.CharField(label='content',widget=forms.Textarea)
	image = forms.ImageField()
	widgets = {
		'content':forms.TextInput(attrs={'placeholder':'Your text here...'})
	}
