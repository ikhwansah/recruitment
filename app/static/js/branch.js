var settings = {
  "async": true,
  "crossDomain": true,
  "url": "/api/V1.0/listall",
  "method": "POST",
  "data": {
      "keyword" : "branch",
      "cur_user": sessionStorage.getItem("cur_user"),
      "token": sessionStorage.getItem("token")
  },
  beforeSend: function () {
      $(".spinner").show();
  },
  complete: function () {
      $(".spinner").hide();
  }
}

function modalEdit(i){
    $.ajax({
        type: 'POST',
        url: "/api/V1.0/branchdetail",
        async: true,
        crossDomain: true,
        data: {
            "cur_user": sessionStorage.getItem("cur_user"),
            "token": sessionStorage.getItem("token"),
            "branch_id": i
        },
        success: function(response) {                
            $('body').append(createmodal(response['branch'],response['dataform'])); 
            $("#editClient"+i).modal("show");
            $("#idedit").val(i);
        }
    });
}

function modalDelete(i){
    $("#deleteClient"+i).modal("show");
}

function createmodal(data,dataform){
    var html = '<div class="modal fade" id="editClient'+data.id+'" tabindex="-1" role="dialog" aria-labelledby="largeModalLabel" aria-hidden="true">';
            html += '<div class="modal-dialog modal-lg" role="document">';
                html += '<div class="modal-content">';
                    html +='<div class="modal-header">';
                        html += '<h5 class="modal-title" id="largeModalLabel">Edit Branch</h5>';
                        html += '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
                            html += '<span aria-hidden="true">&times; </span>';
                        html += '</button>';
                    html += '</div>';
                    html += '<div class="modal-body">';
                        html += '<div class="card">';
                            html += '<div class="card-body">';
                                html += '<div class="row">';
                                    html += '<div class="col-12">';
                                        html += '<label for="name" class="control-label mb-1">Name</label>';
                                        var name;
                                        if (data.name) {
                                            name = data.name;
                                        } else {
                                            name = "";
                                        }
                                        html += '<input id="name'+data.id+'" name="name" type="text" class="form-control" value="'+name+'">';
                                    html += '</div>';
                                html += '</div>';
                                html += '<div class="row">';
                                    html += '<div class="col-12">';
                                        html += '<label for="address">Address </label>';
                                        var address;
                                        if (data.address) {
                                            address = data.address;
                                        } else {
                                            address = "";
                                        }
                                        html +=  '<textarea name="textarea-input" id="address'+data.id+'" rows="9" placeholder="Enter Addres..." class="form-control">'+address+'</textarea>';
                                    html +=  '</div>';
                                html +=  '</div>';
                                html +=  '<div class="row">';
                                    html +=  '<div class="col-6">';
                                        html +=  '<div class="form-group">';
                                            html +=  '<label for="province" class="control-label mb-1">Province</label>';
                                            html +=  '<div class="col-12 col-md-9">';
                                                html +=  '<select name="province" id="province'+data.id+'" class="form-control" onchange="fillcity(this)">';
                                                    html += '<option value = "0">Select Province </option>';
                                                    $.each(dataform['province']['data'], function(key, value) {
                                                      selected = '';
                                                      if (value.id == data.province_id.id) {
                                                          selected = 'selected';
                                                      } else {
                                                        selected = '';
                                                      }
                                                      html += '<option value="' + value.id + '" ' + selected + '>' + value.name + '</option>';
                                                    });
                                                html += '</select>';
                                            html +=  '</div>';
                                        html +=  '</div>';
                                    html +=  '</div>';
                                    html +=  '<div class="col-6">';
                                        html +=  '<div class="form-group">';
                                            html +=  '<label for="city" class="control-label mb-1">City</label>';
                                            html +=  '<div class="col-12 col-md-9">';
                                                html +=  '<select name="city" id="city'+data.id+'" class="form-control" onchange="fillkec(this)">';
                                                    html += '<option value = "0">Select City </option>';
                                                    if(dataform['city']){
                                                        $.each(dataform['city']['data'], function(key, value) {
                                                            selected = '';
                                                            if (value.province_id == data.city_id.province_id) {
                                                                if (value.id == data.city_id.id) {
                                                                    selected = 'selected';
                                                                } else {
                                                                    selected = '';
                                                                }
                                                                html += '<option value="' + value.id + '" ' + selected + '>' + value.name + '</option>';
                                                            }
                                                        });
                                                    }
                                                html +=  '</select>';
                                            html +=  '</div>';
                                        html +=  '</div>';
                                    html +=  '</div>';
                                html +=  '</div>';
                                html +=  '<div class="row">';
                                    html +=  '<div class="col-6">';
                                        html +=  '<div class="form-group">';
                                            html +=  '<label for="kec" class="control-label mb-1">Kecamatan</label>';
                                            html +=  '<div class="col-12 col-md-9">';
                                                html +=  '<select name="kec" id="kec'+data.id+'" class="form-control" onchange="fillkel(this)">';
                                                    html += '<option value = "0">Select Kecamatan </option>';
                                                    if(dataform['kecamatan']){
                                                        $.each( dataform['kecamatan']['data'], function( key, value ) {
                                                            selected='';
                                                            if(value.city_id == data.kecamatan_id.city_id){
                                                                if(value.id == data.kecamatan_id.id){
                                                                    selected = 'selected';  
                                                                }  
                                                                html += '<option value="'+value.id+'" '+selected+'>'+value.name+'</option>';   
                                                            }             
                                                        });      
                                                    }        
                                                html +=  '</select>';
                                            html +=  '</div>';
                                        html +=  '</div>';
                                    html +=  '</div>';
                                    html +=  '<div class="col-6">';
                                        html +=  '<div class="form-group">';
                                            html +=  '<label for="kel" class="control-label mb-1">Kelurahan </label>';
                                            html +=  '<div class="col-12 col-md-9">';
                                                html +=  '<select name="kel" id="kel'+data.id+'" class="form-control" onchange="fillpostalcode(this)">';                                                                  
                                                    html += '<option value = "0">Select Kelurahan </option>';                                                                  
                                                    if(dataform['kelurahan']){
                                                        $.each( dataform['kelurahan']['data'], function( key, value ) {
                                                            selected='';
                                                            if(value.kecamatan_id == data.kelurahan_id.kecamatan_id){
                                                                if(value.id == data.kelurahan_id.id){
                                                                    selected = 'selected';  
                                                                }  
                                                                html += '<option value="'+value.id+'" '+selected+'>'+value.name+'</option>';   
                                                            }             
                                                        });       
                                                    }
                                                html +=  '</select>';
                                            html +=  '</div>';
                                        html +=  '</div>';
                                    html +=  '</div>';
                                html +=  '</div>';
                                html +=  '<div class="row">';
                                    html +=  '<div class="col-6">';
                                        html +=  '<div class="form-group">';
                                            html +=  '<label for="postalcode" class="control-label mb-1">Postal Code</label>';
                                            html +=  '<div class="col-12 col-md-9">';
                                                html +=  '<select name="postalcode" id="postalcode'+data.id+'" class="form-control">';
                                                    html += '<option value = "0">Select Postal Code </option>';               
                                                    if(dataform['postal_code']){
                                                        $.each( dataform['postal_code']['data'], function( key, value ) {
                                                            selected='';
                                                            if(value.kecamatan_id == data.postal_code_id.kecamatan_id){
                                                                if(value.id == data.postal_code_id.id){
                                                                    selected = 'selected';  
                                                                }  
                                                                html += '<option value="'+value.id+'" '+selected+'>'+value.name+'</option>';   
                                                            }             
                                                        });      
                                                    } 
                                                html +=  '</select>';
                                            html +=  '</div>';
                                        html +=  '</div>';
                                    html +=  '</div>';
                                    html +=  '<div class="col-6">';
                                        html +=  '<div class="form-group">';
                                            html +=  '<label for="rt" class="control-label mb-1">RT/RW</label>';
                                            html +=  '<div class="form-group">';
                                                html +=  '<div class="row">';
                                                    html +=  '<div class="col-6">';
                                                        html +=  '<input id="rt'+data.id+'" name="rt" type="text" class="form-control" placeholder="RT"  value = "'+data.rt+'">';    
                                                    html +=  '</div>';
                                                    html +=  '<div class="col-6">';
                                                        html +=  '<input id="rw'+data.id+'" name="rw" type="text" class="form-control" placeholder="RW" value ="'+data.rw+'">';   
                                                    html +=  '</div>';
                                                html +=  '</div>';
                                            html +=  '</div>';
                                        html +=  '</div>';
                                    html +=  '</div>';
                                html +=  '</div>';
                                html +=  '<div class="row">';
                                    html +=  '<div class="col-6">';
                                        html +=  '<div class="form-group">';
                                            html +=  '<label for="birthdate" class="control-label mb-1">Phone Number</label>';
                                            var phonenumber;
                                            if (data.phone_number) {
                                                phonenumber = data.phone_number;
                                            } else {
                                                phonenumber = "";
                                            }
                                            html +=  '<input maxlength="14" placeholder="Enter Phone Number" name="phonenumber" id="phonenumber'+data.id+'" class="form-control" value="'+phonenumber+'">';
                                        html +=  '</div>';
                                    html +=  '</div>';
                                    html +=  '<div class="col-6">';
                                        html +=  '<div class="form-group">';
                                            html +=  '<label for="birthdate" class="control-label mb-1">Email</label>';
                                            var name;
                                            if (data.name) {
                                                name = data.name;
                                            } else {
                                                name = "";
                                            }
                                            html +=  '<input type="email" placeholder="Enter Email" name="email" id="email'+data.id+'" class="form-control" value="'+data.email+'">';
                                        html +=  '</div>';
                                    html +=  '</div>';
                                html +=  '</div>';
                            html +=  '</div>';
                        html +=  '</div>';
                    html +=  '</div>';
                    html +=  '<div>';
                        html +=  '<div class="modal-footer">';
                            html +=  '<div>';
                                html +=  '<button onclick="editCl('+data.id+')" id="submit-button" class="btn btn-info">';
                                    html +=  '<i class="fa fa-check-square"></i>&nbsp;<span>Save</span>';
                                html +=  '</button>';
                            html +=  '</div>';
                            html +=  '<button type="button" class="btn btn-secondary" data-dismiss="modal"><i class="fa fa-times"></i>&nbsp;<span>Cancel</span></button>';
                        html +=  '</div>';
                    html +=  '</div>';
                html +=  '</div>';
            html +=  '</div>';
        html +=  '</div>';

      return html;
}

