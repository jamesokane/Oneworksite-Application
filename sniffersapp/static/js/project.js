/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');

//$(function () {
//
//  /* Functions */
//
//  var loadForm = function () {
//    var btn = $(this);
//    $.ajax({
//      url: btn.attr("data-url"),
//      type: 'get',
//      dataType: 'json',
//      beforeSend: function () {
//        $("#modal-equipment .modal-content").html("");
//        $("#modal-equipment").modal("show");
//      },
//      success: function (data) {
//        $("#modal-equipment .modal-content").html(data.html_form);
//      }
//    });
//  };
//
//  var saveForm = function () {
//    var form = $(this);
//    $.ajax({
//      url: form.attr("action"),
//      data: form.serialize(),
//      type: form.attr("method"),
//      dataType: 'json',
//      success: function (data) {
//        if (data.form_is_valid) {
//          $("dataTables-equipment tbody").html(data.html_list);
//          $("#modal-equipment").modal("hide");
//        }
//        else {
//          $("#modal-equipment .modal-content").html(data.html_form);
//        }
//      }
//    });
//    return false;
//  };
//
//
//  /* Binding */
//
//  // Create
//  $(".js-create-equipment").click(loadForm);
//  $("#modal-equipment").on("submit", ".js-equipment-create-form", saveForm);
//
//  // Update
//  $("#dataTables-equipment").on("click", ".js-update-equipment", loadForm);
//  $("#modal-equipment").on("submit", ".js-equipment-update-form", saveForm);
//
//  // Delete
//  $("#dataTables-equipment").on("click", ".js-delete-equipment", loadForm);
//  $("#modal-equipment").on("submit", ".js-equipment-delete-form", saveForm);
//
//});