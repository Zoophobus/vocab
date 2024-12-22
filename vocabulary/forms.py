from django import forms
import datetime

from .models import LanguageA, LanguageB, Translation, TranslationGroup
from .models import Verbs, SimplePresent, SimplePast, PresentPerfect, Future, Conditional, Infinitive

class LanguageBForm(forms.ModelForm):
    class Meta:
        model = LanguageB
        fields = ['value']#,'creation_date'] # might be better to avoid
        widgets = {
                'value' : forms.TextInput(attrs={
                    'size' : 50,
                    'title' : 'Word',
                    'placeholder' : 'translation ----',
                    'required' : 'True',
                    }),
#                'creation_date' : forms.DateTimeInput(attrs={
#                    'type' : 'datetime-local',
#                    'class' : 'form-control'},
#                    format='%y-%m-%dT%H:%M'),
                }
        labels = {
                'value' : ('Translation'),
#                'creation_date' : ('Created at'),
                }

class LanguageAForm(forms.ModelForm):
    class Meta:
        model = LanguageA 
        fields = ['value']#,'creation_date'] #might be better to avoid
        widgets = {
                'value' : forms.TextInput(attrs={
                    'size' : 50,
                    'title' : 'Word',
                    'placeholder' : 'learn ----',
                    'required' : 'True',
                    }),
                # inclusion of the creation date form
#                'creation_date' : forms.DateTimeInput(attrs={
#                    'type' : 'datetime-local',
#                    'class' : 'form-control'},
#                    format='%y-%m-%dT%H:%M'),
                }
        labels = {
                'value' : ('Learn'),
#                'creation_date' : ('Created at'),
                }

class TranslationGroupForm(forms.ModelForm):
    class Meta:
        model = TranslationGroup
        fields = ['groupName']
        widgets = {
                'groupName' : forms.TextInput(attrs={
                    'size' : 50,
                    'title' : 'Word',
                    'placeholder' : 'group',
                    'required' : 'True',
                    }),
                }
        labels = {
               'groupName' : ('Enter a category (e.g. lesson 1)'),
               }

class TranslationListForm(forms.Form):
    translation_list = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(),
            queryset=TranslationGroup.objects.all(),
            to_field_name="groupName",
            initial=0,
            required=False,
            )

# TODO fix this form so that only a single checkbox can be
# selected
class TranslationsIndividualForm(forms.Form):
    translations = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(),
            queryset=Translation.objects.all(),
            to_field_name="translation_key",
            initial=0,
            required=False,
            )

class TranslationsForm(forms.Form):
    translations = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(),
            queryset=Translation.objects.all(),
            to_field_name="translation_key",
            initial=0,
            required=False,
            )


class VerbTenseForm(forms.Form):
    tense_options = (
        ('All', 'All'),
        ('Present', 'Present'),
        ('Past', 'Past'),
        ('Future', 'Future'),
    )
    verb_tense_fields = forms.ChoiceField(choices=tense_options,initial='All')
#    def __init__(self,*args,**kwargs):
#        if 'choice' in kwargs:
#            self.option = kwargs.pop('choice')
#            super(VerbTenseForm,self).__init__(*args,**kwargs)
#            self.fields['tense_field'].widget = forms.ChoiceField(choices=VerbTenseForm.tense_options,initial=self.option)
#        else:
#            super(VerbTenseForm,self).__init__(*args,**kwargs)
#            self.fields['tense_field'].widget = forms.ChoiceField(choices=VerbTenseForm.tense_options,initial='All')


#class TranslationsForm(forms.ModelForm):
#    class Meta:
#        model = Translation
#        exclude = ('english','dutch')
#    def __init__(self,grp=None,**kwargs):
#        super(TranslationsForm,self).__init__(**kwargs)
#        if isinstance(grp,TranslationGroup):
#            self.fields['translation_group'].queryset = Translation.objects.filter(translation_group=grp)
#        else:
#            self.fields['translation_group'].queryset = Translation.objects.all()


class DateForm(forms.Form):
    date = forms.DateField(
            label='Starting from ...',
            widget=forms.DateInput(attrs={ 
                'type' : 'date',
                'class' : 'form-control',
                },
                format='%d/%m/%d',
            ),
            required=False
        )

class TextForm(forms.Form):
    check = forms.CharField(
            widget=forms.TextInput(attrs={
                'size' : '50',
                'placeholder' : 'write your response here',
                'required' : 'False',
                'autocomplete' : 'off',
                }),
            required=False
            )

class SearchForm(forms.Form):
    check = forms.CharField(
            widget=forms.TextInput(attrs={
                'size' : '50',
                'placeholder' : 'Search ... for editing',
                'required' : 'False',
                'autocomplete' : 'off',
                }),
            required=False
            )

###
# Extension of the forms.py module for verbs 
###

class VerbForm(forms.ModelForm):
    def verb(title):
        return forms.TextInput(attrs={
        'size' : 50,
        'title': title,
        'placeholder': title,
        'required': 'True',
        })
    class Meta:
        pass