function createmodaldelete(data) {
    var html = '<div class="modal fade" id="deleteClient'+data.id+'" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">';
            html += '<div class="modal-dialog modal-sm" role="document">';
                html += '<div class="modal-content"><div class="modal-header">';
                    html += '<h5 class="modal-title" id="deleteModalLabel">Are you sure you want to delete this item?</h5>';
                    html += '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
                        html += '<span aria-hidden="true">&times;</span>';
                    html += "</button>";
                html += "</div>";
                html += "<div>";
                    html += '<div class="modal-footer">';
                        html += "<div>";
                            html += '<button id="delete" onclick="deleteCl('+data.id+')" class="btn btn-info">';
                                html += '<i class="fa fa-check-square"></i>&nbsp;<span id="delete">Delete</span>';
                            html += "</button>";
                        html += "</div>";
                        html += '<button type="button" class="btn btn-secondary" data-dismiss="modal">';
                            html += '<i class="fa fa-times"></i>&nbsp;<span id="cancel">No</span>';
                        html += "</button>";
                    html += "</div>";
                html += "</div>";
            html += "</div>";
        html += "</div>";

    return html;
}

function reloaddata(){ 
    if ( $.fn.DataTable.isDataTable( '#client' ) ) {
        $("#client").dataTable().fnDestroy();
        $('#client').empty(); 
    }
    $('#client').append("<thead><tr><th>Company Name</th><th>Address</th><th>Phone</th><th>Email</th><th>Action</th></tr></thead>"); 
    $.ajax(settings).done(function(response) {
        success: {
            $("#name").val("");
            $("#address").val("");
            $("#rt").val("");
            $("#rw").val("");
            $("#phonenumber").val("");
            $("#email").val("");

            $("#province").empty();
            $('#province').append($('<option>', {
                value: '0',
                text: 'Select Province'
            }));
            $.each(response['province']['data'], function(i, item) {
                $('#province').append($('<option>', {
                    value: item.id,
                    text: item.name
                }));
            });

            data = response["branch"]["data"];
            $(document).ready(function() {
                $.fn.dataTable.ext.errMode = 'none';
                $('#client').DataTable({
                    data: data,
                    columns: [
                    {
                        "data": "name"
                    }, {
                        "data": "address"
                    }, {
                        "data": "phone_number", className: 'dt-body-right'
                    }, {
                        "data": "email"
                    }, {
                        data: null, className: 'dt-body-center', "width": "10%",
                        "render": function ( data,type,full, meta ) {       
                            if(type === 'filter'){
                                $("#editClient"+data.id).empty();
                                $("#editClient"+data.id).remove();
                                $("#deleteClient"+data.id).empty();
                                $("#deleteClient"+data.id).remove();
                                $("body").append(createmodaldelete(data));   
                            }                      
                            return '<div class="table-data-feature"><button data-toggle="modal" class="item" data-toggle="tooltip" data-placement="top" title="Edit" onclick="modalEdit('+data.id+');"><i class="zmdi zmdi-edit"></i></button> <button class="item" data-toggle="tooltip" data-placement="top" title="Delete" onclick="modalDelete('+data.id+');"><i class="zmdi zmdi-delete"></i></button></div>';   
                        }
                  }]
              })
          })
        }
      });      
}//reloaddata
  
