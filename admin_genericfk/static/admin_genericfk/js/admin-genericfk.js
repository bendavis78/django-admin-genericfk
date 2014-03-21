(function($){
  $(document).ready(function(){
    var update = function(select, reset) {
      var $select = $(select);
      var $lookup = $select.siblings('.vRelatedLookup');
      var $link = $lookup.find('a.related-lookup');
      var $input = $lookup.find('input.vForeignKeyRawIdAdminField');
      var $selectedOption = $(select.selectedOptions[0]);
      if (reset) {
        console.log('reset');
        $input.attr('value', '').trigger('change');
      }
      if ($select.val() !== '') {
        $lookup.show();
        $link.attr('href', $selectedOption.attr('data-url'));
      } else {
        $lookup.hide();
        $link.attr('href', '#');
      }
    };
    var $selects = $('select.vGenericForeignKeyTypeSelect');
    $selects.on('change', function(){
      update(this, true);
    });
    $selects.each(function(){update(this, false);});
  });
})(django.jQuery);
