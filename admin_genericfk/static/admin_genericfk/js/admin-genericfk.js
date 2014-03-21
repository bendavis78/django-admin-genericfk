(function($){
  $(document).ready(function(){
    var changeType = function() {
      console.log('changed');
      var $select = $(this);
      var $lookup = $select.siblings('.vRelatedLookup');
      var $link = $lookup.find('a.related-lookup');
      var $selectedOption = $(this.selectedOptions[0]);
      if ($select.val() !== '') {
        $lookup.show();
        $link.attr('href', $selectedOption.attr('data-url'));
      } else {
        $lookup.hide();
        $link.attr('href', '#');
      }
    };
    var $selects = $('select.vGenericForeignKeyTypeSelect');
    $selects.on('change', changeType).trigger('change');
  });
})(django.jQuery);