function fillcity(object){         
    var city = "city";
    editid = $("#idedit").val();
    province = $("#"+object.id).val();
    checkcorr = object.id.split("-");
    checkedit = object.id.substr(-1);
    
    if(checkcorr.length == 2)
        city = "corr-"+ city;  
        if(!isNaN(checkedit))
            city += editid;
            $.ajax({
                type: 'POST',
                url: "/api/V1.0/listall",
                async: true,
                crossDomain: true,
                data: {
                    "keyword" : "city",
                    "cur_user": sessionStorage.getItem("cur_user"),
                    "token": sessionStorage.getItem("token"),
                    "province_id": province
                },
                success: function(response) {
                    $("#"+city).empty();
                    $('#'+city).append($('<option>', {
                        value: '0',
                        text: 'Select City'
                    }));
                    $.each(response['data'], function(i, item) {
                        $('#'+city).append($('<option>', {
                            value: item.id, 
                            text: item.name
                        }));
                    });
                }
            });
}
      

function fillkec(object){
    var kec = "kec";
    editid = $("#idedit").val();
    province = $("#"+object.id).val();
    checkcorr = object.id.split("-");
    checkedit = object.id.substr(-1);
    if(checkcorr.length == 2)
        kec = "corr-"+ kec;  
        if(!isNaN(checkedit))
            kec += editid;
            $.ajax({
                type: 'POST',
                url: "/api/V1.0/listall",
                async: true,
                crossDomain: true,
                data: {
                    "keyword" : "kecamatan",
                    "cur_user": sessionStorage.getItem("cur_user"),
                    "token": sessionStorage.getItem("token"),
                    "city_id": province
                },
                success: function(response) {
                    $("#"+kec).empty();
                    $('#'+kec).append($('<option>', {
                        value: '0',
                        text: 'Select Kecamatan'
                    }));
                    $.each(response['data'], function(i, item) {
                        $('#'+kec).append($('<option>', {
                            value: item.id,
                            text: item.name
                        }));
                    });
                }
            });
}

