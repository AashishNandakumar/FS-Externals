from django import forms
from .models import *


class StudentNewRegistrationForm(forms.ModelForm):
    class Meta:
        model = StudentNew
        fields = "__all__"


class FeedbackForm(forms.Form):
    # specify fields and validation rules
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    feedback = forms.CharField(widget=forms.Textarea, required=True)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name.isalpha():
            raise forms.ValidationError("Name must only contain letters!")

        return name

    def clean_feedback(self):
        feedback = self.cleaned_data.get("feedback")
        if len(feedback) < 10:
            raise forms.ValidationError("Feedback must be atleast 10 characters long!")

        return feedback

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        email = cleaned_data.get("email")
        if name and email:
            if name.lower() in email.lower():
                raise forms.ValidationError(
                    "email must not contain your name for privacy reasons"
                )
        return cleaned_data
