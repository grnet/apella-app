from django.forms import ModelForm
from apella.models import ApellaUser, Position, Candidacy

class ApellaUserForm(ModelForm):
    class Meta:
        model = ApellaUser
        fields = ['username', 'password', 'role']

class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'author', 'state', 'starts_at',
                  'ends_at', 'electors', 'committee', 'elected']

class CandidacyForm(ModelForm):
    class Meta:
        model = Candidacy
        fields = '__all__'
