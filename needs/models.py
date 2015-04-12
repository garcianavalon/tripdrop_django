from django.core.urlresolvers import reverse
from django.db import models

from django_countries.fields import CountryField


class ContactPerson(models.Model):
    name = models.CharField(max_length=50)
    relation_with_institution = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=20)


class Region(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Need(models.Model):
    NEED_TYPES = (
        ('MA', 'Material'),
        ('SE', 'Sevicios(talleres/voluntariado)'),
    )
    need_type = models.CharField(
        max_length=2, choices=NEED_TYPES)
    country = CountryField()
    region = models.ForeignKey(Region)
    city = models.ForeignKey(City)
    petition = models.CharField(max_length=500)
    places_to_visit = models.CharField(max_length=300)
    created_at = models.DateTimeField('date published', auto_now_add=True)
    modified_at = models.DateTimeField('date last modified', auto_now=True)
    
    contact_persons = models.ManyToManyField(ContactPerson)
    # TODO(garcianavalon) geo localization
    # TODO(garcianavalon) 0+ images
    # TODO(garcianavalon) 0+ youtube videos

    def get_absolute_url(self):
        return reverse('needs:detail', kwargs={'need_id': self.pk})

class Institution(models.Model):
    INSTITUTION_TYPES = (
        ('ED', 'Educativo'),
        ('SA', 'Sanitario'),
        ('SO', 'Social'),
        ('ON', 'ONG'),
        ('RE', 'Religioso'),
        ('OT', 'Otros'),
    )
    institution_type = models.CharField(
        max_length=2, choices=INSTITUTION_TYPES)
    name = models.CharField(max_length=20)
    needs = models.ManyToManyField(Need)
    description = models.CharField(max_length=300)

        