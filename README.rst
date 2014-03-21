======================
django-admin-genericfk
======================

This simple django app provides a useful admin widget for models using generic
foreign keys. The widget renders a dropdown to select the content type, and then
renders a "raw foreign key" lookup field, similiar to the admin's raw_id_fields.

To use, simply add `admin_genericfk` to your `INSTALLED_APPS`. Then, in your
modeladmin, extend the GenericFKMixin, and specify the generic fields to use in
`generic_raw_id_fields`:

.. code:: python
  
  from django.contrib import admin 
  from admin_genericfk import GenericFKMixin

  @admin.register(models.TaggedItem)
  class TaggedItemAdmin(GenericFKMixin, admin.ModelAdmin):
      generic_raw_id_fields = ['content_object']
