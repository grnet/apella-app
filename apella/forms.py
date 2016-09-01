from django.forms import ModelForm
from apella.models import ApellaUser, Position, Candidacy,\
        Institution

class ApellaUserForm(ModelForm):
    class Meta:
        model = ApellaUser
        fields = ['username', 'password', 'role']

class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = '__all__'

class CandidacyForm(ModelForm):
    class Meta:
        model = Candidacy
        fields = '__all__'

class InstitutionForm(ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'
