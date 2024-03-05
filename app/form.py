from django import forms

from app.models import ProfileImg


class ImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImg
        fields = ('user_image',)
