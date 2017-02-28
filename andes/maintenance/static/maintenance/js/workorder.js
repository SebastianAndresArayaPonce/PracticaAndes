$(document).ready(function() {
  $("#wo-hourmeter").on("blur", function () {
    $(".gl-hourmeter").html("Horómetro " + $("#wo-hourmeter").val().toString());
  });
  $("#wo-out-date").on("blur", function () {
    $(".gl-out-date").html("Fecha de salida: " + $("#wo-out-date").val().toString());
    $(".wo-exit-out-date").html($("#wo-out-date").val().toString());
  });
  $("#wo-out-time").on("blur", function () {
    $(".gl-out-time").html("Hora de salida:" + $("#wo-out-time").val().toString());
    $(".wo-exit-out-time").html($("#wo-out-time").val().toString());
  });
  $(".switch_button").on("click", function () {
    if ($("#guideline").is("[hidden]")) {
      $("#workorder").attr("hidden", "hidden");
      $("#guideline").removeAttr("hidden");
    } else {
      $("#guideline").attr("hidden", "hidden");
      $("#workorder").removeAttr("hidden");
    };
  });
  $("#spare_part_add_row").on("click", function () {
    var suffix = $("tr.spare_part_row:last td:first select").attr("name").match(/\d+/);
    $.get('/sparepartlist/' + suffix, {}, function (data) {
      $('tr.spare_part_row:last').after( data );
      $("#spare_part_number_" + suffix).attr("required", "required");
      $("#spare_part_quantity_" + suffix).attr("required", "required");
    });
  });
  $("#spare_part_del_row").on("click", function () {
    var suffix = $("tr.spare_part_row:last td:first select").attr("name").match(/\d+/);
    if ( parseInt(suffix) > 1) {
      $("tr.spare_part_row:last").remove();
      $("#spare_part_number_" + (parseInt(suffix)-1).toString()).removeAttr("required");
      $("#spare_part_quantity_" + (parseInt(suffix)-1).toString()).removeAttr("required");
    };
  });
  $(".wo-form-table").on("change", "tr.spare_part_row td select", function() {
    var id = ($(this).val()).toString();
    var suffix = $(this).attr("name").match(/\d+/);
    var last_suffix = $("tr.spare_part_row:last td:first select").attr("name").match(/\d+/);
    if (id == "") {
      $("#spare_part_description_" + suffix).html( "<br>" );
      if (parseInt(suffix) == parseInt(last_suffix)) {
        $("#spare_part_quantity_" + suffix).removeAttr("required");
      };
    } else {
      $.get('/spareparttype/' + id, {}, function (data) {
        $("#spare_part_description_" + suffix).html( data );
        $("#spare_part_quantity_" + suffix).attr("required", "required");
      });
    };
  });
  $(".wo-form-table").on("blur", "tr.spare_part_row td input", function() {
    var value = ($(this).val()).toString();
    var suffix = $(this).attr("name").match(/\d+/);
    if (value == "") {
      $("#spare_part_number_" + suffix).removeAttr("required");
    } else {
      $("#spare_part_number_" + suffix).attr("required", "required");
    };
  });
  $("#input_add_row").on("click", function () {
    var suffix = $("tr.input_row:last td:first select").attr("name").match(/\d+/);
    $.get('/inputlist/' + suffix, {}, function (data) {
      $('tr.input_row:last').after( data );
      $("#input_description_" + suffix).attr("required", "required");
      $("#input_quantity_" + suffix).attr("required", "required");
    });
  });
  $("#input_del_row").on("click", function () {
    var suffix = $("tr.input_row:last td:first select").attr("name").match(/\d+/);
    if ( parseInt(suffix) > 1) {
      $("tr.input_row:last").remove();
      $("#input_description_" + (parseInt(suffix)-1).toString()).removeAttr("required");
      $("#input_quantity_" + (parseInt(suffix)-1).toString()).removeAttr("required");
    };
  });
  $(".wo-form-table").on("change", "tr.input_row td select", function() {
    var id = ($(this).val()).toString();
    var suffix = $(this).attr("name").match(/\d+/);
    var last_suffix = $("tr.input_row:last td:first select").attr("name").match(/\d+/);
    if (id == "" && parseInt(suffix) == parseInt(last_suffix)) {
      $("#input_quantity_" + suffix).removeAttr("required");
    } else {
      $("#input_quantity_" + suffix).attr("required", "required");
    };
  });
  $(".wo-form-table").on("blur", "tr.input_row td input", function() {
    var value = ($(this).val()).toString();
    var suffix = $(this).attr("name").match(/\d+/);
    if (value == "") {
      $("#input_description_" + suffix).removeAttr("required");
    } else {
      $("#input_description_" + suffix).attr("required", "required");
    };
  });
  $("#workorder-form").submit(function () {
    return confirm("Are you sure? You will not be able to change it later");
  });
});
