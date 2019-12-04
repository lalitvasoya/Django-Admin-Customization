from django.contrib import admin
from user_profile.models import Profile, Department
from django.urls import path, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from .form import AddDetailForm
from .models import Department
from django.utils.html import format_html
from django.core import serializers
from django.contrib.contenttypes.models import ContentType


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # list_display = ('enrollment', 'name', 'department')
    list_display = ('enrollment', 'name', 'department',
                    'account_actions', 'present')
    search_fields = ['name', 'enrollment', 'department__name']
    list_filter = ['department__name', 'present']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'addnew/',
                self.admin_site.admin_view(self.process_action),
                name='account-deposit',
            ),
            path(
                'noaction/',
                self.admin_site.admin_view(self.no_action),
                name='account-noaction',
            ),
        ]
        return custom_urls + urls
    # Button in every row

    def account_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">No Action</a>&nbsp;',
            reverse('admin:account-noaction')
        )
    account_actions.short_description = 'Account Actions'
    account_actions.allow_tags = True

    def no_action(self, request):
        url = reverse(
            'admin:user_profile_profile_changelist',
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

    # Button in next to add profile

    def process_action(self, request, *args, **kwargs):
        # account = self.get_object(request, account_id)
        action_form = AddDetailForm
        if request.method != 'POST':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                try:
                    department = Department.objects.get(name=request.POST.get('department'))
                    if not department:
                        department = Department.objects.create(name=request.POST.get('department'))
                    instance = form.save(commit=False)
                    instance.department = department
                    instance.save()
                except Exception as e:
                    print(e)
                    # If save() raised, the form will a have a non
                    # field error containing an informative message.
                    pass
                else:
                    self.message_user(request, 'Success')
                    url = reverse(
                        'admin:user_profile_profile_changelist',
                        current_app=self.admin_site.name,
                    )
                    return HttpResponseRedirect(url)
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        # context['account'] = account
        return TemplateResponse(
            request,
            'admin/account/account_action.html',
            context,
        )
    actions = ['make_present', 'make_absent' ]

    def make_present(self, request, queryset):
        rows_updated = queryset.update(present=True)
        if rows_updated == 1:
            message_bit = "1"
        else:
            message_bit = "%s" % rows_updated
        self.message_user(
            request, "%s successfully make present." % message_bit)

    def make_absent(self, request, queryset):
        rows_updated = queryset.update(present=False)
        if rows_updated == 1:
            message_bit = "1 "
        else:
            message_bit = "%s" % rows_updated
        self.message_user(
            request, "%s successfully make absent." % message_bit)

admin.site.register(Department)
admin.site.site_header = "Wel-Come to New World"
