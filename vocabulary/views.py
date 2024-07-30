from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.utils import timezone
from django.views import View

import random
import re
import datetime

from .forms import LanguageBForm, LanguageAForm, DateForm, TextForm, TranslationGroupForm, TranslationListForm, TranslationsForm
from .models import LanguageA, LanguageB, Translation, TranslationGroup

from .forms import SimplePresentForm, SimplePastForm, PresentPerfectForm, FutureForm, ConditionalForm#, VerbsForm # is VerbsForm required here?
from .models import SimplePresent, SimplePast, PresentPerfect, Future, Conditional, Verbs, Infinitive#, Tense # Tense is probably not required
# Create your views here.


# Some utility functions for use globally across the views
def recent_translations():
    latest = Translation.objects.order_by('-creation_date')[:5]
    return [t.language_a.value + " - " + t.language_b.value for t in latest]


def index(request):
    return render(request,'learn/index.html',
            {   
                'recent' : recent_translations(),
                }
        )

def add(request):
    if request.method == 'POST':
        entries = request.POST.getlist('value')
        entryA = None
        entryB = None
        category = None
        # first try to either create or obtain the entries
        try:
            entryA = LanguageA.objects.get(value=entries[0])
        except:
            entryA = LanguageA(value=entries[0],creation_date=timezone.now())
            entryA.save()
        try:
            entryB = LanguageB.objects.get(value=entries[1])
        except:
            entryB = LanguageB(value=entries[1],creation_date=timezone.now())
            entryB.save()
        
        # get the category or create a new category from the provided details
        group = TranslationGroupForm(request.POST)
        try: 
            category = TranslationGroup.objects.get(groupName=group.data['groupName'])
        except:
            category = TranslationGroup(groupName=group.data['groupName'],created=timezone.now())
            category.save()
        try:
            data = Translation(language_a=entryA,language_b=entryB,creation_date=timezone.now(),translation_key=entryA.value + '---' + entryB.value)
            data.save()
            data.translation_group.add(category)
            status = True
        except IntegrityError:
            status = False

    return HttpResponseRedirect(reverse('index'),{
        'recent' : recent_translations(),
        'status' : status,
        })

def add_verb(request):
    
    if request.method == 'POST':
        entries = request.POST.getlist('value')
        entryA = None
        entryB = None
        category = None
        # first try to create, or get the entries
        try:
            entryA = LanguageA(value=entries[0],creation_date=timezone.now())
            entryA.save()
        except:
            entryA = LanguageA.objects.get(value=entries[0])
        try:
            entryB = LanguageB(value=entries[1],creation_date=timezone.now())
            entryB.save()
        except:
            entryB = LanguageB.objects.get(value=entries[1])
        
        # get the category for the translation
        group = TranslationGroupForm(request.POST)
        try: 
            category = TranslationGroup(groupName=group.data['groupName'],created=timezone.now())
            category.save()
        except IntegrityError:
            category = TranslationGroup.objects.get(groupName=group.data['groupName'])
        # create the different conjugate forms
        try:
            spr = SimplePresentForm(request.POST)
            spa = SimplePastForm(request.POST)
            pp = PresentPerfectForm(request.POST)
            f = FutureForm(request.POST)
            c = ConditionalForm(request.POST)
            im = Infinitive(
                    infinitive_form = entries[1]
                    )
            im.save()
            if spr.is_valid():
                sprm = SimplePresent(
                        spr_first_person_singular = spr.data['spr_first_person_singular'],
                        spr_first_person_plural = spr.data['spr_first_person_plural'],
                        spr_second_person_singular = spr.data['spr_second_person_singular'],
                        spr_second_person_plural = spr.data['spr_second_person_plural'],
                        spr_third_person_singular = spr.data['spr_third_person_singular'],
                        spr_third_person_plural = spr.data['spr_third_person_plural']
                        )
                sprm.save()
            if spa.is_valid():
                spam = SimplePast(
                        spa_first_person_singular = spa.data['spa_first_person_singular'],
                        spa_first_person_plural = spa.data['spa_first_person_plural'],
                        spa_second_person_singular = spa.data['spa_second_person_singular'],
                        spa_second_person_plural = spa.data['spa_second_person_plural'],
                        spa_third_person_singular = spa.data['spa_third_person_singular'],
                        spa_third_person_plural = spa.data['spa_third_person_plural']
                        )
                spam.save()
            if pp.is_valid():
                ppm = PresentPerfect(
                        pp_first_person_singular = pp.data['pp_first_person_singular'],
                        pp_first_person_plural = pp.data['pp_first_person_plural'],
                        pp_second_person_singular = pp.data['pp_second_person_singular'],
                        pp_second_person_plural = pp.data['pp_second_person_plural'],
                        pp_third_person_singular = pp.data['pp_third_person_singular'],
                        pp_third_person_plural = pp.data['pp_third_person_plural']
                        )
                ppm.save()
            if f.is_valid():
                fm = Future(
                        f_first_person_singular = f.data['f_first_person_singular'],
                        f_first_person_plural = f.data['f_first_person_plural'],
                        f_second_person_singular = f.data['f_second_person_singular'],
                        f_second_person_plural = f.data['f_second_person_plural'],
                        f_third_person_singular = f.data['f_third_person_singular'],
                        f_third_person_plural = f.data['f_third_person_plural']
                        )
                fm.save()
            if c.is_valid():
                cm = Conditional(
                        c_first_person_singular = c.data['c_first_person_singular'],
                        c_first_person_plural = c.data['c_first_person_plural'],
                        c_second_person_singular = c.data['c_second_person_singular'],
                        c_second_person_plural = c.data['c_second_person_plural'],
                        c_third_person_singular = c.data['c_third_person_singular'],
                        c_third_person_plural = c.data['c_third_person_plural']
                        )
                cm.save()
                verb_tenses = Verbs(infinitive = im, simple_present=sprm, simple_past=spam,
                    present_perfect=ppm, future=fm, conditional=cm)
                verb_tenses.save()
        except Exception as e:
            status = False

        try:
            data = Translation(language_a=entryA, language_b=entryB, creation_date=timezone.now(), translation_key=entryA.value + '---' + entryB.value, is_a_verb=True, tenses=verb_tenses)
            data.save()
            data.translation_group.add(category)
            status = True
        except IntegrityError:
            status = False

    return HttpResponseRedirect(reverse('index'),{
        'recent' : recent_translations(),
        'status' : status,
        })


