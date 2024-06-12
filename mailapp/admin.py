from django.contrib import admin

from mailapp.models import Client, Mailing, MailingLog


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'message', 'created_at', 'status', 'datetime_send',)
    list_filter = ('title',)


@admin.register(Client)
class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email',)
    list_filter = ('email',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('log_text', 'mailing', 'created_at', 'updated_at',)
    list_filter = ('mailing',)