function fillkel(object){
    var kel = "kel";
    editid = $("#idedit").val();
    province = $("#"+object.id).val();
    checkcorr = object.id.split("-");
    checkedit = object.id.substr(-1);
    if(checkcorr.length == 2)
        kel = "corr-"+kel;  
        if(!isNaN(checkedit))
            kel += editid;
            $.ajax({
                type: 'POST',
                url: "/api/V1.0/listall",
                async: true,
                crossDomain: true,
                data: {
                    "keyword" : "kelurahan",
                    "cur_user": sessionStorage.getItem("cur_user"),
                    "token": sessionStorage.getItem("token"),
                    "kecamatan_id": province
                },
                success: function(response) {
                    $("#"+kel).empty();
                    $('#'+kel).append($('<option>', {
                        value: '0',
                        text: 'Select Kelurahan'
                    }));
                    $.each(response['data'], function(i, item) {
                        $('#'+kel).append($('<option>', {
                            value: item.id,
                            text: item.name
                        }));
                    });
                }
            });
}

function fillpostalcode(object) {
    var postal = "postalcode";
    editid = $("#idedit").val();
    province = $("#"+object.id).val();
    checkcorr = object.id.split("-");
    checkedit = object.id.substr(-1);
    if(checkcorr.length == 2)
        postal = "corr-"+postal;  
        if(!isNaN(checkedit))
            postal += editid;
            $.ajax({
                type: 'POST',
                url: "/api/V1.0/listall",
                async: true,
                crossDomain: true,
                data: {
                    "keyword" : "postalcode",
                    "cur_user": sessionStorage.getItem("cur_user"),
                    "token": sessionStorage.getItem("token"),
                    "kecamatan_id": province
                },
                success: function(response) {
                    $("#"+postal).empty();
                    $('#'+postal).append($('<option>', {
                        value: '0',
                        text: 'Select postal Code'
                    }));
                    $.each(response['data'], function(i, item) {
                        $('#'+postal).append($('<option>', {
                            value: item.id,
                            text: item.name
                        }));
                    });
                }
            });
}


