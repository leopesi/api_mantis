from django import forms

class ConsultaMantisForm(forms.Form):
    issue_id = forms.CharField(
        label='ID do Problema',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o ID do problema'})
    )

    def clean_issue_id(self):
        issue_id = self.cleaned_data.get('issue_id')
        if not issue_id.isdigit():
            raise forms.ValidationError("O input deve ser numérico.")
        return issue_id