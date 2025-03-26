from django.db import models
from datetime import datetime


class Genre(models.Model):
    name = models.CharField("სახელი", max_length=50, blank=False, null=False)
    description = models.TextField("აღწერა", blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField("სათაური", max_length=100, blank=False, null=False)
    author = models.CharField("ავტორი", max_length=100, blank=False, null=False)
    description = models.TextField("აღწერა", blank=True, null=True)
    publish_date = models.DateTimeField("გამოცემის თარიღი", blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    borrowed_by = models.CharField(max_length=100, blank=True, null=True)
    borrow_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def borrow(self, person):
        self.borrowed_by = person
        self.borrow_date = datetime.now()
        self.save()

    def return_book(self):
        self.borrowed_by = None
        self.borrow_date = None
        self.save()