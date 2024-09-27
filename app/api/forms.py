from django import forms

class ConsultaMantisForm(forms.Form):
    issue_id = forms.CharField(label='Issue ID', max_length=100, required=True)

    def clean_issue_id(self):
        issue_id = self.cleaned_data.get('issue_id')
        if not issue_id.isdigit():
            raise forms.ValidationError("O Issue ID deve ser numérico.")
        return issue_id
