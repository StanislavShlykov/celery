from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'post_name',
            'post_text',
            'category',
            'author',
        ]



    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("post_text")
        if text is not None and len(text) < 50:
            raise ValidationError({
                "post_text": "Текст статьи не может быть менее 50 символов."
            })

        name = cleaned_data.get("post_name")
        if name == text:
            raise ValidationError(
                "Текст статьи не должен быть идентичен названию."
            )

        return cleaned_data
