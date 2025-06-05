from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from .static.constants import DEPARTMENT_CODE_VALIDATION_MESSAGE, PHONE_NO_VALIDATION_MESSAGE

# Create your models here.

class Department(models.Model):
    """Department model representing different company departments"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^[A-Z]{2,10}$', DEPARTMENT_CODE_VALIDATION_MESSAGE)]
    )
    description = models.TextField(blank=True)
    established_date = models.DateField()
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_absolute_url(self):
        return reverse('department-detail', kwargs={'pk': self.pk})
    

class Employee(models.Model):
    """Employee model representing company employees"""
    class JobLevel(models.IntegerChoices):
        ENTRY = 1, 'Entry Level'
        MID = 2, 'Mid Level'
        SENIOR = 3, 'Senior'
        LEAD = 4, 'Lead'
        MANAGER = 5, 'Manager'
        DIRECTOR = 6, 'Director'
        VP = 7, 'Vice President'
        EXECUTIVE = 8, 'Executive'
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', PHONE_NO_VALIDATION_MESSAGE)]
    )
    date_of_birth = models.DateField()
    date_joined = models.DateField()
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    job_level = models.IntegerField(choices=JobLevel.choices, default=JobLevel.ENTRY)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['email']),
            models.Index(fields=['department']),
        ]
        
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    
    def get_absolute_url(self):
        return reverse('employee-detail', kwargs={'pk': self.pk})
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)