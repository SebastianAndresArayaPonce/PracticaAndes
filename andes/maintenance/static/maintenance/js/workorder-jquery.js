$(document).ready(function() {
  $(".spare_part_number").change(function() {
    var id = $(this).val();
    $(".spare_part_description").text( id );
    alert( id );
  });
});
