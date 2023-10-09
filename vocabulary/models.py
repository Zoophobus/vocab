from django.db import models
from django.utils import timezone

import random
import re
# Create your models here.


def translation_default(arg1,arg2):
    return arg1 + " - " + arg2

def group_default(arg=None):
    if arg==None:
        return 'NA'
    return arg


class LanguageA(models.Model):
    value = models.CharField(max_length=100,unique=True)
    creation_date = models.DateTimeField('Date',auto_now=True)
    @classmethod
    def create(cls,name):
        self.value = name
    def __str__(self):
        return self.value 


class LanguageB(models.Model):
    value = models.CharField(max_length=100,unique=True)
    creation_date = models.DateTimeField('Date',auto_now=True)
    @classmethod
    def create(cls,name):
        self.value = name
    def __str__(self):
        return self.value 


class TranslationGroup(models.Model):
    groupName = models.CharField(max_length=50,unique=True)
    created = models.DateField('Date',auto_now_add=True)
    def name(self):
        return re.sub(r'_',' ',self.groupName.capitalize())
    def __str__(self):
        return re.sub(r'_',' ',self.groupName.capitalize())


###
# Extension for verbs and grammar (purely tenses)
###


class Infinitive(models.Model):
    infinitive_form = models.CharField(max_length=100)

    def __str__(self):
        return "the infinitive of"

    def random(self):
        return ("the infinitive of", self.infinitive_form)

    def checkConjugation(self, value):
        return self.infinitive_form


class SimplePresent(models.Model):
    spr_first_person_singular = models.CharField(max_length=100)
    spr_second_person_singular = models.CharField(max_length=100)
    spr_third_person_singular = models.CharField(max_length=100)
    spr_first_person_plural = models.CharField(max_length=100)
    spr_second_person_plural = models.CharField(max_length=100)
    spr_third_person_plural = models.CharField(max_length=100)

    def __str__(self):
        return "the present (simple)"

    def random(self):
        conj = random.randint(0,5)
        if conj == 0:
            return ("the present (simple): first person singular of", self.spr_first_person_singular)
        elif conj == 1:
            return ("the present (simple): second person singular of", self.spr_second_person_singular)
        elif conj == 2:
            return ("the present (simple): third person singular of", self.spr_third_person_singular)
        elif conj == 3:
            return ("the present (simple): first person plural of", self.spr_first_person_plural)
        elif conj == 4:
            return ("the present (simple): second person plural of", self.spr_second_person_plural)
        elif conj == 5:
            return ("the present (simple): third person plural of", self.spr_third_person_singular)

    def checkConjugation(self, value):
        if value.endswith("first person singular of"):
            return self.spr_first_person_singular
        elif value.endswith("second person singular of"):
            return self.spr_second_person_singular
        elif value.endswith("third person singular of"):
            return self.spr_third_person_singular
        elif value.endswith("first person plural of"):
            return self.spr_first_person_plural
        elif value.endswith("second person plural of"):
            return self.spr_second_person_plural
        elif value.endswith("third person plural of"):
            return self.spr_third_person_plural


class SimplePast(models.Model):
    spa_first_person_singular = models.CharField(max_length=100)
    spa_second_person_singular = models.CharField(max_length=100)
    spa_third_person_singular = models.CharField(max_length=100)
    spa_first_person_plural = models.CharField(max_length=100)
    spa_second_person_plural = models.CharField(max_length=100)
    spa_third_person_plural = models.CharField(max_length=100)

    def __str__(self):
        return "the past perfect"

    def random(self):
        conj = random.randint(0,5)
        if conj == 0:
            return ("the past perfect: first person singular of", self.spa_first_person_singular)
        elif conj == 1:
            return ("the past perfect: second person singular of", self.spa_second_person_singular)
        elif conj == 2:
            return ("the past perfect: third person singular of", self.spa_third_person_singular)
        elif conj == 3:
            return ("the past perfect: first person plural of", self.spa_first_person_plural)
        elif conj == 4:
            return ("the past perfect: second person plural of", self.spa_second_person_plural)
        elif conj == 5:
            return ("the past perfect: third person plural of", self.spa_third_person_singular)

    def checkConjugation(self, value):
        if value.endswith("first person singular of"):
            return self.spa_first_person_singular
        elif value.endswith("second person singular of"):
            return self.spa_second_person_singular
        elif value.endswith("third person singular of"):
            return self.spa_third_person_singular
        elif value.endswith("first person plural of"):
            return self.spa_first_person_plural
        elif value.endswith("second person plural of"):
            return self.spa_second_person_plural
        elif value.endswith("third person plural of"):
            return self.spa_third_person_plural


