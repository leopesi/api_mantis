"""from django import forms

class MantisIssueForm(forms.Form):
    issue_id = forms.CharField(
        label="ID da Issue",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Adiciona classes de estilo
            'placeholder': 'Digite o ID da Issue',
            'required': True
        })
    )
"""

from django import forms

class MantisIssueForm(forms.Form):
    issue_id = forms.CharField(label="ID da Issue", max_length=100, required=True)
