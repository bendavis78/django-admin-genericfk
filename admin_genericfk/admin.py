from admin_genericfk.fields import GenericForeignKeyField
from admin_genericfk.widgets import GenericForeignKeyRawIdWidget


class GenericFKFormMixin(object):
    modeladmin = None

    def __init__(self, *args, **kwargs):
        obj = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        if obj:
            for name in self.modeladmin.generic_raw_id_fields:
                initial[name] = getattr(obj, name)
        kwargs['initial'] = initial
        super(GenericFKFormMixin, self).__init__(*args, **kwargs)


class GenericFKMixin(object):
    generic_raw_id_fields = []

    def generic_modeform_factory(self, form):
        """
        The modeform_factory skips generic fields, so we start with a new form
        that has our generic fields already declared.
        """
        class_name = self.model.__name__ + str('Form')
        bases = (GenericFKFormMixin, form)

        attrs = {
            'modeladmin': self
        }

        for name in self.generic_raw_id_fields:
            db_field = getattr(self.model, name)
            required = not db_field.blank
            attrs[name] = GenericForeignKeyField(db_field, required=required)

        return type(form)(class_name, bases, attrs)

    def get_form(self, request, obj=None, **kwargs):
        form = kwargs.get('form', self.form)
        kwargs['form'] = self.generic_modeform_factory(form)
        form = super(GenericFKMixin, self).get_form(request, obj, **kwargs)
        for name in self.generic_raw_id_fields:
            db_field = getattr(self.model, name)
            form.base_fields[name].widget = GenericForeignKeyRawIdWidget(
                db_field, self)
            form.base_fields[name].help_text = (
                'Select a type, then click the search icon to select the '
                'related object.')
        return form

    def save_model(self, request, obj, form, change):
        for name in self.generic_raw_id_fields:
            value = form.cleaned_data.get(name)
            setattr(obj, name, value)
        super(GenericFKMixin, self).save_model(request, obj, form, change)

    def to_field_allowed(self, request, to_field):
        # This method causes an exception in ModelAdmin since it calls
        # get_related_field() on GenericRel. This extra check is not really
        # necessary unless you're doing something strange.
        return True
