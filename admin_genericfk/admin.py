from admin_genericfk.fields import GenericForeignKeyField
from admin_genericfk.widgets import GenericForeignKeyRawIdWidget


class GenericFKMixin(object):
    def generic_modeform_factory(self, form):
        """
        The modeform_factory skips generic fields, so we start with a new form
        that has our generic fields already declared.
        """
        class_name = self.model.__name__ + str('Form')

        attrs = {}
        for name in self.generic_raw_id_fields:
            db_field = getattr(self.model, name)
            attrs[name] = GenericForeignKeyField(db_field)

        return type(form)(class_name, (form,), attrs)

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
