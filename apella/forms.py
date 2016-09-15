from django.forms import ModelForm
from apella.models import ApellaUser, Position, Candidacy,\
        Institution, Department, Registry, SubjectArea, Subject


class ApellaUserForm(ModelForm):
    class Meta:
        model = ApellaUser
        fields = ['username', 'password', 'role']


class PositionForm(ModelForm):
    position_code = 'APELLA'

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


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class RegistryForm(ModelForm):
    class Meta:
        model = Registry
        fields = '__all__'


class SubjectAreaForm(ModelForm):
    class Meta:
        model = SubjectArea
        fields = '__all__'


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
