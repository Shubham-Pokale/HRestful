from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.messages.storage.fallback import FallbackStorage
from .models import Department, Employee
from .forms import DepartmentForm, EmployeeForm
from .views import DepartmentCreateView, EmployeeCreateView

class DepartmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name="Engineering",
            code="ENG",
            description="Software development department",
            established_date="2020-01-01",
            budget=1000000.00
        )
    
    def test_department_creation(self):
        self.assertEqual(self.department.name, "Engineering")
        self.assertEqual(self.department.code, "ENG")
        self.assertEqual(self.department.budget, 1000000.00)
    
    def test_department_str_representation(self):
        self.assertEqual(str(self.department), "Engineering (ENG)")
    
    def test_department_get_absolute_url(self):
        url = self.department.get_absolute_url()
        self.assertEqual(url, f"/departments/{self.department.pk}/")

class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name="HR",
            code="HRD",
            description="Human Resources",
            established_date="2020-01-01",
            budget=500000.00
        )
        cls.employee = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="+1234567890",
            date_of_birth="1990-01-01",
            date_joined="2020-01-01",
            salary=75000.00,
            job_level=2,
            department=cls.department
        )
    
    def test_employee_creation(self):
        self.assertEqual(self.employee.first_name, "John")
        self.assertEqual(self.employee.last_name, "Doe")
        self.assertEqual(self.employee.email, "john.doe@example.com")
        self.assertEqual(self.employee.department.name, "HR")
    
    def test_employee_full_name_property(self):
        self.assertEqual(self.employee.full_name, "John Doe")
    
    def test_employee_email_normalization(self):
        employee = Employee.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="Jane.Smith@Example.COM",
            phone="+1234567891",
            date_of_birth="1991-01-01",
            date_joined="2020-01-02",
            salary=80000.00,
            job_level=3,
            department=self.department
        )
        self.assertEqual(employee.email, "jane.smith@example.com")

class DepartmentFormTest(TestCase):
    def test_department_form_valid_data(self):
        form = DepartmentForm(data={
            'name': 'Marketing',
            'code': 'MKT',
            'description': 'Marketing department',
            'established_date': '2020-01-01',
            'budget': 500000.00
        })
        self.assertTrue(form.is_valid())
    
    def test_department_form_invalid_budget(self):
        form = DepartmentForm(data={
            'name': 'Marketing',
            'code': 'MKT',
            'description': 'Marketing department',
            'established_date': '2020-01-01',
            'budget': -100.00
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['budget'], ['Budget cannot be negative'])
    
    def test_department_form_code_normalization(self):
        form = DepartmentForm(data={
            'name': 'Marketing',
            'code': 'mkt',
            'description': 'Marketing department',
            'established_date': '2020-01-01',
            'budget': 500000.00
        })
        self.assertTrue(form.is_valid())
        department = form.save()
        self.assertEqual(department.code, 'MKT')

class DepartmentViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        permission = Permission.objects.get(codename='add_department')
        cls.user.user_permissions.add(permission)
        
        cls.department = Department.objects.create(
            name='Engineering',
            code='ENG',
            description='Engineering department',
            established_date='2020-01-01',
            budget=1000000.00
        )
    
    def setUp(self):
        self.client.login(username='testuser', password='testpass123')
    
    def test_department_list_view(self):
        response = self.client.get(reverse('core:department-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engineering')
        self.assertTemplateUsed(response, 'core/department_list.html')
    
    def test_department_create_view(self):
        response = self.client.post(reverse('core:department-create'), {
            'name': 'Marketing',
            'code': 'MKT',
            'description': 'Marketing department',
            'established_date': '2020-01-01',
            'budget': 500000.00
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Department.objects.count(), 2)
        self.assertEqual(Department.objects.last().name, 'Marketing')
    
    def test_department_create_view_invalid_data(self):
        response = self.client.post(reverse('core:department-create'), {
            'name': '',
            'code': 'MKT',
            'description': 'Marketing department',
            'established_date': '2020-01-01',
            'budget': 500000.00
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        self.assertEqual(Department.objects.count(), 1)

class EmployeeViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        permission = Permission.objects.get(codename='add_employee')
        cls.user.user_permissions.add(permission)
        
        cls.department = Department.objects.create(
            name='Engineering',
            code='ENG',
            description='Engineering department',
            established_date='2020-01-01',
            budget=1000000.00
        )
    
    def setUp(self):
        self.client.login(username='testuser', password='testpass123')
    
    def test_employee_create_view(self):
        response = self.client.post(reverse('core:employee-create'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'date_of_birth': '1990-01-01',
            'date_joined': '2020-01-01',
            'salary': 75000.00,
            'job_level': 2,
            'department': self.department.pk,
            'is_active': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.first().full_name, 'John Doe')
    
    def test_employee_create_view_invalid_email(self):
        Employee.objects.create(
            first_name='Existing',
            last_name='User',
            email='existing@example.com',
            phone='+1234567891',
            date_of_birth='1990-01-01',
            date_joined='2020-01-01',
            salary=80000.00,
            job_level=3,
            department=self.department
        )
        response = self.client.post(reverse('core:employee-create'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'existing@example.com',
            'phone': '+1234567890',
            'date_of_birth': '1990-01-01',
            'date_joined': '2020-01-01',
            'salary': 75000.00,
            'job_level': 2,
            'department': self.department.pk,
            'is_active': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'An employee with this email already exists')
        self.assertEqual(Employee.objects.count(), 1)

class PermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.department = Department.objects.create(
            name='Engineering',
            code='ENG',
            description='Engineering department',
            established_date='2020-01-01',
            budget=1000000.00
        )
    
    def test_department_create_view_no_permission(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('core:department-create'))
        self.assertEqual(response.status_code, 403)
    
    def test_department_create_view_with_permission(self):
        permission = Permission.objects.get(codename='add_department')
        self.user.user_permissions.add(permission)
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('core:department-create'))
        self.assertEqual(response.status_code, 200)