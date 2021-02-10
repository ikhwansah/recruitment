var settings = {
    "async": true,
    "crossDomain": true,
    "url": "/api/V1.0/listall",
    "method": "POST",
    "data": {
          "keyword" : "division",
          "cur_user": sessionStorage.getItem("cur_user"),
          "token": sessionStorage.getItem("token")
    },
    beforeSend: function () {
        $(".spinner").show();
    },
    complete: function () {
        $(".spinner").hide();
    },
}

// var dataform;
function modalEditDivision(i){
    $("#editDivision"+i).modal("show");
}

function modalDeleteDivision(i){
    $("#deleteDivision"+i).modal("show");
}

function createmodalDiv(data){
      var html = '<div class="modal fade" id="editDivision'+data.id+'" tabindex="-1" role="dialog" aria-labelledby="largeModalLabel" aria-hidden="true">';
            html += '<div class="modal-dialog modal-md" role="document">';
                html += '<div class="modal-content">';
                      html += '<div class="modal-header">';
                            html += '<h5 class="modal-title" id="largeModalLabel">Edit Division</h5>';
                            html += '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
                                html += '<span aria-hidden="true">&times;</span>';
                            html += '</button>';
                      html += '</div>';
                      html += '<div class="modal-body">';
                            html += '<div class="card">';
                                html += '<div class="card-body">';
                                    html += '<div class="row" style="display: none;">'; 
                                        html += '<div class="col-12">';
                                            html += '<div class="form-group">';
                                                html += '<label class="control-label mb-1">ID</label>';
                                                html += '<input id="divid'+data.id+'" type="number" class="form-control" value="'+data.id+'">';
                                            html += '</div>';
                                        html += '</div>';
                                    html += '</div>';
                                    html += '<div class="row">';
                                        html += '<div class="col-12">';
                                            html += '<div class="form-group">';
                                                html += '<label class="control-label mb-1">Divison Name</label>';
                                                html += '<input id="divName'+data.id+'" type="text" class="form-control" value="'+data.name+'">';
                                            html += '</div>';
                                        html += '</div>';
                                    html += '</div>';                                    
                                html += '</div>';
                            html += '</div>';
                        html += '</div>';
                        html += '<div>';
                            html +=  '<div class="modal-footer">';
                                html +=  '<div>';
                                    html +=  '<button class="btn btn-info" onclick="insertDiv('+data.id+')">';
                                        html += '<i class="fa fa-check-square"></i>&nbsp;<span id="save">Edit</span>';
                                    html += '</button>';
                                html += '</div>';
                                html += '<button type="button" class="btn btn-secondary" data-dismiss="modal"><i class="fa fa-times"></i>&nbsp;<span id="cancel">Cancel</span></button>';
                            html += '</div>';
                        html += '</div>';
                    html += '</div>';
                html += '</div>';
            html += '</div>';
        html += '</div>';
        html += '<div class="modal fade" id="deleteDivision'+data.id+'" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">';
              html += '<div class="modal-dialog modal-sm" role="document">';
                html += '<div class="modal-content"><div class="modal-header">';
                  html += '<h5 class="modal-title" id="deleteModalLabel">Are you sure you want to delete this item?</h5>';
                    html += '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
                      html += '<span aria-hidden="true">&times;</span>';
                    html += '</button>';
                html += '</div>';
                html += '<div>';
                  html += '<div class="modal-footer">';
                      html += '<div>';
                        html += '<button id="delete" onclick="deleteDiv('+data.id+')" class="btn btn-info">';
                          html += '<i class="fa fa-check-square"></i>&nbsp;<span id="delete">Delete</span>';
                        html += '</button>';
                      html += '</div>';
                      html += '<button type="button" class="btn btn-secondary" data-dismiss="modal">';
                        html += '<i class="fa fa-times"></i>&nbsp;<span id="cancel">No</span>';
                      html += '</button>';
                  html += '</div>';
                html += '</div>';
              html += '</div>';
        html += '</div>';
      return html;
}

function reloaddata(){
      if ( $.fn.DataTable.isDataTable( '#division' ) ) {
          $("#division").dataTable().fnDestroy();
          $('#division').empty();
      }
      $('#division').append('<thead><tr><th align="center">ID</th><th align="center">Division</th><th align="center">Action</th></tr></thead>');
      $.ajax(settings).done(function(response) {
            division = response["division"]["data"];

              $('#division').DataTable({
                  data: division,
                  order: [[ 1, "asc" ]],
                  info: false,
                  columns: [
                    { "data": "id",
                      "visible": false,
                    },
                    { "data": "name" },
                    {
                      data: null, "width": "10%",
                      "render": function ( data,type,full, meta ) {       
                        if(type === 'filter'){                          
                            $("#editDivision"+data.id).empty();
                            $("#editDivision"+data.id).remove();
                            $("#deleteDivision"+data.id).empty();
                            $("#deleteDivision"+data.id).remove();
                            $(".modal-backdrop.fade.show").remove();
                            $('body').append(createmodalDiv(data));      
                        }                      
                        return '<div class="table-data-feature"><button data-toggle="modal" class="item" data-toggle="tooltip" data-placement="top" title="Edit" onclick="modalEditDivision('+data.id+');"><i class="zmdi zmdi-edit"></i></button> <button class="item" data-toggle="tooltip" data-placement="top" title="Delete" onclick="modalDeleteDivision('+data.id+');"><i class="zmdi zmdi-delete"></i></button></div>';   
                      
                                             
                         }
                  }]
              })
      });
}//reloaddata

function insertDiv(i){
    name = $("#divName"+i).val();          
    id = $("#divid"+i).val();
    var form = new FormData();
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    form.append("name", name);
    form.append("id", id);
    $.ajax({
        type : 'POST',
        url : "/api/V1.0/insertdivision",
        async: true,
        crossDomain: true,
        data: form,
        mimeType : "multipart/form-data",
        processData: false,
        contentType: false,
        beforeSend: function () {
            $(".spinner").show();
        },
        complete: function () {
            $(".spinner").hide();
        },
        success : function(response){
            $("#editDivision"+i).modal("hide");
            $("#modalDivision"+i).modal("hide");
            $("#divName").val('');
            reloaddata();
        }
    });
}

function deleteDiv(i){
    id = $("#divid"+i).val();
    var form = new FormData();
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    form.append("id", id);
    $.ajax({
        type : 'POST',
        url : "/api/V1.0/removedivision",
        async: true,
        crossDomain: true,
        data: form,
        mimeType : "multipart/form-data",
        processData: false,
        contentType: false,
        beforeSend: function () {
            $(".spinner").show();
        },
        complete: function () {
            $(".spinner").hide();
        },
        success : function(response){
            $("#deleteDivision"+i).modal("hide");
            reloaddata();
        }
    });
}
