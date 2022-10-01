from django.contrib import admin

# Register your models here.
from .models import Piggy


class PiggyAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Piggy, PiggyAdmin)
