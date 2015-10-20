from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm
from django.template.defaultfilters import slugify

from django_countries.fields import CountryField


class ContactPerson(models.Model):
    name = models.CharField(max_length=50)
    relation_with_institution = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=20)


class Municipality(models.Model):
    country = CountryField()
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class InstitutionType(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Need(models.Model):
    NEED_TYPES = (
        ('MA', 'Material'),
        ('SE', 'Sevicios(talleres/voluntariado)'),
    )
    institution_type = models.ManyToManyField(InstitutionType)
    institution_description = models.CharField(max_length=300)
    title = models.CharField(max_length=40)
    need_type = models.CharField(
        max_length=2, choices=NEED_TYPES)
    petition = models.CharField(max_length=500)
    places_to_visit = models.CharField(max_length=300)
    created_at = models.DateTimeField('date published', auto_now_add=True)
    modified_at = models.DateTimeField('date last modified', auto_now=True)
    municipality = models.ForeignKey(Municipality)
    contact_persons = models.ManyToManyField(ContactPerson, blank=True)
    slug = models.SlugField(editable=False)
    # geolocation
    postal_address = models.CharField(max_length=300, blank=True)
    lat = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    # TODO(garcianavalon) 0+ images
    # TODO(garcianavalon) 0+ youtube videos

    def get_absolute_url(self):
        return reverse('needs:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        super(Need, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
    
        