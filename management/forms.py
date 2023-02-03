# import form class from django
from decimal import Decimal
from datetime import datetime
from itertools import zip_longest

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.utils.translation import gettext as _

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

class DrawerClosingForm(forms.Form):

	getnet = forms.DecimalField(max_digits=10, decimal_places=0)
	carnes = forms.DecimalField(max_digits=10, decimal_places=0)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.drawer_id = kwargs.pop('initial').get('drawer')
		denominations = Denomination.objects.filter(type='Bill').order_by('displayOrder')
		i = 1
		for denom in denominations:
			field_name = 'bill_%s' % denom.value
			self.fields[field_name] = forms.DecimalField(required=False,max_digits=10, decimal_places=0, validators=[RegexValidator()])
			self.fields[field_name].label = denom.value
			try:
				self.initial[field_name] = 0
			except IndexError:
				self.initial[field_name] = ''
			i += 1
		denominations = Denomination.objects.filter(type='Coin').order_by('displayOrder')
		i = 1
		for denom in denominations:
			field_name = 'coin_%s' % denom.value
			self.fields[field_name] = forms.DecimalField(required=False,max_digits=10, decimal_places=0)
			self.fields[field_name].label = denom.value
			try:
				self.initial[field_name] = 0
			except IndexError:
				self.initial[field_name] = ''
			i += 1

	def clean(self):

		cleaned_data = super(DrawerClosingForm, self).clean()

		for field in list(cleaned_data):
			if field.startswith('bill_') or field.startswith('coin_'):
				denom = field
				value = cleaned_data[field]
				denom = field[5:]

				if(value != 0 and value % Decimal(denom) != 0):
					self.add_error(field, ValidationError(_('Invalid Amount. It shoulb be multiple of %(field)s'), params={'field': denom}))

		return cleaned_data

	def save(self):
		
		totalAmount = 0

		details = []

		denominations = Denomination.objects.all()

		instance = ClosingBalance(
				dateTime=datetime.now(),
				drawer_id = self.drawer_id, 
				totalCarnes = self.cleaned_data['carnes'], 
				totalGetnet = self.cleaned_data['getnet']
		)

		for field in self.cleaned_data:

			if field.startswith('bill_') or field.startswith('coin_'):
				denom = denominations.filter(value = field[5:])
				fieldValue = self.cleaned_data[field]

				detail = ClosingBalanceDetail(totalAmount = fieldValue, denomination = denom.get())
				details.append(detail)
				totalAmount += fieldValue


		totalAmount += self.cleaned_data['getnet'] + self.cleaned_data['carnes']
		instance.totalCashAmount = totalAmount

		instance.save()
		for detail in details:
			detail.balance = instance
			detail.save()

	def get_bills(self):
		for field_name in self.fields:
			print(field_name)
			if field_name.startswith('bill_'):
				yield self[field_name]
	
	def get_coins(self):
		for field_name in self.fields:
			print(field_name)
			if field_name.startswith('coin_'):
				yield self[field_name]