from enum import unique
from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    abstract = models.TextField()
    published = models.BooleanField()
    rating = models.IntegerField()
    pub_date = models.DateField()

    def __str__(self):
        return str(self.title)


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class Student(models.Model):
    username = models.CharField(max_length=100)
    city = models.CharField(max_length=10)
    college = models.CharField(max_length=300)
    branch = models.CharField(max_length=100)


class StudentNew(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class InternshipDomain(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name="internship_domains")

    def __str__(self):
        return str(self.name)


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    feedback = models.TextField()

    def __str__(self):
        return str(self.email)