function addCl() {
    var form = new FormData();
    valid = false; 
    if($("#name").val() == ''){
        $("#name").focus();
        alert("Name not filled in");
        valid = false;
    }else{
        name = $("#name").val();
        form.append("name", name);
        valid = true;
    }
    if($("#address").val() == ''){
        $("#address").focus();
        alert("Address not filled in");
        valid = false;
    }else{
        address = $("#address").val();
        form.append("address", address);
        valid = true;
    }
    if($("#province").val() == '0'){
        $("#province").focus();
        alert("Province not filled in");
        valid = false;
    }else{
        province = $("#province").val();
        form.append("province", province);
        valid = true;
    }
    if($("#city").val() == '0'){
        $("#city").focus();
        alert("City not filled in");
        valid = false;
    }else{
        city = $("#city").val();
        form.append("city", city);
        valid = true;
    }
    if($("#kec").val() == '0'){
        $("#kec").focus();
        alert("District not filled in");
        valid = false;
    }else{
        kecamatan = $("#kec").val();
        form.append("kecamatan", kecamatan);
        valid = true;
    }
    if($("#kel").val() == '0'){
        $("#kel").focus();
        alert("Village not filled in");
        valid = false;
    }else{
        kelurahan = $("#kel").val();
        form.append("kelurahan", kelurahan);
        valid = true;
    }
    if($("#postalcode").val() == '0'){
        $("#postalcode").focus();
        alert("Postal Code not filled in");
        valid = false;
    }else{
        postalcode = $("#postalcode").val();
        form.append("postalcode", postalcode);
        valid = true;
    }
    if($("#rt").val() == ''){
        $("#rt").focus();
        alert("RT not filled in");
        valid = false;
    }else{
        rt = $("#rt").val();
        form.append("rt", rt);
        valid = true;
    }
    if($("#rw").val() == ''){
        $("#rw").focus();
        alert("Rw not filled in");
        valid = false;
    }else{
        rw = $("#rw").val();
        form.append("rw", rw);
        valid = true;
    }
    if($("#phonenumber").val() == ''){
        $("#phonenumber").focus();
        alert("Phone number not filled in");
        valid = false;
    }else{
        phone = $("#phonenumber").val();
        form.append("phonenumber",phone);
        valid = true;
    }
    if($("#email").val() == ''){
        $("#email").focus();
        alert("Email not filled in");
        valid = false;
    }else{
        email = $("#email").val();
        form.append("email", email);
        valid = true;
    }
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    form.append("branch_id", '');
    if(valid == true){
        $.ajax({
              type: 'POST',
              url: "/api/V1.0/insertbranch",
              async: true,
              crossDomain: true,
              data: form,
              processData: false,
              contentType: false,
              beforeSend: function () {
                $(".spinner").show();
              },
              complete: function () {
                $(".spinner").hide();
              },
              success: function(response) {
                  if(response['status'] == '400'){
                      alert(response['message'])
                  }else{
                    alert("Branch Successfully Added");
                    $("#addClient").modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                  }
              }
      });
    }
}

