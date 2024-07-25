from django.contrib import admin
from SpamCaller.models.models import Contact,RegisteredProfile,ContactsProfilesMapping

admin.site.register(Contact)
admin.site.register(ContactsProfilesMapping)
admin.site.register(RegisteredProfile)