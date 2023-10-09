from django.contrib import admin

from .models import (
        LanguageA, LanguageB, Translation, TranslationGroup,
        Infinitive, SimplePresent, SimplePast, PresentPerfect,
        Future, Conditional, Verbs, 
        )
# Register your models here.

admin.site.register(LanguageA)
admin.site.register(LanguageB)
admin.site.register(Translation)
admin.site.register(TranslationGroup)
admin.site.register(Infinitive)
admin.site.register(SimplePresent)
admin.site.register(SimplePast)
admin.site.register(PresentPerfect)
admin.site.register(Future)
admin.site.register(Conditional)
admin.site.register(Verbs)
