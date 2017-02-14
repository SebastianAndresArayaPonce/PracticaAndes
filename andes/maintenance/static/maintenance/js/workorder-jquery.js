$(document).ready(function() {
/*  $(".spare_part_number").change(function() {
    var id = $(this).val();
    $(".spare_part_description").text( id );
    alert( id );
  });*/
  $("#spare_part_add_row").on("click", function () {
    var suffix = $("tr.spare_part_row:last td:first select").attr("name").match(/\d+/);
    var markup1 = '<tr class="spare_part_row"><td class="wo-solid-left"><select class="wo-form-select" name="spare_part_number_';
    var markup2 = '"><option selected value> -- select an option -- </option>';
    var markup3 = '</select></td><td><br></td><td class="wo-solid-right"><input class="wo-form-text" type="text" name="spare_part_quantity_'
    var markup4 = '"></td><td colspan="3" class="blank"><br></td></tr>';
    $("tr.spare_part_row:last").after(markup1 + suffix + markup2 + {% for entry in spare_parts %} + '<option value="' + {{entry.id}} + '">' + {{entry.spare_part_type}} + ' F: ' + {{ entry.factory_number }} + ' / S: ' + {{ entry.sage_number }} + '</option>' + {% endfor %} + markup3 + suffix + markup4);
  });
  $("#spare_part_del_row").on("click", function () {
    var suffix = $("tr.spare_part_row:last td:first select").attr("name").match(/\d+/);
    alert( suffix );
    if (suffix > 1) {
      $("tr.spare_part_row:last").remove();
    }
  });
});
