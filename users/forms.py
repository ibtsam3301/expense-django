from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = '__all__'

	def save(self, commit=True, **extra_fields):
     
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(self.email)
		user = self.model(email=email, **extra_fields)
		user.set_password(self.password)
		user.save(using=self._db)
		return user