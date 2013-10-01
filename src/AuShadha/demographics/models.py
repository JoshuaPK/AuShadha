################################################################################
# Description  : Patient Models for managing Patient Demographics & Contact 
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

from django.db import models
from django.contrib.auth.models import User

from AuShadha.settings import APP_ROOT_URL
from AuShadha.utilities.urls import UrlGenerator, generic_url_maker

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm
from patient.models import PatientDetail

from dijit_fields_constants import CONTACT_FORM_CONSTANTS,    \
                                   GUARDIAN_FORM_CONSTANTS,   \
                                   PHONE_FORM_CONSTANTS,      \
                                   EMAIL_AND_FAX_FORM_CONSTANTS,\
                                   DEMOGRAPHICS_FORM_CONSTANTS

DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES = ('patient_detail',)



class Contact(AuShadhaBaseModel):

    """
      Class that defines the Contact Address of a particular patient.
    """

    def __init__(self, *args, **kwargs):
      super(Contact,self).__init__(*args, **kwargs)
      self.__model_label__ = "contact"
      self._parent_model = 'patient_detail'

    address_type = models.CharField('Type',
                                    max_length=10,
                                    choices=(("Home", "Home"),
                                             ("Office", "Office"),
                                             ("Others", "Others")
                                             ),
                                    default = "Home")
    address = models.TextField(max_length=100,
                               help_text='limit to 100 words'
                               )
    city = models.CharField(max_length=20,
                            default='Coimbatore'
                            )
    state = models.CharField(max_length=20,
                             default="Tamil Nadu"
                             )
    country = models.CharField(max_length=20,
                               default="India"
                               )
    pincode = models.PositiveIntegerField(max_length=8,
                                          null=True,
                                          blank=True
                                              )
    patient_detail = models.ForeignKey(PatientDetail,
                                       null=True,
                                       blank=True
                                       )

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Address"
        ordering = ('patient_detail', 'city', 'state')

    def __unicode__(self):
        if self.pincode:
            return "%s, %s, %s, %s - %s" % (self.address,
                                            self.city,
                                            self.state,
                                            self.country,
                                            self.pincode
                                            )
        else:
            return "%s, %s, %s, %s" % (self.address,
                                       self.city,
                                       self.state,
                                       self.country
                                       )

    def _field_list(self):
        self.field_list = []
        print self._meta.fields
        for field in self._meta.fields:
            self.field_list.append(field)
        return self.field_list

    def _formatted_obj_data(self):
        if not self.field_list:
            _field_list()
        str_obj = "<ul>"
        for obj in self._field_list:
            _str += "<li>" + obj + "<li>"
            str_obj += _str
        str_obj += "</ul>"
        return str_obj


class Phone(AuShadhaBaseModel):

    """
      Class that defines the Phone data of a patient.
    """

    def __init__(self, *args, **kwargs):
      super(Phone,self).__init__(*args, **kwargs)
      self.__model_label__ = "phone"
      self._parent_model = 'patient_detail'

    phone_type = models.CharField('Type',
                                  max_length=10,
                                  choices=(("Home", "Home"),
                                           ("Office", "Office"),
                                           ("Mobile", "Mobile"),
                                           ("Fax", "Fax"),
                                           ("Others", "Others")
                                           ),
                                  default = "Home")
    ISD_Code = models.PositiveIntegerField('ISD',
                                           max_length=4,
                                           null=True,
                                           blank=True,
                                           default="0091"
                                           )
    STD_Code = models.PositiveIntegerField('STD',
                                           max_length=4,
                                           null=True,
                                           blank=True,
                                           default="0422"
                                           )
    phone = models.PositiveIntegerField(max_length=10,
                                        null=True,
                                        blank=True
                                        )
    patient_detail = models.ForeignKey(PatientDetail,
                                       null=True,
                                       blank=True
                                       )

    class Meta:
        verbose_name = "Phone"
        verbose_name_plural = "Phone"
        ordering = ('patient_detail',
                    'phone_type',
                    'ISD_Code',
                    'STD_Code'
                    )

    def __unicode__(self):
        if self.phone:
            return "%s- %s -%s" % (self.ISD_Code, self.STD_Code, self.phone)
        else:
            return "No Phone Number Provided"

    def _field_list(self):
        self.field_list = []
        print self._meta.fields
        for field in self._meta.fields:
            self.field_list.append(field)
        return self.field_list

    def _formatted_obj_data(self):
        if not self.field_list:
            _field_list()
        str_obj = "<ul>"
        for obj in self._field_list:
            _str += "<li>" + obj + "<li>"
            str_obj += _str
        str_obj += "</ul>"
        return str_obj



class EmailAndFax(models.Model):

    """
       Model that manages the Email, Fax and Web contact details of a patient.
    """


    def __init__(self, *args, **kwargs):
      super(EmailAndFax,self).__init__(*args, **kwargs)
      self.__model_label__ = "email_and_fax"
      self._parent_model = 'patient_detail'

    date_entered = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=75, blank=True, null=True)
    fax = models.PositiveIntegerField(
        max_length=20, null=True, blank=True)
    web = models.URLField(max_length=50, null=True, blank=True)
    patient_detail = models.ForeignKey(
        PatientDetail, null=True, blank=True)

    def __unicode__(self):
        return "%s- %s -%s" % (self.email, self.fax, self.web)

    class Meta:
        verbose_name = "Email, Web and Fax"
        verbose_name_plural = "Email, Web and Fax"
        ordering = ('date_entered', 'patient_detail')

    def _field_list(self):
        self.field_list = []
        print self._meta.fields
        for field in self._meta.fields:
            self.field_list.append(field)
        return self.field_list

    def _formatted_obj_data(self):
        if not self.field_list:
            _field_list()
        str_obj = "<ul>"
        for obj in self._field_list:
            _str += "<li>" + obj + "<li>"
            str_obj += _str
        str_obj += "</ul>"
        return str_obj