def options(request):
    if request.method == 'GET':
        form_data = request.GET
        if 'learn_vocabulary' in form_data:
            return render(request,'learn/learn_vocabulary.html', 
                    {
                        'date_form' : DateForm(request.GET),
                        'by_groups' : TranslationListForm(request.GET),
                        }
                    )
        elif 'test_vocabulary' in form_data:
            return render(request,'learn/test.html',
                    {
                        'date_form' : DateForm(request.GET),
                        'by_groups' : TranslationListForm(request.GET),
                        }
                    )
        elif 'remove_translation' in form_data:
            return render(request,'learn/remove.html',
                    {
                        'by_groups' : TranslationListForm(request.GET),
                        'everything' : TranslationsForm(request.GET),
                })
        elif 'add' in form_data:
            return render(request,'learn/add.html',
                    {
                        'language_a' : LanguageAForm(request.GET),
                        'language_b' : LanguageBForm(request.GET),
                        'group' : TranslationGroupForm(request.GET),
                        })
        elif 'add_verb' in form_data:
            return render(request,'learn/add_verb.html',
                    {
                        'SimplePast' : SimplePastForm(request.GET),
                        'SimplePresent' : SimplePresentForm(request.GET),
                        'PresentPerfect' : PresentPerfectForm(request.GET),
                        'Future' : FutureForm(request.GET),
                        'Conditional' : ConditionalForm(request.GET),
                        'language_a' : LanguageAForm(request.GET),
                        'language_b' : LanguageBForm(request.GET),
                        'group' : TranslationGroupForm(request.GET),

                        })
    return index(request) 


