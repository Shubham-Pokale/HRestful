# core/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Q
from .models import Department, Employee
from .forms import DepartmentForm, EmployeeForm
from django.views.generic import TemplateView
from django.db.models import Count

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add statistics to the context
        context['department_count'] = Department.objects.count()
        context['employee_count'] = Employee.objects.count()
        context['recent_employees'] = Employee.objects.order_by('-date_joined')[:5]
        context['recent_departments'] = Department.objects.order_by('-established_date')[:3]
        
          # Chart data
        departments = Department.objects.annotate(employee_count=Count('employees'))
        context['department_names'] = list(departments.values_list('name', flat=True))
        context['employee_counts'] = list(departments.values_list('employee_count', flat=True))
        
        return context

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'department_list.html' 
    context_object_name = 'departments'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search', '').strip()
        
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) |
                Q(code__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        
        return queryset.prefetch_related('employees')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('search', '')
        return context

class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    template_name = 'department_detail.html'
    context_object_name = 'department'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = self.object.employees.filter(is_active=True)
        return context

class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department_form.html'
    success_url = reverse_lazy('core:department-list')
    permission_required = 'core.add_department'
    success_message = "Department %(name)s was created successfully"
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department_form.html'
    permission_required = 'core.change_department'
    success_message = "Department %(name)s was updated successfully"
    
    def get_success_url(self):
        return reverse_lazy('core:department-detail', kwargs={'pk': self.object.pk})

class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Department
    template_name = 'department_confirm_delete.html'
    success_url = reverse_lazy('core:department-list')
    permission_required = 'core.delete_department'
    success_message = "Department was deleted successfully"
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        from django.contrib import messages
        messages.success(request, self.success_message)
        return response
    
class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('department')
        search_term = self.request.GET.get('search', '').strip()
        department_id = self.request.GET.get('department', '').strip()
        
        if search_term:
            queryset = queryset.filter(
                Q(last_name__icontains=search_term) |
                Q(first_name__icontains=search_term) |
                Q(email__icontains=search_term)
            )
        
        if department_id and department_id.isdigit():
            queryset = queryset.filter(department_id=int(department_id))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('search', '')
        context['departments'] = Department.objects.all()
        context['selected_department'] = self.request.GET.get('department', '')
        return context

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employee_detail.html'
    context_object_name = 'employee'
    
    def get_queryset(self):
        return super().get_queryset().select_related('department')

class EmployeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('core:employee-list')
    permission_required = 'core.add_employee'
    success_message = "Employee %(first_name)s %(last_name)s was created successfully"
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EmployeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    permission_required = 'core.change_employee'
    success_message = "Employee %(first_name)s %(last_name)s was updated successfully"
    
    def get_success_url(self):
        return reverse_lazy('core:employee-detail', kwargs={'pk': self.object.pk})

class EmployeeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('core:employee-list')
    permission_required = 'core.delete_employee'
    success_message = "Employee was deleted successfully"
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        from django.contrib import messages
        messages.success(request, self.success_message)
        return response