class PresentPerfect(models.Model):
    pp_first_person_singular = models.CharField(max_length=100)
    pp_second_person_singular = models.CharField(max_length=100)
    pp_third_person_singular = models.CharField(max_length=100)
    pp_first_person_plural = models.CharField(max_length=100)
    pp_second_person_plural = models.CharField(max_length=100)
    pp_third_person_plural = models.CharField(max_length=100)

    def __str__(self):
        return "the present perfect"

    def random(self):
        conj = random.randint(0,5)
        if conj == 0:
            return ("the present perfect: first person singular of", self.pp_first_person_singular)
        elif conj == 1:
            return ("the present perfect: second person singular of", self.pp_second_person_singular)
        elif conj == 2:
            return ("the present perfect: third person singular of", self.pp_third_person_singular)
        elif conj == 3:
            return ("the present perfect: first person plural of", self.pp_first_person_plural)
        elif conj == 4:
            return ("the present perfect: second person plural of", self.pp_second_person_plural)
        elif conj == 5:
            return ("the present perfect: third person plural of", self.pp_third_person_singular)

    def checkConjugation(self, value):
        if value.endswith("first person singular of"):
            return self.pp_first_person_singular
        elif value.endswith("second person singular of"):
            return self.pp_second_person_singular
        elif value.endswith("third person singular of"):
            return self.pp_third_person_singular
        elif value.endswith("first person plural of"):
            return self.pp_first_person_plural
        elif value.endswith("second person plural of"):
            return self.pp_second_person_plural
        elif value.endswith("third person plural of"):
            return self.pp_third_person_plural


class Future(models.Model):
    f_first_person_singular = models.CharField(max_length=100)
    f_second_person_singular = models.CharField(max_length=100)
    f_third_person_singular = models.CharField(max_length=100)
    f_first_person_plural = models.CharField(max_length=100)
    f_second_person_plural = models.CharField(max_length=100)
    f_third_person_plural = models.CharField(max_length=100)

    def __str__(self):
        return "the (simple) future"

    def random(self):
        conj = random.randint(0,5)
        if conj == 0:
            return ("the (simple) future, first person singular of", self.f_first_person_singular)
        elif conj == 1:
            return ("the (simple) future, second person singular of", self.f_second_person_singular)
        elif conj == 2:
            return ("the (simple) future, third person singular of", self.f_third_person_singular)
        elif conj == 3:
            return ("the (simple) future, first person plural of", self.f_first_person_plural)
        elif conj == 4:
            return ("the (simple) future, second person plural of", self.f_second_person_plural)
        elif conj == 5:
            return ("the (simple) future, third person plural of", self.f_third_person_singular)

    def checkConjugation(self, value):
        if value.endswith("first person singular of"):
            return self.f_first_person_singular
        elif value.endswith("second person singular of"):
            return self.f_second_person_singular
        elif value.endswith("third person singular of"):
            return self.f_third_person_singular
        elif value.endswith("first person plural of"):
            return self.f_first_person_plural
        elif value.endswith("second person plural of"):
            return self.f_second_person_plural
        elif value.endswith("third person plural of"):
            return self.f_third_person_plural


class Conditional(models.Model):
    c_first_person_singular = models.CharField(max_length=100)
    c_second_person_singular = models.CharField(max_length=100)
    c_third_person_singular = models.CharField(max_length=100)
    c_first_person_plural = models.CharField(max_length=100)
    c_second_person_plural = models.CharField(max_length=100)
    c_third_person_plural = models.CharField(max_length=100)

    def __str__(self):
        return "the conditional"

    def random(self):
        conj = random.randint(0,5)
        if conj == 0:
            return ("the conditional, first person singular of", self.c_first_person_singular)
        elif conj == 1:
            return ("the conditional, second person singular of", self.c_second_person_singular)
        elif conj == 2:
            return ("the conditional, third person singular of", self.c_third_person_singular)
        elif conj == 3:
            return ("the conditional, first person plural of", self.c_first_person_plural)
        elif conj == 4:
            return ("the conditional, second person plural of", self.c_second_person_plural)
        elif conj == 5:
            return ("the conditional, third person plural of", self.c_third_person_singular)

    def checkConjugation(self, value):
        if value.endswith("first person singular of"):
            return self.c_first_person_singular
        elif value.endswith("second person singular of"):
            return self.c_second_person_singular
        elif value.endswith("third person singular of"):
            return self.c_third_person_singular
        elif value.endswith("first person plural of"):
            return self.c_first_person_plural
        elif value.endswith("second person plural of"):
            return self.c_second_person_plural
        elif value.endswith("third person plural of"):
            return self.c_third_person_plural