class Learn(View):
    vocabulary_to_learn = list()
    finished_vocabulary = True 
    current_translation = None
    current_word = None

    @staticmethod
    def positive_response(request, attempt, translation: tuple, alternatives, finished_vocabulary):
        return render(request,'learn/learn_vocabulary.html',
            {
                'category' : translation[0],
                'translation' : translation[1],
                'response' : attempt,
                'good_response' : True,
                'alternatives' : alternatives,
                'completed' : finished_vocabulary,
                })
            
    @staticmethod
    def check_request(request):
        '''
        Uses static class variables to check if the users response includes the correct answer.
        Parameter: the request object from the relevant form: In this case from the "check" button.
        Returns: The respective page with the template learn_vocabulary.html
        '''
        attempt = request.GET.getlist('check')[0]
        relevant = list()
        alternative = list()
        if Learn.current_translation.language_a.value.__eq__(Learn.current_word[1].value):
            # Required language specification due to the use of Django Model attributes for sorting
            # and filtering response variables, searching language_b for a response in language_a
            relevant = Translation.objects.filter(language_a=Learn.current_translation.language_a)
            for translations in relevant:
                passed, correct = translations.check_translation(attempt, Learn.current_word[0], 'b')
                if passed:
                    relevant = relevant.exclude(language_b=translations.language_b)
                    alternatives = [alt.language_b.value for alt in relevant] if len(relevant) > 0 else False
                    return Learn.positive_response(
                            request,
                            attempt,
                            Learn.current_word,
                            alternatives,
                            Learn.finished_vocabulary
                        )
                elif Learn.current_translation.is_a_verb:
                    alternative.append(correct)
            if not Learn.current_translation.is_a_verb:
                alternative = relevant
        else:
            # The alternative language specification, searching language_a for a response in
            # language_b
            relevant = Translation.objects.filter(language_b=Learn.current_translation.language_b)
            for translations in relevant:
                passed, correct = translations.check_translation(attempt, Learn.current_word[0], 'a')
                if passed:
                    relevant = relevant.exclude(language_a=translations.language_a)
                    alternatives = [alt.language_a.value for alt in relevant] if len(relevant) > 0 else False
                    return Learn.positive_response(
                            request,
                            attempt,
                            Learn.current_word,
                            alternatives,
                            Learn.finished_vocabulary
                        )
                elif Learn.current_translation.is_a_verb:
                    alternative.append(correct)
            if not Learn.current_translation.is_a_verb:
                alternative = relevant
        return render(request,'learn/learn_vocabulary.html',
            {
                'category' : Learn.current_word[0],
                'translation' : Learn.current_word[1],
                'response' : attempt,
                'good_response' : False,
                'alternatives' : alternative,
                'completed' : Learn.finished_vocabulary,
                })

    @staticmethod
    def start(request):
        if Learn.finished_vocabulary:
            if len(request.GET.getlist('translation_list')) > 0:
                Learn.vocabulary_to_learn = list()
                for group in request.GET.getlist('translation_list'):
                    Learn.vocabulary_to_learn += list(Translation.objects.filter(translation_group__groupName=group))
            elif 'date' in request.GET:
                upperDate =  datetime.date.today().year.__str__() + "-" + datetime.date.today().month.__str__() +'-'+ str(datetime.date.today().day+1)
                Learn.vocabulary_to_learn = list(Translation.objects.filter(creation_date__range=[request.GET['date'],upperDate]))
            else:
                return index(request)
            random.shuffle(Learn.vocabulary_to_learn)
            Learn.finished_vocabulary = False
        try:
            Learn.current_translation = Learn.vocabulary_to_learn.pop()
            Learn.current_word = Learn.current_translation.choose()
        except:
            Learn.finished_vocabulary = True
        return render(request,'learn/learn_vocabulary.html',
            {   
                'category' : Learn.current_word[0],
                'translation' : Learn.current_word[1],
                'response' : TextForm(request.GET),
                'completed' : Learn.finished_vocabulary
                })
 
    @staticmethod
    def next(request):
        if len(Learn.vocabulary_to_learn) == 0:
            Learn.finished_vocabulary = True
        if Learn.current_translation == None or Learn.current_translation.ready():
            Learn.current_translation = Learn.vocabulary_to_learn.pop()
        Learn.current_word = Learn.current_translation.choose()
        if len(Learn.vocabulary_to_learn) == 0:
            Learn.finished_vocabulary = True
        return render(request,'learn/learn_vocabulary.html',
                {
                    'category' : Learn.current_word[0],
                    'translation' : Learn.current_word[1],
                    'response' : TextForm(request.GET),
                    'completed' : Learn.finished_vocabulary,
                    'date_form' : DateForm(request.GET),
                    })


    def get(self, request):
        if 'return' in request.GET or 'finish' in request.GET:
            Learn.finished_vocabulary = True
            return index(request)
        elif 'start' in request.GET:
            return Learn.start(request)
        elif 'next' in request.GET:
            return Learn.next(request)
        elif 'check' in request.GET:
            return Learn.check_request(request)

    @classmethod
    def as_view(cls,request):
        return cls.get(cls,request)



