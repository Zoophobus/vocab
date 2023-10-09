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
def recentTranslations():
    latest = Translation.objects.order_by('-creation_date')[:5]
    return [t.language_a.value + " - " + t.language_b.value for t in latest]


def index(request):
    return render(request,'learn/index.html',
            {   
#                'english' : eng,
#                'dutch' : dtch,
#                'group' : grp,
                'recent' : recentTranslations(),
                }
        )

def add(request):
    if request.method == 'POST':
        entries = request.POST.getlist('value')
        EntryA = None
        EntryB = None
        category = None
        # first we try and either create or obtain the entries
        try:
            # Create the entries and save them
            EntryA = LanguageA(value=entries[0],creation_date=timezone.now())
            EntryA.save()
        except:
            EntryA = LanguageA.objects.get(value=entries[0])
        try:
            EntryB = LanguageB(value=entries[1],creation_date=timezone.now())
            EntryB.save()
        except:
            EntryB = LanguageB.objects.get(value=entries[1])
        
        # then we try and bind them together, along with creating or obtaining the category
        group = TranslationGroupForm(request.POST)
        try: 
            category = TranslationGroup(groupName=group.data['groupName'],created=timezone.now())
            category.save()
        except IntegrityError:
            category = TranslationGroup.objects.get(groupName=group.data['groupName'])
        try:
            data = Translation(language_a=EntryA,language_b=EntryB,creation_date=timezone.now(),translation_key=EntryA.value + '---' + EntryB.value)
            data.save()
            data.translation_group.add(category)
            status = True
        except IntegrityError:
            status = False

    return HttpResponseRedirect(reverse('index'),{
        'recent' : recentTranslations(),
        'status' : status,
        })

def add_verb(request):
    
    if request.method == 'POST':
        entries = request.POST.getlist('value')
        entryA = None
        entryB = None
        category = None
        # first we try and either create or obtain the entries
        try:
            # Create the entries and save them
            entryA = LanguageA(value=entries[0],creation_date=timezone.now())
            entryA.save()
        except:
            entryA = LanguageA.objects.get(value=entries[0])
        try:
            entryB = LanguageB(value=entries[1],creation_date=timezone.now())
            entryB.save()
        except:
            entryB = LanguageB.objects.get(value=entries[1])
        
        # then we try and bind them together, along with creating or obtaining the category
        group = TranslationGroupForm(request.POST)
        try: 
            category = TranslationGroup(groupName=group.data['groupName'],created=timezone.now())
            category.save()
        except IntegrityError:
            category = TranslationGroup.objects.get(groupName=group.data['groupName'])
        try:
            # TODO might need some further adjustment, in case things go wrong
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
            print(e)

        try:
            data = Translation(language_a=entryA, language_b=entryB, creation_date=timezone.now(), translation_key=entryA.value + '---' + entryB.value, is_a_verb=True, tenses=verb_tenses)
            data.save()
            data.translation_group.add(category)
            status = True
        except IntegrityError:
            status = False

    return HttpResponseRedirect(reverse('index'),{
        'recent' : recentTranslations(),
        'status' : status,
        })


def options(request):
    if request.method == 'GET':
        form_data = request.GET
        if 'learn_vocabulary' in form_data:
            request.GET.get
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
    return render(request,'learn/index.html',
            {
                'recent' : recentTranslations(),
                }
            )

