![Project Screenshot](assets/Screenshot.png)

A professional HR management system built with Django, designed to streamline employee and department management with clean, modern interfaces.

**Features**

- Department Management: Create, view, update, and delete departments

- Employee Management: Comprehensive employee records with CRUD operations

- User Authentication: Secure login/logout functionality

- Responsive Design: Works on all device sizes

- Modern UI: Clean, elegant interface with intuitive navigation


**Planned Features (Coming Soon)**

- Employee performance tracking

- Leave management system

- Document management

- Reporting and analytics

- Role-based access control

**Technologies Used**
- Backend: Django 4.2

- Database: PostgreSQL

- Frontend: HTML5, CSS3, JavaScript

- Deployment: Render.com

## Getting Started

Prerequisites

- Python 3.10+

- PostgreSQL 13+

- Git

Installation

Clone the repository

bash
git clone https://github.com/Shubham-Pokale/HRestful.git
cd HRestful

- Set up virtual environment


  - `python -m venv venv`
 
  - `venv\Scripts\activate`

- Install dependencies

  - `pip install -r requirements.txt`
  - `Configure environment variables`

- Create a .env file in the project root:`

    `DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://user:password@localhost:5432/hrestful`

Run migrations


`python manage.py migrate`
    
Create superuser

`python manage.py createsuperuser`

Run development server


`python manage.py runserver`

Deployment

This project is configured for easy deployment to Render.com. Follow these steps:

- Create a new Web Service on Render

- Connect your GitHub repository

- Add environment variables:

  - DEBUG: False

  - SECRET_KEY: Your secret key

  - DATABASE_URL: From your PostgreSQL service

Set build command:


`pip install -r requirements.txt && python manage.py collectstatic --noinput`

Set start command:

`gunicorn hrestful.wsgi`

Project Structure

**Contributing**

We welcome contributions! Please follow these steps:

-  Fork the repository

-  Create your feature branch (git checkout -b feature/AmazingFeature)

- Commit your changes (git commit -m 'Add some AmazingFeature')

- Push to the branch (git push origin feature/AmazingFeature)

- Open a Pull Request

**License**

Distributed under the MIT License. See LICENSE for more information.

**Contact*

Shubham Pokale - shubham.pokale@appzlogic.com