class Test(View):
    vocabularTestList = list()
    current_translation = None
    current_word = None
    successes=0
    attempts=0

    @staticmethod
    def positive_response(request, attempt, current, alternatives):
        return render(request,'learn/test.html',
            {
                'category' : current[0],
               'translation' : current[1],
                'response' : attempt,
                'good_response' : True,
                'alternatives' : alternatives,
                }
            )
    
    @staticmethod
    def test_response(request):
        attempt = request.GET.getlist('check')[0]
        Test.attempts+=1
        relevant = list()
        alternatives = list()
        if Test.current_translation.language_a.value.__eq__(Test.current_word[1].value):
            relevant = Translation.objects.filter(language_a=Test.current_translation.language_a)
            for b_translations in relevant:
                passed, correct = b_translations.check_translation(attempt, Test.current_word[0], 'b')
                if passed:
                    Test.successes+=1
                    relevant = relevant.exclude(language_b=b_translations.language_b)
                    alternative_responses = [alt.language_b.value for alt in relevant] if len(relevant) > 0 else False
                    return Test.positive_response(
                            request,
                            attempt,
                            Test.current_word,
                            alternative_responses
                            )
                elif Test.current_translation.is_a_verb:
                    alternatives.append(correct)
            if not Test.current_translation.is_a_verb:
                alternatives = relevant
        else:
            relevant = Translation.objects.filter(language_b=Test.current_translation.language_b)
            for a_translations in relevant:
                passed, correct = a_translations.check_translation(attempt, Test.current_word[0], 'a')
                if passed:
                    Test.successes+=1
                    relevant = relevant.exclude(language_a=a_translations.language_a)
                    alternative_responses = [alt.language_a.value for alt in relevant] if len(relevant) > 0 else False
                    return Test.positive_response(
                            request,
                            attempt,
                            Test.current_word,
                            alternative_responses
                            )
                if Test.current_translation.is_a_verb:
                    alternatives.append(correct)
            if not Test.current_translation.is_a_verb:
                alternatives = relevant
        return render(request,'learn/test.html',
            {
                'category' : Test.current_word[0],
                'translation' : Test.current_word[1],
                'response' : attempt,
                'good_response' : False,
                'alternatives' : alternatives,
                })

    @staticmethod
    def start_test(request):
        Test.attempts = 0
        Test.successes = 0
        Test.vocabularTestList = list()
        if len(request.GET.getlist('translation_list')) > 0:
            for group in request.GET.getlist('translation_list'):
                Test.vocabularTestList += list(Translation.objects.filter(translation_group__groupName=group))
        else:
            upperDate =  datetime.date.today().year.__str__() + "-" + datetime.date.today().month.__str__() +'-'+ str(datetime.date.today().day+1)
            Test.vocabularTestList = list(Translation.objects.filter(creation_date__range=[request.GET['date'],upperDate]))
        if Test.current_translation == None or Test.current_translation.ready(3):
            Test.current_translation = Test.vocabularTestList[random.randrange(0, len(Test.vocabularTestList))]
        Test.current_word = Test.current_translation.choose()
        return render(request,'learn/test.html',
            {   
                'category' : Test.current_word[0],
                'translation' : Test.current_word[1],
                'response' : TextForm(request.GET),
                })

    @staticmethod
    def next(request):
        if Test.current_translation == None or Test.current_translation.ready(3):
            Test.current_translation = Test.vocabularTestList[random.randrange(0, len(Test.vocabularTestList))]
        Test.current_word = Test.current_translation.choose()
        return render(request,'learn/test.html',
                {
                    'category' : Test.current_word[0],
                    'translation' : Test.current_word[1],
                    'response' : TextForm(request.GET),
                    'date_form' : DateForm(request.GET),
                    })

    def get(self,request):
        if 'return' in request.GET:
            return index(request)
        elif 'start' in request.GET:
            return Test.start_test(request)
        elif 'next' in request.GET:
            return Test.next(request)
        elif 'finish' in request.GET:
            return render(request,'learn/test.html',
                    {
                        'completed' : True,
                        'date_form' : DateForm(request.GET),
                        'by_groups' : TranslationListForm(request.GET),
                        'tried' : Test.attempts,
                        'successes' : Test.successes,
                        })
        elif 'check' in request.GET:
            return Test.test_response(request)

    @classmethod
    def as_view(cls,request):
        return cls.get(cls,request)

def delete(request):
    if request.method == 'POST':
        trnsList = request.POST.getlist('translations')
        for key in trnsList:
            translation_terms_to_remove = Translation.objects.get(translation_key=key)
            translation_terms_to_remove.delete()
    return render(request,'learn/remove.html',
            {
                'by_groups' : TranslationListForm(request.GET),
                'everything' : TranslationsForm(request.GET),
                })

def group(request):
    trnsLst = list()
    if request.method == 'GET':
        translation_group = request.GET.get('translation_list')[0]
        return render(request,'learn/remove.html',
            {
                'by_groups' : TranslationListForm(request.GET),
                'everything' : TranslationsForm(request.GET,grp=translation_group),
                })
