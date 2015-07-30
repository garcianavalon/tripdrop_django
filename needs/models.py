from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm
from django.template.defaultfilters import slugify

from django_countries.fields import CountryField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ContactPerson(models.Model):
    name = models.CharField(max_length=50)
    relation_with_institution = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=20)

class Country(models.Model):
    name = CountryField()

class Municipality(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=20)

class Need(models.Model):
    NEED_TYPES = (
        ('MA', 'Material'),
        ('SE', 'Sevicios(talleres/voluntariado)'),
    )
    title = models.CharField(max_length=40)
    need_type = models.CharField(
        max_length=2, choices=NEED_TYPES)
    petition = models.CharField(max_length=500)
    places_to_visit = models.CharField(max_length=300)
    created_at = models.DateTimeField('date published', auto_now_add=True)
    modified_at = models.DateTimeField('date last modified', auto_now=True)
    country = models.ForeignKey(Country)
    municipality = models.ForeignKey(Municipality)
    contact_persons = models.ManyToManyField(ContactPerson, blank=True)
    slug = models.SlugField(editable=False)
    # TODO(garcianavalon) geo localization
    # TODO(garcianavalon) 0+ images
    # TODO(garcianavalon) 0+ youtube videos

    def get_absolute_url(self):
        return reverse('needs:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        super(Need, self).save(*args, **kwargs)

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

# ModelForms
class NeedForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(NeedForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Need
        # TODO(garcianavalon) this is ok for prototyping but should set explicit
        # fields for production to avoid security vulnerabilities
        fields = '__all__'

        