class SimplePresentForm(VerbForm):
    class Meta:
        model = SimplePresent
        fields = ['spr_first_person_singular', 'spr_first_person_plural',
                'spr_second_person_singular', 'spr_second_person_plural',
                'spr_third_person_singular', 'spr_third_person_plural']
        widgets ={ 
                'spr_first_person_singular' : VerbForm.verb('1st Person singular'),
                'spr_first_person_plural' : VerbForm.verb('1st Person plural'),
                'spr_second_person_singular' : VerbForm.verb('2nd Person singular'),
                'spr_second_person_plural' : VerbForm.verb('2nd Person plural'),
                'spr_third_person_singular' : VerbForm.verb('3rd Person singular'),
                'spr_third_person_plural' : VerbForm.verb('3rd Person plural'),
            }
        labels = {
                'spr_first_person_singular' : '1st person singular',
                'spr_first_person_plural' : '1st person plural',
                'spr_second_person_singular' : '2nd person singular',
                'spr_second_person_plural' : '2nd person plural',
                'spr_third_person_singular' : '3rd person singular',
                'spr_third_person_plural' : '3rd person plural',
            }


class SimplePastForm(VerbForm):
    class Meta:
        model = SimplePast
        fields = ['spa_first_person_singular', 'spa_first_person_plural',
                'spa_second_person_singular', 'spa_second_person_plural',
                'spa_third_person_singular', 'spa_third_person_plural']
        widgets ={ 
                'spa_first_person_singular' : VerbForm.verb('1st Person singular'),
                'spa_first_person_plural' : VerbForm.verb('1st Person plural'),
                'spa_second_person_singular' : VerbForm.verb('2nd Person singular'),
                'spa_second_person_plural' : VerbForm.verb('2nd Person plural'),
                'spa_third_person_singular' : VerbForm.verb('3rd Person singular'),
                'spa_third_person_plural' : VerbForm.verb('3rd Person plural'),
            }
        labels = {
                'spa_first_person_singular' : '1st person singular',
                'spa_first_person_plural' : '1st person plural',
                'spa_second_person_singular' : '2nd person singular',
                'spa_second_person_plural' : '2nd person plural',
                'spa_third_person_singular' : '3rd person singular',
                'spa_third_person_plural' : '3rd person plural',
            }



class PresentPerfectForm(VerbForm):
    class Meta:
        model = PresentPerfect
        fields = ['pp_first_person_singular', 'pp_first_person_plural',
                'pp_second_person_singular', 'pp_second_person_plural',
                'pp_third_person_singular', 'pp_third_person_plural']
        widgets ={ 
                'pp_first_person_singular' : VerbForm.verb('1st Person singular'),
                'pp_first_person_plural' : VerbForm.verb('1st Person plural'),
                'pp_second_person_singular' : VerbForm.verb('2nd Person singular'),
                'pp_second_person_plural' : VerbForm.verb('2nd Person plural'),
                'pp_third_person_singular' : VerbForm.verb('3rd Person singular'),
                'pp_third_person_plural' : VerbForm.verb('3rd Person plural')
            }
        labels = {
                'pp_first_person_singular' : '1st person singular',
                'pp_first_person_plural' : '1st person plural',
                'pp_second_person_singular' : '2nd person singular',
                'pp_second_person_plural' : '2nd person plural',
                'pp_third_person_singular' : '3rd person singular',
                'pp_third_person_plural' : '3rd person plural',
            }


class FutureForm(VerbForm):
    class Meta:
        model = Future
        fields = ['f_first_person_singular', 'f_first_person_plural',
                'f_second_person_singular', 'f_second_person_plural',
                'f_third_person_singular', 'f_third_person_plural']
        widgets ={ 
                'f_first_person_singular' : VerbForm.verb('1st Person singular'),
                'f_first_person_plural' : VerbForm.verb('1st Person plural'),
                'f_second_person_singular' : VerbForm.verb('2nd Person singular'),
                'f_second_person_plural' : VerbForm.verb('2nd Person plural'),
                'f_third_person_singular' : VerbForm.verb('3rd Person singular'),
                'f_third_person_plural' : VerbForm.verb('3rd Person plural'),
            }
        labels = {
                'f_first_person_singular' : '1st person singular',
                'f_first_person_plural' : '1st person plural',
                'f_second_person_singular' : '2nd person singular',
                'f_second_person_plural' : '2nd person plural',
                'f_third_person_singular' : '3rd person singular',
                'f_third_person_plural' : '3rd person plural',
            }


class ConditionalForm(VerbForm):
    class Meta:
        model = Conditional 
        fields = ['c_first_person_singular', 'c_first_person_plural',
                'c_second_person_singular', 'c_second_person_plural',
                'c_third_person_singular', 'c_third_person_plural']
        widgets ={ 
                'c_first_person_singular' : VerbForm.verb('1st Person singular'),
                'c_first_person_plural' : VerbForm.verb('1st Person plural'),
                'c_second_person_singular' : VerbForm.verb('2nd Person singular'),
                'c_second_person_plural' : VerbForm.verb('2nd Person plural'),
                'c_third_person_singular' : VerbForm.verb('3rd Person singular'),
                'c_third_person_plural' : VerbForm.verb('3rd Person plural'),
            }
        labels = {
                'c_first_person_singular' : '1st person singular',
                'c_first_person_plural' : '1st person plural',
                'c_second_person_singular' : '2nd person singular',
                'c_second_person_plural' : '2nd person plural',
                'c_third_person_singular' : '3rd person singular',
                'c_third_person_plural' : '3rd person plural',
            }
