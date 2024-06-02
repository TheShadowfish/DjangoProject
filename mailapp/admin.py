from django.contrib import admin

from mailapp.models import Mail


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email',)
    list_filter = ('email',)