# TODO create a better structure for the Learn and Test View classes.
class Learn(View):
    # this is a weird case where the following static variables
    # do not appear to have the same scope as the class, which
    # is what would normally be expected
    toLearn = list()
    finished = True 
    current_translation = None
    current = None

    @staticmethod
    def positive_response(request, attempt, translation: tuple, alternatives, finished):
        return render(request,'learn/learn_vocabulary.html',
            {
                'category' : translation[0],
                'translation' : translation[1],
                'response' : attempt,
                'good_response' : True,
                'alternatives' : alternatives,
                'completed' : finished,
                })

    def get(self, request):
        if 'return' in request.GET or 'finish' in request.GET:
            self.finished = True
            return HttpResponseRedirect(reverse('index'),{
                'recent' : recentTranslations(),
                })
        elif 'start' in request.GET:
            if self.finished:
                self.toLearn = list()
                if len(request.GET.getlist('translation_list')) > 0:
                    for group in request.GET.getlist('translation_list'):
                        self.toLearn += list(Translation.objects.filter(translation_group__groupName=group))
                elif 'date' in request.GET:
                    upperDate =  datetime.date.today().year.__str__() + "-" + datetime.date.today().month.__str__() +'-'+ str(datetime.date.today().day+1)
                    self.toLearn = list(Translation.objects.filter(creation_date__range=[request.GET['date'],upperDate]))
                else:
                    # add a shortened list with the five most recent entries
                    return HttpResponseRedirect(reverse('index'),{
                        'recent' : recentTranslations(),
                        })
                random.shuffle(self.toLearn)
                self.finished = False
            try:
                if self.current == None or self.current.ready():
                    self.current = self.toLearn.pop()
                self.current_translation = self.current.choose()
            except:
                self.finished = True
            return render(request,'learn/learn_vocabulary.html',
                {   
                    'category' : self.current_translation[0],
                    'translation' : self.current_translation[1],
                    'response' : TextForm(request.GET),
                    'completed' : self.finished
                    })
        elif 'next' in request.GET:
            if self.current == None or self.current.ready():
                self.current = learning.pop()
            self.current_translation = self.current.choose()
            if len(self.toLearn) == 0:
                self.finished = True
            return render(request,'learn/learn_vocabulary.html',
                    {
                        'category' : self.current_translation[0],
                        'translation' : self.current_translation[1],
                        'response' : TextForm(request.GET),
                        'completed' : self.finished,
                        'date_form' : DateForm(request.GET),
                        })
        elif 'check' in request.GET:
            attempt = request.GET.getlist('check')[0]
            relevant = list()
            alternative = list()
            if self.current.language_a.value == self.current_translation[1]:
                # we look up the attempt in language B
                # look up in language (_a, or _b)
                # with self.current.language (_a, or _b)

                relevant = Translation.objects.filter(language_a=self.current.language_a)
                for b_translations in relevant:
                    passed, correct = b_translations.check_translation(attempt, self.current_translation[0], 'b')
                    if passed:
#                    if re.sub(r'^the ','',attempt) == re.sub('^the ','',b_translations.language_b.value):
                        relevant = relevant.exclude(language_b=b_translations.language_b)
                        if len(relevant) > 0:
                            return Learn.positive_response(
                                    request,
                                    attempt,
                                    self.current_translation,
                                    [alt.language_b.value for alt in relevant],
                                    self.finished
                                )
                        else:
                            return Learn.positive_response(
                                    request, attempt, 
                                    self.current_translation, False, self.finished
                                    )
                    elif self.current.is_a_verb:
                        alternative.append(correct)
                if not self.current.is_a_verb:
                    alternative = relevant
            else:
                # we look up the attempt in language A
                relevant = Translation.objects.filter(language_b=self.current.language_b)
                for a_translations in relevant:
                    passed, correct = a_translations.check_translation(attempt, self.current_translation[0], 'a')
                    if passed:
#                    if re.sub(r'^the ','',attempt) == re.sub(r'^the ','',a_translations.language_a.value):
                        relevant = relevant.exclude(language_a=a_translations.language_a)
                        if len(relevant) > 0:
                            return Learn.positive_response(
                                    request,
                                    attempt,
                                    self.current_translation,
                                    [alt.language_a.value for alt in relevant],
                                    self.finished
                                )
                        else:
                            return Learn.positive_response(
                                    request, attempt,
                                    self.current_translation, False, self.finished
                                    )
                    elif self.current.is_a_verb:
                        alternative.append(correct)
                if not self.current.is_a_verb:
                    alternative = relevant
            return render(request,'learn/learn_vocabulary.html',
                {
                    'category' : self.current_translation[0],
                    'translation' : self.current_translation[1],
                    'response' : attempt,
                    'good_response' : False,
                    'alternatives' : alternative,
                    'completed' : self.finished,
                    })

    @classmethod
    def as_view(cls,request):
        return cls.get(cls,request)



