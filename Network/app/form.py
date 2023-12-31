from django.forms import ModelForm
from django.contrib.auth.models import User

# Create the form class.
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username","email","password"]