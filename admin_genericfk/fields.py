from django import forms


class GenericForeignKeyField(forms.MultiValueField):
    def __init__(self, db_field, *args, **kwargs):
        self.db_field = db_field
        opts = db_field.model._meta
        ct_field = opts.get_field_by_name(db_field.ct_field)[0]
        fk_field = opts.get_field_by_name(db_field.fk_field)[0]
        fields = (ct_field.formfield(), fk_field.formfield())
        super(GenericForeignKeyField, self).__init__(
            fields=fields, *args, **kwargs)

    def compress(self, data):
        ct, pk = data
        return ct.get_object_for_this_type(pk=pk)
