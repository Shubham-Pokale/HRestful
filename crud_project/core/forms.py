from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Department, Employee
from django.contrib.auth import get_user_model

User = get_user_model()

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'established_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_code(self):
        code = self.cleaned_data['code']
        return code.upper()
    
    def clean_budget(self):
        budget = self.cleaned_data['budget']
        if budget < 0:
            raise ValidationError("Budget cannot be negative")
        return budget

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
        }
        exclude = ['created_by', 'created_at', 'updated_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()
        self.fields['date_joined'].initial = timezone.now().date()
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if Employee.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("An employee with this email already exists")
        return email
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        if dob > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future")
        return dob
    
    def clean(self):
        cleaned_data = super().clean()
        date_joined = cleaned_data.get('date_joined')
        date_of_birth = cleaned_data.get('date_of_birth')
        
        if date_joined and date_of_birth:
            if date_joined < date_of_birth:
                raise ValidationError("Date joined cannot be before date of birth")
            
            age_at_joining = (date_joined - date_of_birth).days / 365
            if age_at_joining < 18:
                raise ValidationError("Employee must be at least 18 years old when joining")
        
        return cleaned_data