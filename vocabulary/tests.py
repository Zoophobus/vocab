from django.test import TestCase
from django.utils import timezone

# Create your tests here.

from models import LanguageA, LanguageB, TranslationGroup, Translation
from forms import LanguageAForm, LanguageBForm, TranslationGroupForm, TranslationsForm
from views import Learn, Test

class modelTests(TestCase):
    def setup(self):
        self.english = LanguageA(value='Ecumenical')
        self.english.save()
        self.dutch = LanguageB(value='Oecumenisch')
        self.dutch.save()
        self.group = TranslationGroup(groupName='Protestants')
        self.group.save()
        self.adjective = Translation(language_a=self.english, language_b=self.dutch, translation_group=self.group)
        self.adjective.save()


    def test_translation_model(self):
        self.assertFalse(adjective.verb())
        non_verb = Translation(language_a=self.english, language_b=self.dutch, translation_group=self.group)
        self.assertRaises(Exception, non_verb.save)

    def test_adjective_model(self):
        valid_input = 'Parish house'
        valid_term = LanguageA(value=valid_input)
        valid_term.save()
        invalid_input = 20*'Parish house'
        invalid_term = LanguageA(value=invalid_input)
        self.assertRaises(DataError, invalid_term.save)


class FormTests(TestCase):
    def setup(self):
        self.lang_a_form_data = {'value':'one'}
        self.lang_b_form_data = {'value':'een'}
        self.group_form_data = {'groupName': 'numeric'}
        self.lang_a_invalid_form_data = {'value': 'two', 'creation_data' : timezone.now()}

    def valid_form(self):
        form = LanguageA(self.lang_a_form_data)
        self.assertTrue(form.is_valid())
        form = LanguageA(self.lang_a_invalid_form_data)
        self.assertFalse(form.is_valid())