class Verbs(models.Model):
    infinitive = models.ForeignKey(Infinitive,
        on_delete=models.CASCADE,
        )
    simple_present = models.ForeignKey(SimplePresent,
        on_delete=models.CASCADE,
        )
    simple_past = models.ForeignKey(SimplePast,
        on_delete=models.CASCADE,
        )
    present_perfect = models.ForeignKey(PresentPerfect,
        on_delete=models.CASCADE,
        )
    future = models.ForeignKey(Future,
        on_delete=models.CASCADE,
        )
    conditional = models.ForeignKey(Conditional,
        on_delete=models.CASCADE,
        )

    def choose(self) -> object:
        tense = random.randint(0,5)
        if tense == 0:
            return self.simple_present.random()
        elif tense == 1:
            return self.simple_past.random()
        elif tense == 2:
            return self.present_perfect.random()
        elif tense == 3:
            return self.future.random()
        elif tense == 4:
            return self.conditional.random()
        elif tense == 5:
            return self.infinitive.random()
        return False

    def checkConjugation(self, value):
        if value.startswith(self.simple_present.__str__()):
            return self.simple_present.checkConjugation(value)
        elif value.startswith(self.simple_past.__str__()):
            return self.simple_past.checkConjugation(value)
        elif value.startswith(self.present_perfect.__str__()):
            return self.present_perfect.checkConjugation(value)
        elif value.startswith(self.future.__str__()):
            return self.future.checkConjugation(value)
        elif value.startswith(self.conditional.__str__()):
            return self.conditional.checkConjugation(value)
        elif value.startswith(self.infinitive.__str__()):
            return self.infinitive.checkConjugation(value)


# The main Translation class Model

class Translation(models.Model):
    language_a = models.ForeignKey(LanguageA,
            on_delete=models.RESTRICT,
            )
    language_b = models.ForeignKey(LanguageB,
            on_delete=models.RESTRICT,
            )
    translation_key = models.CharField(max_length=203,unique=True,
            default=translation_default(language_a.__str__(),language_b.__str__()))
    creation_date = models.DateField('Date',auto_now_add=True)
    translation_group = models.ManyToManyField(TranslationGroup,
#            on_delete=models.RESTRICT,
            )
    is_a_verb = models.BooleanField(default=False)
    tenses = models.ForeignKey(Verbs,
            on_delete=models.CASCADE,
            null=True
            )

    def __str__(self):
        return self.language_a.__str__() + " --- " + self.language_b.__str__() + "\n"

    def choose(self) -> str:
        if not self.is_a_verb:
            return ("adj/adv/noun", self.language_a.value) if random.randint(0,1) > 0 else ("adj/adv/noun", self.language_b.value)
        else:
            conjugations = Verbs.objects.get(pk=self.tenses.pk)
            return (conjugations.choose()[0], self.language_a.value)
        
    def ready(self, repeats: int = 6) -> bool:
        if not self.is_a_verb:
            return True
        elif not hasattr(Translation.ready, 'is_ready') or Translation.ready.is_ready < 0:
            Translation.ready.is_ready = repeats
        give = False
        if Translation.ready.is_ready == 0:
            give = True
        Translation.ready.is_ready -= 1
        return give

    def verb(self, set_: bool = None) -> bool:
        if set_ is not None:
             self.is_a_verb = set_
        return self.is_a_verb

    def check_translation(self, response: str, form: str, language: str):
        attempt = r"" + re.escape(response)
        correct = ''
        if not self.is_a_verb and form == "adj/adv/noun":
            if language.endswith('b'):
                correct = self.language_b.value
                if re.search(attempt, self.language_b.value):
                    return True, correct
            else:
                correct = self.language_a.value
                if re.search(attempt, self.language_a):
                    return True, correct
        elif form != "adj/adv/noun":
            correct = self.tenses.checkConjugation(form)
            if re.search(attempt, correct):
                return True, correct
        return False, correct


