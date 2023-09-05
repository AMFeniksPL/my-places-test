from django.forms import ModelForm
from .models import Place, Topic, File
from django.contrib.auth.forms import UserCreationForm
from .models import User

class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'description', 'isPrivate', 'accessPassword']

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']