function editCl(i) {
    var form = new FormData();
    valid = false;
    if($("#name"+i).val() == ''){
        $("#name"+i).focus();
        alert("Name not filled in");
        valid = false;
    }else{
        name = $("#name"+i).val();
        form.append("name", name);
        valid = true;
    }
    if($("#address"+i).val() == ''){
        $("#address"+i).focus();
        alert("Address not filled in");
        valid = false;
    }else{
        address = $("#address"+i).val();
        form.append("address", address);
        valid = true;
    }
    if($("#province"+i).val() == '0'){
        $("#province"+i).focus();
        alert("Province not filled in");
        valid = false;
    }else{
        province = $("#province"+i).val();
        form.append("province", province);
        valid = true;
    }
    if($("#city"+i).val() == '0'){
        $("#city"+i).focus();
        alert("City not filled in");
        valid = false;
    }else{
        city = $("#city"+i).val();
        form.append("city", city);
        valid = true;
    }
    if($("#kec"+i).val() == '0'){
        $("#kec"+i).focus();
        alert("District not filled in");
        valid = false;
    }else{
        kecamatan = $("#kec"+i).val();
        form.append("kecamatan", kecamatan);
        valid = true;
    }
    if($("#kel"+i).val() == '0'){
        $("#kel"+i).focus();
        alert("Village not filled in");
        valid = false;
    }else{
        kelurahan = $("#kel"+i).val();
        form.append("kelurahan", kelurahan);
        valid = true;
    }
    if($("#postalcode"+i).val() == '0'){
        $("#postalcode"+i).focus();
        alert("Postal Code not filled in");
        valid = false;
    }else{
        postalcode = $("#postalcode"+i).val();
        form.append("postalcode", postalcode);
        valid = true;
    }
    if($("#rt"+i).val() == ''){
        $("#rt"+i).focus();
        alert("Rt not filled in");
        valid = false;
    }else{
        rt = $("#rt"+i).val();
        form.append("rt", rt);
        valid = true;
    }
    if($("#rw"+i).val() == ''){
        $("#rw"+i).focus();
        alert("Rw not filled in");
        valid = false;
    }else{
        rw = $("#rw"+i).val();
        form.append("rw", rw);
        valid = true;
    }
    if($("#phonenumber"+i).val() == ''){
        $("#phonenumber"+i).focus();
        alert("Phone Number not filled in");
        valid = false;
    }else{
        phone = $("#phonenumber"+i).val();
        form.append("phonenumber",phone);
        valid = true;
    }
    if($("#email"+i).val() == ''){
        $("#email"+i).focus();
        alert("Email not filled in");
        valid = false;
    }else{
        email = $("#email"+i).val();
        form.append("email", email);
        valid = true;
    }
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    form.append("branch_id", i);
    if(valid == true){
          $.ajax({
              type: 'POST',
              url: "/api/V1.0/insertbranch",
              async: true,
              crossDomain: true,
              data: form,
              processData: false,
              contentType: false,
              beforeSend: function () {
                $(".spinner").show();
              },
              complete: function () {
                $(".spinner").hide();
              },
              success: function(response) {
                  if(response['status'] == '400'){
                      alert(response['message'])
                  }else{
                    $("#editClient"+i).modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                  }
              }
          });
    }
}
      
function deleteCl(i){
    id = i;
    var form = new FormData();
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    form.append("id", id);
    $.ajax({
        type : 'POST',
        url : "/api/V1.0/removebranch",
        async: true,
        crossDomain: true,
        dataType: "json",
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
            if(response['status'] == "400"){
                alert(response['message']);
            }
            else{
                $("#deleteClient"+i).modal("hide");  
                reloaddata();
            }
        }
    });
}