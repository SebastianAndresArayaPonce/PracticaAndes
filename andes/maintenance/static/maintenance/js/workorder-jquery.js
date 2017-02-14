$(document).ready(function() {
/*  $(".spare_part_number").change(function() {
    var id = $(this).val();
    $(".spare_part_description").text( id );
    alert( id );
  });*/
  $("#spare_part_add_row").on( "click", function () {
    var suffix = $("tr.spare_part_row:last td:first select").attr("name").match(/\d+/);
    $.get('/sparepartlist/' + suffix, {}, function (data) {
      $('tr.spare_part_row:last').after( data );
    });
    $("#spare_part_number_" + suffix).attr("required", "required");
  });
  $("#spare_part_del_row").on("click", function () {
    var suffix = $("tr.spare_part_row:last td:first select").attr("name").match(/\d+/);
    if ( suffix > 1 ) {
      $("tr.spare_part_row:last").remove();
      $("#spare_part_number_" + (parseInt(suffix)-1).toString()).removeAttr("required");
    };
  });
});
