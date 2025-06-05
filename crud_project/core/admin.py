from django.contrib import admin
from .models import Department, Employee
from django.utils.html import format_html
# Register your models here.

class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 0
    fields = ['full_name', 'email', 'job_level', 'is_active']
    readonly_fields = ['full_name']
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'
    
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'employee_count', 'budget_formatted')
    search_fields = ('name', 'code')
    list_filter = ('established_date',)
    inlines = [EmployeeInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'description')
        }),
        ('Financials', {
            'fields': ('budget', 'established_date'),
            'classes': ('collapse',)
        }),
    )
    
    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = 'Employees'
    
    def budget_formatted(self, obj):
        return f"${obj.budget:,.2f}"
    budget_formatted.short_description = 'Budget'
    budget_formatted.admin_order_field = 'budget'
    
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'department', 'job_level_display', 'is_active', 'salary_formatted')
    list_filter = ('department', 'job_level', 'is_active', 'date_joined')
    search_fields = ('last_name', 'first_name', 'email')
    list_select_related = ('department',)
    list_editable = ('is_active',)
    fieldsets = (
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Employment', {
            'fields': ('department', 'date_joined', 'salary', 'job_level', 'is_active')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def job_level_display(self, obj):
        return obj.get_job_level_display()
    job_level_display.short_description = 'Job Level'
    
    def salary_formatted(self, obj):
        return f"${obj.salary:,.2f}"
    salary_formatted.short_description = 'Salary'
    salary_formatted.admin_order_field = 'salary'