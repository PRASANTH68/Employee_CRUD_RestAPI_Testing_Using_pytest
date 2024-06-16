import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from employee.models import Employee

@pytest.mark.django_db
def test_create_employee():
    client = APIClient()
    url = reverse('employee-list')
    data = {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com', 'department': 'Engineering'}
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['first_name'] == 'John'
    assert response.data['last_name'] == 'Doe'
    assert response.data['email'] == 'john.doe@example.com'
    assert response.data['department'] == 'Engineering'

@pytest.mark.django_db
def test_get_employees():
    client = APIClient()
    url = reverse('employee-list')
    Employee.objects.create(first_name='John', last_name='Doe', email='john.doe@example.com', department='Engineering')
    Employee.objects.create(first_name='Jane', last_name='Smith', email='jane.smith@example.com', department='HR')
    response = client.get(url, format='json')
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['first_name'] == 'John'
    assert response.data[1]['first_name'] == 'Jane'

@pytest.mark.django_db
def test_update_employee():
    client = APIClient()
    employee = Employee.objects.create(first_name='John', last_name='Doe', email='john.doe@example.com', department='Engineering')
    url = reverse('employee-detail', kwargs={'pk': employee.id})
    data = {'first_name': 'Johnny', 'last_name': 'Doe', 'email': 'john.doe@example.com', 'department': 'Engineering'}
    response = client.put(url, data, format='json')
    assert response.status_code == 200
    assert response.data['first_name'] == 'Johnny'
    assert response.data['last_name'] == 'Doe'
    assert response.data['email'] == 'john.doe@example.com'
    assert response.data['department'] == 'Engineering'

@pytest.mark.django_db
def test_delete_employee():
    client = APIClient()
    employee = Employee.objects.create(first_name='John', last_name='Doe', email='john.doe@example.com', department='Engineering')
    url = reverse('employee-detail', kwargs={'pk': employee.id})
    response = client.delete(url)
    assert response.status_code == 204
    assert Employee.objects.count() == 0