class Guardian(AuShadhaBaseModel):

    """
      Class that defines the Guardian of a Particular patient.
    """

    def __init__(self, *args, **kwargs):
      super(Guardian,self).__init__(*args, **kwargs)
      self.__model_label__ = "guardian"
      self._parent_model = 'patient_detail'
    
    guardian_name = models.CharField(max_length=20, blank=True,
                                     null=True,
                                     help_text="Enter Guardian Name if Patient is a minor"
                                     )
    relation_to_guardian = models.CharField('Relation',
                                            max_length=20,
                                            blank=True,
                                            null=True,
                                            help_text="Enter relationship to Guardian if Patient is a Minor",
                                            choices=(("Father", "Father"),
                                                     ("Mother", "Mother"),
                                                     ("Local Guardian", "LocalGuardian")
                                                     )
                                            )
    guardian_phone = models.PositiveIntegerField('Phone',
                                                 max_length=20,
                                                 blank=True,
                                                 null=True
                                                 )
    patient_detail = models.ForeignKey(
        PatientDetail, null=True, blank=True)

    class Meta:
        verbose_name = "Guardian Details"
        verbose_name_plural = "Guardian Details"
        ordering = ('patient_detail', 'guardian_name')

    def __unicode__(self):
        if self.guardian_name:
            return "%s " % (self.guardian_name)
        else:
            return "No Guardian Name Provided"

class Demographics(AuShadhaBaseModel):

    """
      Maintains Demographics data for the patient.
      This has been adapted from the excellent work by GNU Health project.
    """

    def __init__(self, *args, **kwargs):
      super(Demographics,self).__init__(*args, **kwargs)
      self.__model_label__ = "demographics"
      self._parent_model = 'patient_detail'

    date_of_birth = models.DateField(auto_now_add=False,
                                     null=True,
                                     blank=True
                                         )
    socioeconomics = models.CharField(max_length=100, default="Middle",
                                      choices=(("low", "Low"),
                                               ("middle", "Middle"),
                                               ("high", "High")
                                                   )
                                      )
    education = models.CharField(max_length=100,
                                 default="Graduate",
                                         choices=(('pg', 'Post-Graduate'),
                                                  ('g', 'Graduate'),
                                                  ('hs', 'High School'),
                                                  ('lg', "Lower Grade School"),
                                                  ('i', "Iliterate")
                                                  )
                                 )
    housing_conditions = models.TextField(max_length=250,
                                          default="Comfortable, with good sanitary conditions"
                                          )
    religion = models.CharField(max_length=200)
    religion_notes = models.CharField(max_length=100,
                                      null=True,
                                      blank=True
                                      )
    race = models.CharField(max_length=200)
    languages_known = models.TextField(max_length=300)
    patient_detail = models.ForeignKey(PatientDetail,
                                       null=True,
                                       blank=True,
                                       unique=True
                                       )

    def __unicode__(self):
        return " Demographics for - %s" % (self.patient_detail)

    def _field_list(self):
        self.field_list = []
        print self._meta.fields
        for field in self._meta.fields:
            self.field_list.append(field)
        return self.field_list

    def formatted_obj_data(self):
        field_list = self._field_list()
        str_obj = "<ul>"
        for obj in field_list:
            _str = "<li>" + obj + "<li>"
            str_obj += _str
        str_obj += "</ul>"
        return str_obj




############################# Model Forms ######################################


class GuardianForm(AuShadhaBaseModelForm):

    """
        ModelForm for Guardian Data Recording
    """

    __form_name__ = "Guardian Form"

    dijit_fields = GUARDIAN_FORM_CONSTANTS

    class Meta:
        model = Guardian
        exclude = DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES


class ContactForm(AuShadhaBaseModelForm):

    """
        ModelForm for Contact Details Recording
    """

    __form_name__ = "Contact Form"

    dijit_fields = CONTACT_FORM_CONSTANTS

    class Meta:
        model = Contact
        exclude = DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES


class PhoneForm(AuShadhaBaseModelForm):

    """
        ModelForm for Phone Recording
    """

    __form_name__ = "Phone Form"

    dijit_fields = PHONE_FORM_CONSTANTS

    class Meta:
        model = Phone
        exclude = DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES


class EmailAndFaxForm(AuShadhaBaseModelForm):

    """
        ModelForm for Email and Fax Data Recording
    """

    __form_name__ = "Email and Fax Form"

    dijit_fields = EMAIL_AND_FAX_FORM_CONSTANTS

    class Meta:
        model = EmailAndFax
        exclude = DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES


class DemographicsForm(AuShadhaBaseModelForm):

    """
        ModelForm for Demographics Data Recording
    """

    __form_name__ = "Demographics Form"

    dijit_fields = DEMOGRAPHICS_FORM_CONSTANTS

    class Meta:
        model = Demographics
        exclude = DEFAULT_DEMOGRAPHICS_FORM_EXCLUDES