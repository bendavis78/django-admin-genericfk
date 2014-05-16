import urllib

from django import forms
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.admin.views.main import TO_FIELD_VAR
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.utils.translation import ugettext as _


def get_changelist_url(contenttype, admin_site):
    url = 'admin:{0.app_label}_{0.model}_changelist'.format(contenttype)
    params = {
        TO_FIELD_VAR: contenttype.model_class()._meta.pk.name
    }
    url = reverse(url, current_app=admin_site.name)
    url += '?' + urllib.urlencode(params)
    return url


class GenericForeignKeyRawIdInput(forms.TextInput):
    def __init__(self, gfk_field, modeladmin, attrs=None,
                 using=None):
        self.modeladmin = modeladmin
        self.admin_site = self.modeladmin.admin_site
        self.gfk_field = gfk_field
        self.model = gfk_field.model
        self.opts = self.model._meta
        self.db = using
        super(GenericForeignKeyRawIdInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        # use the actual object from here on
        attrs = attrs.copy()
        value = attrs.pop('compressed_value')

        if attrs is None:
            attrs = {}

        extra = []

        current_url = ''
        if value:
            current_ct = ContentType.objects.get_for_model(value)
            current_url = get_changelist_url(current_ct, self.admin_site)

        if 'class' not in attrs:
            attrs['class'] = 'vForeignKeyRawIdAdminField'
        extra.append('<a href="{0}" class="related-lookup" id="lookup_id_{1}"'
                     ' onclick="return showRelatedObjectLookupPopup(this);">'
                     .format(current_url, name))
        extra.append(
            '<img src="{0}" width="16" height="16" alt="{0}" /></a>'
            .format(static('admin/img/selector-search.gif'), _('Lookup'))
        )
        pk = value is not None and value.pk or ''
        output = [super(GenericForeignKeyRawIdInput, self).render(
            name, force_text(pk), attrs)] + extra

        if value:
            output.append(self.label_for_value(value))

        return mark_safe(''.join(output))

    def label_for_value(self, value):
        obj = value._meta.model._default_manager.using(self.db).get(
            **{'pk': value.pk})
        label = escape(Truncator(obj).words(14, truncate='...'))
        return '&nbsp;<strong>{0}</strong>'.format(label)


class GenericForeignKeyRawIdSelect(forms.Select):
    def __init__(self, db_field, modeladmin, attrs=None, choices=()):
        self.db_field = db_field
        self.modeladmin = modeladmin
        self.admin_site = modeladmin.admin_site
        if not choices:
            opts = self.db_field.model._meta
            ct_field = opts.get_field_by_name(db_field.ct_field)[0]
            choices = ct_field.get_choices()

        if attrs is None:
            attrs = {}
        if 'class' not in attrs:
            attrs['class'] = 'vGenericForeignKeyTypeSelect'

        super(GenericForeignKeyRawIdSelect, self).__init__(attrs, choices)

    def render(self, name, value, attrs):
        attrs = attrs.copy()
        attrs.pop('compressed_value')
        return super(GenericForeignKeyRawIdSelect, self).render(
            name, value, attrs)

    def render_option(self, selected_choices, option_value, option_label):
        selected_html = ''
        url = ''
        data_attr = ''
        if option_value:
            contenttype = ContentType.objects.get(pk=option_value)
            url = get_changelist_url(contenttype, self.admin_site)
            data_attr = mark_safe(' data-url="{0}"'.format(url))
        else:
            option_value = ''
            option_label = '-- Select type --'

        if force_text(option_value) in selected_choices:
            selected_html = mark_safe(' selected="selected"')

        return format_html('<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           selected_html,
                           data_attr,
                           force_text(option_label))


class GenericForeignKeyRawIdWidget(forms.MultiWidget):
    def __init__(self, db_field, modeladmin, attrs=None, using=None):
        select = GenericForeignKeyRawIdSelect(
            db_field, modeladmin, attrs, using)
        input = GenericForeignKeyRawIdInput(
            db_field, modeladmin, attrs, using)
        widgets = (select, input)
        super(GenericForeignKeyRawIdWidget, self).__init__(widgets, attrs)

    def render(self, name, value, attrs=None):
        attrs['compressed_value'] = value
        return super(GenericForeignKeyRawIdWidget, self).render(
            name, value, attrs)

    def decompress(self, value):
        if isinstance(value, (tuple, list)):
            return value
        if value:
            ct = ContentType.objects.get_for_model(value)
            return (force_text(ct.pk), force_text(value.pk))
        return (None, None)

    def format_output(self, rendered_widgets):
        output = u'{0}&nbsp;<span class="vRelatedLookup">{1}</span>'
        return mark_safe(output.format(*rendered_widgets))

    class Media:
        css = {
            'all': ['admin_genericfk/css/admin-genericfk.css']
        }
        js = [
            'admin_genericfk/js/admin-genericfk.js'
        ]