class Test(View):
    # this is a weird case where the following static variables
    # do not appear to have the same scope as the class, which
    # is what would normally be expected
    vocabularTestList = list()
    current_translation = None
    current = None
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

    def get(self,request):
        if 'return' in request.GET:
            return HttpResponseRedirect(reverse('index'),{
                'recent' : recentTranslations(),
                })
        elif 'start' in request.GET:
            self.attempts = 0
            self.successes = 0
            self.vocabularTestList = list()
            if len(request.GET.getlist('translation_list')) > 0:
                for group in request.GET.getlist('translation_list'):
                    self.vocabularTestList += list(Translation.objects.filter(translation_group__groupName=group))
            else:
                upperDate =  datetime.date.today().year.__str__() + "-" + datetime.date.today().month.__str__() +'-'+ str(datetime.date.today().day+1)
                self.vocabularTestList = list(Translation.objects.filter(creation_date__range=[request.GET['date'],upperDate]))
            if self.current == None or self.current.ready(3):
                self.current = self.vocabularTestList[random.randrange(0, len(self.vocabularTestList))]
            self.current_translation = self.current.choose()
            return render(request,'learn/test.html',
                {   
                    'category' : self.current_translation[0],
                    'translation' : self.current_translation[1],
                    'response' : TextForm(request.GET),
                    })
        elif 'next' in request.GET:
            if self.current == None or self.current.ready(3):
                self.current = self.vocabularTestList[random.randrange(0, len(self.vocabularTestList))]
            self.current_translation = self.current.choose()
            return render(request,'learn/test.html',
                    {
                        'category' : self.current_translation[0],
                        'translation' : self.current_translation[1],
                        'response' : TextForm(request.GET),
                        'date_form' : DateForm(request.GET),
                        })
        elif 'finish' in request.GET:
            return render(request,'learn/test.html',
                    {
                        'completed' : True,
                        'date_form' : DateForm(request.GET),
                        'by_groups' : TranslationListForm(request.GET),
                        'tried' : self.attempts,
                        'successes' : self.successes,
                        })
        elif 'check' in request.GET:
            attempt = request.GET.getlist('check')[0]
            self.attempts+=1
            relevant = list()
            alternatives = list()
            if self.current.language_a.value == self.current_translation[1]:
                # we look up the attempt in language B
                relevant = Translation.objects.filter(language_a=self.current.language_a)
                for b_translations in relevant:
                    passed, correct = b_translations.check_translation(attempt, self.current_translation[0], 'b')
                    if passed:
#                    if re.sub(r'^the ','',attempt) == re.sub(r'^the ','',b_translations.language_b.value):
                        self.successes+=1
                        relevant = relevant.exclude(language_b=b_translations.language_b)
                        if len(relevant) > 0:
                            return self.positive_response(
                                    request,
                                    attempt,
                                    self.current_translation,
                                    [alt.language_b.value for alt in relevant]
                                    )
                        else:
                            return self.positive_response(
                                    request, attempt,
                                    self.current_translation, False
                                    )
                    elif self.current.is_a_verb:
                        alternatives.append(correct)
                if not self.current.is_a_verb:
                    alternatives = relevant
            else:
                # we look up the attempt in language A
                relevant = Translation.objects.filter(language_b=self.current.language_b)
                for a_translations in relevant:
                    passed, correct = a_translations.check_translation(attempt, self.current_translation[0], 'b')
                    if passed:
#                    if re.sub(r'^the ','',attempt) == re.sub(r'^the ','',a_translations.language_a.value):
                        self.successes+=1
                        relevant = relevant.exclude(language_a=a_translations.language_a)
                        if len(relevant) > 0:
                            return self.positive_response(
                                    request,
                                    attempt,
                                    self.current_translation,
                                    [alt.language_a.value for alt in relevant])
                        else:
                            return self.positive_response(
                                    request, attempt, 
                                    self.current_translation, False
                                    )
                    if self.current.is_a_verb:
                        alternatives.append(correct)
                if not self.current.is_a_verb:
                    alternatives = relevant
            return render(request,'learn/test.html',
                {
                    'category' : self.current_translation[0],
                    'translation' : self.current_translation[1],
                    'response' : attempt,
                    'good_response' : False,
                    'alternatives' : alternatives,
                    })

    @classmethod
    def as_view(cls,request):
        return cls.get(cls,request)

def delete(request):
    if request.method == 'POST':
        trnsList = request.POST.getlist('translations')
        for key in trnsList:
            print(type(key))
            trnsl = Translation.objects.get(translation_key=key)
            trnsl.delete()
    return render(request,'learn/remove.html',
            {
                'by_groups' : TranslationListForm(request.GET),
                'everything' : TranslationsForm(request.GET),
                })

def group(request):
    trnsLst = list()
    if request.method == 'GET':
        grp = request.GET.get('translation_list')[0]
        print(grp)
        return render(request,'learn/remove.html',
            {
                'by_groups' : TranslationListForm(request.GET),
                'everything' : TranslationsForm(request.GET,grp=grp),
                })
