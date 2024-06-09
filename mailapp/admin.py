from django.contrib import admin

from mailapp.models import Mail, Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','message', 'created_at','status', 'datetime_send',)
    list_filter = ('title',)


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email',)
    list_filter = ('email',)
