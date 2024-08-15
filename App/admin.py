from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(StudentNew)
admin.site.register(InternshipDomain)
admin.site.register(Publisher)

"""
Admin Interface
    why do we need it?
        1. Easy management of database contents
        2. Ease of performing Admin activities
        3. Rapid development and prototyping
        4. Built-in user authentication and authorization
"""
