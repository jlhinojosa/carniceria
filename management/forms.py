# import form class from django
from django import forms

# import GeeksModel from models.py
from .models import *

# create a ModelForm
class VenueForm(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = Venue
		fields = "__all__"
		exclude = ['owner']

class DrawerForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(DrawerForm, self).__init__(*args, **kwargs)                       
		self.fields['venue'].disabled = True

	class Meta:
		model = Drawer
		fields = "__all__"
