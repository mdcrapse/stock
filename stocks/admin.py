from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Owns)
admin.site.register(Stock)
admin.site.register(Transaction)
admin.site.register(Team)
