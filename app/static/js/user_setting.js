function reloaddata(){
	$('.btn.head-btn1').remove();
    $('.btn.head-btn2').remove();
    $('#navigation.account').remove();
    $("#reg-name").val("");
    $("#reg-phonenumber").val("");
    $("#reg-email").val("");
    $("#reg-gender").val("0");
    $("#reg-religion").val("0");
    $("#reg-password").val("");
    $("#email").val("");
    $("#password").val("");

    $.ajax({
    	type: 'POST',
        url: "/api/V1.0/checkuser",
        async: true,
        crossDomain: true,
        data: {
        	"cur_user" : sessionStorage.getItem("cur_user"),
            "token": sessionStorage.getItem("token")
        },
        success: function(response) {
        	if(response['status'] == '200'){
            	$('.header-btn.d-none.f-right.d-lg-block').append('<ul id="navigation" class="account"><li><a href="#">Hello, '+ sessionStorage.name +'</a><ul class="submenu"><li><a onclick="modalSetting('+ sessionStorage.cur_user +');" style="cursor: pointer;"><i class="fa fa-info-circle"></i>  Account Setting</a></li><li><a onclick="logout_user();" style="cursor: pointer;"><i class="fa fa-unlock-alt"></i>  Logout</a></li></ul></li></ul>');
            }else{
            	$('.header-btn.d-none.f-right.d-lg-block').append('<a onclick="modalRegister();" class="btn head-btn1" style="color: #fff; cursor: pointer;">Register</a><a onclick="modalLogin();" class="btn head-btn2" style="cursor: pointer;">Login</a>');
            }
        }
    });
    $("body").append(createmodallogin());
    $("body").append(createmodalregister());
}

function modalSetting(i) {
    if ($("#user_setting" + i).length) {
        $("#user_setting" + i).modal("show");
        $("#idsetting").val(i);
    } else {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/userdetail",
            async: true,
            crossDomain: true,
            data: {
                cur_user: sessionStorage.getItem("cur_user"),
                token: sessionStorage.getItem("token"),
                user_id: i,
            },
            success: function (response) {
                $("body").append(createmodalsetting(response["employee"], response["dataform"]));
                fillattachment(response["employee"]);
                $("#user_setting" + i).modal("show");
                $("#idsetting").val(i);
            },
        });
    }
}

function createmodalsetting(data, dataform) {
    var html = '<div class="modal fade" id="user_setting'+ data.id +'" tabindex="-1" role="dialog" aria-labelledby="largeModalLabel" aria-hidden="true">';
    html += '<div class="modal-dialog modal-lg" role="document">';
    html += '<div class="modal-content">';
    html += '<div class="modal-header">';
    html += '<h5 class="modal-title">Account Details</h5>';
    html += '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
    html += "</div>";
    html += '<div class="modal-body">';
    html += '<div class="card">';
    html += '<div class="card-body">';
    html += '<div class="default-tab">';
    html += "<nav>";
    html += '<div class="nav nav-tabs" id="nav-tab" role="tablist">';
    html += '<a class="nav-item nav-link active" id="nav-bio-tab" data-toggle="tab" href="#nav-bio'+ data.id +'" role="tab" aria-controls="nav-bio" aria-selected="true">Biodata</a>';
    html += '<a class="nav-item nav-link" data-toggle="tab" id="nav-correspondance-tab" href="#nav-correspondance'+ data.id +'" role="tab" aria-controls="nav-correspondance" aria-selected="false">Domisili</a>';
    html += '<a class="nav-item nav-link" data-toggle="tab" id="nav-edu-tab" href="#nav-edu'+ data.id +'" role="tab" aria-controls="nav-edu" aria-selected="false">Education</a>';
    html += '<a class="nav-item nav-link" id="nav-work-tab" data-toggle="tab" href="#nav-work'+ data.id +'" role="tab" aria-controls="nav-work" aria-selected="false">Work Experience</a>';
    html += '<a class="nav-item nav-link" id="nav-file-tab" data-toggle="tab" href="#nav-file'+ data.id +'" role="tab" aria-controls="nav-file" aria-selected="false">Attachment Files</a>';
    html += "</div>";
    html += "</nav>";
    html += '<div class="tab-content pl-3 pt-2" id="nav-tabContent" style="margin-bottom: -2.5em">';
    html += '<div class="tab-pane fade show active" id="nav-bio'+ data.id +'" role="tabpanel" aria-labelledby="nav-bio-tab">';
    html += '<div class="card-body card-block">';
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Name</label>';
    var name;
    if (data.name) {
        name = data.name;
    } else {
        name = "";
    }
    html += '<input id="name' + data.id + '" type="text" class="form-control" value="' + name + '">';
    html += "</div>";
    html += "</div>";
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">NIK(KTP)</label>';
    var nik;
    if (data.nik) {
        nik = data.nik;
    } else {
        nik = "";
    }
    html += '<input id="nik' + data.id + '" type="text" class="form-control" value="' + nik + '">';
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Phone Number</label>';
    var phone;
    if (data.phone_number) {
        phone = data.phone_number;
    } else {
        phone = "";
    }
    html += '<input id="phonenumber' + data.id + '" class="form-control" value="' + phone + '">';
    html += "</div>";
    html += "</div>";
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Email</label>';
    var email;
    if (data.email) {
        email = data.email;
    } else {
        email = "";
    }
    html += '<input type="email" id="email' + data.id + '" class="form-control" value="' + email + '">';
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Gender</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="gender" id="gender' + data.id + '" class="form-control">';
    if ("Female" == data.gender) {
        html += '<option value="1">Male</option>';
        html += '<option value="2" selected>Female</option>';
    } else {
        html += '<option value="1" selected>Male</option>';
        html += '<option value="2">Female</option>';
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Religion</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select id="religion' + data.id + '" class="form-control">';
    if ("1" == data.religion) {
        html += '<option value="1" selected>Islam</option>';
        html += '<option value="2">Christian</option>';
        html += '<option value="3">Catholic</option>';
        html += '<option value="4">Hindu</option>';
        html += '<option value="5">Buddha</option>';
    } else if ("2" == data.religion) {
        html += '<option value="1">Islam</option>';
        html += '<option value="2" selected>Christian</option>';
        html += '<option value="3">Catholic</option>';
        html += '<option value="4">Hindu</option>';
        html += '<option value="5">Buddha</option>';
    } else if ("3" == data.religion) {
        html += '<option value="1">Islam</option>';
        html += '<option value="2">Christian</option>';
        html += '<option value="3" selected>Catholic</option>';
        html += '<option value="4">Hindu</option>';
        html += '<option value="5">Buddha</option>';
    } else if ("4" == data.religion) {
        html += '<option value="1">Islam</option>';
        html += '<option value="2">Christian</option>';
        html += '<option value="3">Catholic</option>';
        html += '<option value="4" selected>Hindu</option>';
        html += '<option value="5">Buddha</option>';
    } else if ("5" == data.religion) {
        html += '<option value="1">Islam</option>';
        html += '<option value="2">Christian</option>';
        html += '<option value="3">Catholic</option>';
        html += '<option value="4">Hindu</option>';
        html += '<option value="5" selected>Buddha</option>';
    } else {
        html += '<option value="0" selected>Select Religion</option>';
        html += '<option value="1">Islam</option>';
        html += '<option value="2">Christian</option>';
        html += '<option value="3">Catholic</option>';
        html += '<option value="4">Hindu</option>';
        html += '<option value="5">Buddha</option>';
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-12">';
    html += "<label>Address</label>";
    var address;
    if (data.address) {
        address = data.address;
    } else {
        address = "";
    }
    html += '<textarea name="textarea-input" id="address' + data.id + '" rows="9" class="form-control">' + data.address + "</textarea>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Province</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="province" id="province' + data.id + '" class="form-control" onchange="fillcity(this)">';
    html += '<option value = "0">Select Province</option>';
    $.each(dataform["province"]["data"], function (key, value) {
        selected = "";
        if (value.id == data.province_id.id) {
            selected = "selected";
        } else {
            selected = "";
        }
        html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
    });
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">City</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="city" id="city' + data.id + '" class="form-control" onchange="fillkec(this)">';
    html += '<option value = "0">Select City</option>';
    if (dataform["city"]) {
        $.each(dataform["city"]["data"], function (key, value) {
            selected = "";
            if (value.province_id == data.city_id.province_id) {
                if (value.id == data.city_id.id) {
                    selected = "selected";
                } else {
                    selected = "";
                }
                html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
            }
        });
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Kecamatan</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="kec" id="kec' + data.id + '" class="form-control" onchange="fillkel(this)">';
    html += '<option value = "0">Select Kecamatan</option>';
    if (dataform["kecamatan"]) {
        $.each(dataform["kecamatan"]["data"], function (key, value) {
            selected = "";
            if (value.city_id == data.kecamatan_id.city_id) {
                if (value.id == data.kecamatan_id.id) {
                    selected = "selected";
                } else {
                    selected = "";
                }
                html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
            }
        });
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Kelurahan</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="kel" id="kel' + data.id + '" class="form-control" onchange="fillpostalcode(this)">';
    html += '<option value = "0">Select Kelurahan</option>';
    if (dataform["kelurahan"]) {
        $.each(dataform["kelurahan"]["data"], function (key, value) {
            selected = "";
            if (value.kecamatan_id == data.kelurahan_id.kecamatan_id) {
                if (value.id == data.kelurahan_id.id) {
                    selected = "selected";
                } else {
                    selected = "";
                }
                html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
            }
        });
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Postalcode</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="postalcode" id="postalcode' + data.id + '" class="form-control" >';
    html += '<option value = "0">Select Postalcode</option>';
    if (dataform["postal_code"]) {
        $.each(dataform["postal_code"]["data"], function (key, value) {
            selected = "";
            if (value.kecamatan_id == data.postal_code_id.kecamatan_id) {
                if (value.id == data.postal_code_id.id) {
                    selected = "selected";
                } else {
                    selected = "";
                }
                html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
            }
        });
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">RT/RW</label>';
    html += '<div class="form-group">';
    html += '<div class="row">';
    html += '<div class="col-6">';
    var rt;
    if (data.rt) {
        rt = data.rt;
    } else {
        rt = "";
    }
    html += '<input id="rt' + data.id + '" type="text" class="form-control" value="' + rt + '">';
    html += "</div>";
    html += '<div class="col-6">';
    var rw;
    if (data.rw) {
        rw = data.rw;
    } else {
        rw = "";
    }
    html += '<input id="rw' + data.id + '" type="text" class="form-control" value = "' + rw + '">';
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Birthdate</label>';
    var birthdate;
    if (data.birthdate) {
        birthdate = data.birthdate;
    } else {
        birthdate = "";
    }
    html += '<input type="date" id="birthdate' + data.id + '" class="form-control" value="' + birthdate + '">';
    html += "</div>";
    html += "</div>";
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Birthplace</label>';
    var birthplace;
    if (data.birthplace) {
        birthplace = data.birthplace;
    } else {
        birthplace = "";
    }
    html += '<input type="text" id="birthplace' + data.id + '" class="form-control" value="' + birthplace + '">';
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += "<label>Marital Status</label>";
    html += '<div class="col-12 col-md-9">';
    html += '<select name="marital" id="marital' + data.id + '" class="form-control">';
    if ("1" == data.marital) {
        html += '<option value="1" selected>Single</option>';
        html += '<option value="2">Married</option>';
        html += '<option value="3">Widow/ Widower</option>';
        html += '<option value="4">Divorce</option>';
    } else if ("2" == data.marital) {
        html += '<option value="1">Single</option>';
        html += '<option value="2" selected>Married</option>';
        html += '<option value="3">Widow/ Widower</option>';
        html += '<option value="4">Divorce</option>';
    } else if ("3" == data.marital) {
        html += '<option value="1">Single</option>';
        html += '<option value="2">Married</option>';
        html += '<option value="3" selected>Widow/ Widower</option>';
        html += '<option value="4">Divorce</option>';
    } else if ("4" == data.marital) {
        html += '<option value="1">Single</option>';
        html += '<option value="2">Married</option>';
        html += '<option value="3">Widow/ Widower</option>';
        html += '<option value="4" selected>Divorce</option>';
    } else {
        html += '<option value="0" selected>Select Status</option>';
        html += '<option value="1">Single</option>';
        html += '<option value="2">Married</option>';
        html += '<option value="3">Widow/ Widower</option>';
        html += '<option value="4">Divorce</option>';
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="modal-footer">';
    html += '<div class="items-link items-link2"><a onclick="editEmp(' + data.id + ')" style="cursor: pointer;"><i class="fa fa-check-square"></i> Save</a></div>';
    html += '<div class="items-link items-link2"><a data-dismiss="modal" style="cursor: pointer;"><i class="fa fa-times"></i> Cancel</a></div>';
    html += "</div>";
    html += "</div>";
    html += '<div class="tab-pane fade" id="nav-correspondance' + data.id + '" role="tabpanel" aria-labelledby="nav-correspondance-tab">';
    html += '<div class="card-body card-block">';
    html += '<div class="row">';
    html += '<div class="col-12">';
    html += '<label for="co-address">Correspondance Address</label>';
    if (data["cor-address"].address) {
        coraddress = data["cor-address"].address;
    } else {
        coraddress = "";
    }
    html += '<textarea name="textarea-input" id="corr-address' + data.id + '" rows="9" class="form-control">' + coraddress + "</textarea>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-12">';
    html += '<label for="statusadd" class="control-label mb-1">Status Address</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="statusaddress" id="statusaddress' + data.id + '" class="form-control">';
    html += '<option value = "0">Select Status Address</option>';
    $.each(dataform["status_address"]["data"], function (key, value) {
        selected = "";
        if (data["cor-address"].status_address_id) {
            if (value.id == data["cor-address"].status_address_id.id) {
                selected = "selected";
            } else {
                selected = "";
            }
        }
        html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
    });
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label for="corr-province" class="control-label mb-1">Province</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="corr-province" id="corr-province' + data.id + '" class="form-control" onchange="fillcity(this)">';
    html += '<option value="0">Select Province</option>';
    if (dataform["province"]) {
        $.each(dataform["province"]["data"], function (key, value) {
            selected = "";
            if (data["cor-address"].province_id) {
                if (value.id == data["cor-address"].province_id.id) {
                    selected = "selected";
                } else {
                    selected = "";
                }
            }
            html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
        });
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label for="corr-city" class="control-label mb-1">City</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="corr-city" id="corr-city' + data.id + '" class="form-control" onchange="fillkec(this)">';
    html += '<option value="0">Select City</option>';
    if (dataform["cor-city"]) {
        $.each(dataform["cor-city"]["data"], function (key, value) {
            selected = "";
            if (data["cor-address"].city_id && data["cor-address"].city_id.province_id == value.province_id) {
                if (value.id == data["cor-address"].city_id.id) {
                    selected = "selected";
                } else {
                    selected = "";
                }
                html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
            }
        });
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label for="corr-kec" class="control-label mb-1">Kecamatan</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="corr-kec" id="corr-kec' + data.id + '" class="form-control" onchange="fillkel(this)">';
    html += '<option value = "0">Select Kecamatan</option>';
    if (dataform["cor-kecamatan"]) {
        $.each(dataform["cor-kecamatan"]["data"], function (key, value) {
            selected = "";
            if (data["cor-address"].kecamatan_id && data["cor-address"].kecamatan_id.city_id == value.city_id) {
                if (value.id == data["cor-address"].kecamatan_id.id) {
                    selected = "selected";
                } else {
                    selected = "";
                }
                html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
            }
        });
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label for="corr-kel" class="control-label mb-1">Kelurahan</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="corr-kel" id="corr-kel' + data.id + '" class="form-control" onchange="fillpostalcode(this)">';
    html += '<option value="0">Select Kelurahan</option>';
    if (dataform["cor-kelurahan"]) {
        $.each(dataform["cor-kelurahan"]["data"], function (key, value) {
            selected = "";
            if (data["cor-address"].kelurahan_id && data["cor-address"].kelurahan_id.kecamatan_id == value.kecamatan_id) {
                if (value.id == data["cor-address"].kelurahan_id.id) {
                    selected = "selected";
                } else {
                    selected = "";
                }
                html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
            }
        });
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">Postalcode</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="corr-postalcode" id="corr-postalcode' + data.id + '" class="form-control">';
    html += '<option value = "0">Select Postalcode</option>';
    if (dataform["cor-postal_code"]) {
        $.each(dataform["cor-postal_code"]["data"], function (key, value) {
            selected = "";
            if (data["cor-address"].postal_code_id && data["cor-address"].postal_code_id.kecamatan_id == value.kecamatan_id) {
                if (value.id == data["cor-address"].postal_code_id.id) {
                    selected = "selected";
                } else {
                    selected = "";
                }
                html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
            }
        });
    }
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label for="corr-rt" class="control-label mb-1">RT/RW</label>';
    html += '<div class="form-group">';
    html += '<div class="row">';
    html += '<div class="col-6">';
    var cort;
    if (data["cor-address"].rt) {
        cort = data["cor-address"].rt;
    } else {
        cort = "";
    }
    html += '<input id="corr-rt' + data.id + '" type="text" class="form-control" value="' + cort + '">';
    html += "</div>";
    html += '<div class="col-6">';
    var corw;
    if (data["cor-address"].rw) {
        corw = data["cor-address"].rw;
    } else {
        corw = "";
    }
    html += '<input id="corr-rw' + data.id + '" type="text" class="form-control" value="' + corw + '">';
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="modal-footer">';
    html += '<div class="items-link items-link2"><a onclick="editCorres(' + data.id + ')" style="cursor: pointer;"><i class="fa fa-check-square"></i> Save</a></div>';
    html += '<div class="items-link items-link2"><a data-dismiss="modal" style="cursor: pointer;"><i class="fa fa-times"></i> Cancel</a></div>';
    html += "</div>";
    html += "</div>";
    html += '<div class="tab-pane fade" id="nav-edu' + data.id + '" role="tabpanel" aria-labelledby="nav-edu-tab">';
    html += '<div class="card-body card-block">';
    html += '<div class="row">';
    html += '<div class="col-12">';
    html += '<label class="control-label mb-1">Last Education</label>';
    html += '<div class="col-12 col-md-9">';
    html += '<select name="lastedu" id="lastedu' + data.id + '" class="form-control">';
    html += '<option value = "0">Select Education Level</option>';
    $.each(dataform["level_education"]["data"], function (key, value) {
        selected = "";
        if (data["history_education"].level_education) {
            if (value.id == data["history_education"].level_education) {
                selected = "selected";
            } else {
                selected = "";
            }
        }
        html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
    });
    html += "</select>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="bordertop">';
    html += '<label class="control-label mb-1">Educational Background</label>';
    html += "</div>";
    html += '<div class="table table-sm table-hover table-responsive table-bordered">';
    html += '<table id="edutable">';
    html += "<thead class='thead-light'>";
    html += "<tr>";
    html += '<th class="th-middle" rowspan="2">Level</th>';
    html += '<th class="th-middle" rowspan="2">Institution Name</th>';
    html += '<th class="th-middle" rowspan="2">City</th>';
    html += '<th class="th-middle" rowspan="2">Majors</th>';
    html += '<th class="th-middle" colspan="2">Year</th>';
    html += '<th class="th-middle" rowspan="2">Passed/ No</th>';
    html += "</tr>";
    html += "<tr>";
    html += "<th class='th-middle'>Start</th>";
    html += "<th class='th-middle'>End</th>";
    html += "</tr>";
    html += "</thead>";
    html += "<tbody>";
    html += "<tr>";
    html += "<td>Primary School</td>";
    var nama_sd;
    if (data["history_education"].nama_sd) {
        nama_sd = data["history_education"].nama_sd;
    } else {
        nama_sd = "";
    }
    html += '<td><input id="nama_sd' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + nama_sd + '"></td>';
    var City_sd;
    if (data["history_education"].City_sd) {
        City_sd = data["history_education"].City_sd;
    } else {
        City_sd = "";
    }
    html += '<td><input id="City_sd' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_sd + '"></td>';
    var jurusan_sd;
    if (data["history_education"].jurusan_sd) {
        jurusan_sd = data["history_education"].jurusan_sd;
    } else {
        jurusan_sd = "";
    }
    html += '<td><input id="jurusan_sd' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + jurusan_sd + '" disabled></td>';
    var masuk_sd;
    if (data["history_education"].masuk_sd) {
        masuk_sd = data["history_education"].masuk_sd;
    } else {
        masuk_sd = "";
    }
    html += '<td><input id="masuk_sd' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + masuk_sd + '"></td>';
    var Passed_sd;
    if (data["history_education"].Passed_sd) {
        Passed_sd = data["history_education"].Passed_sd;
    } else {
        Passed_sd = "";
    }
    html += '<td><input id="Passed_sd' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + Passed_sd + '"></td>';
    html += "<td>";
    html += '<select id="status_sd' + data.id + '" class="input-sm form-control-sm form-control">';
    if ("1" == data["history_education"].status_sd) {
        html += '<option value="1" selected>Passed</option>';
        html += '<option value="2">No</option>';
    } else if ("2" == data["history_education"].status_sd) {
        html += '<option value="1">Passed</option>';
        html += '<option value="2" selected>No</option>';
    } else {
        html += '<option value="0" selected></option>';
        html += '<option value="1">Passed</option>';
        html += '<option value="2">No</option>';
    }
    html += "</select>";
    html += "</td>";
    html += "</tr>";
    html += "<tr>";
    html += "<td>Junior High School</td>";
    var nama_smp;
    if (data["history_education"].nama_smp) {
        nama_smp = data["history_education"].nama_smp;
    } else {
        nama_smp = "";
    }
    html += '<td><input id="nama_smp' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + nama_smp + '"></td>';
    var City_smp;
    if (data["history_education"].City_smp) {
        City_smp = data["history_education"].City_smp;
    } else {
        City_smp = "";
    }
    html += '<td><input id="City_smp' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_smp + '"></td>';
    var jurusan_smp;
    if (data["history_education"].jurusan_smp) {
        jurusan_smp = data["history_education"].jurusan_smp;
    } else {
        jurusan_smp = "";
    }
    html += '<td><input id="jurusan_smp' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + jurusan_smp + '" disabled></td>';
    var masuk_smp;
    if (data["history_education"].masuk_smp) {
        masuk_smp = data["history_education"].masuk_smp;
    } else {
        masuk_smp = "";
    }
    html += '<td><input id="masuk_smp' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + masuk_smp + '"></td>';
    var Passed_smp;
    if (data["history_education"].Passed_smp) {
        Passed_smp = data["history_education"].Passed_smp;
    } else {
        Passed_smp = "";
    }
    html += '<td><input id="Passed_smp' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + Passed_smp + '"></td>';
    html += "<td>";
    html += '<select id="status_smp' + data.id + '" class="input-sm form-control-sm form-control">';
    if ("1" == data["history_education"].status_smp) {
        html += '<option value="1" selected>Passed</option>';
        html += '<option value="2">No</option>';
    } else if ("2" == data["history_education"].status_smp) {
        html += '<option value="1">Passed</option>';
        html += '<option value="2" selected>No</option>';
    } else {
        html += '<option value="0" selected></option>';
        html += '<option value="1">Passed</option>';
        html += '<option value="2">No</option>';
    }
    html += "</select>";
    html += "</td>";
    html += "</tr>";
    html += "<tr>";
    html += "<td>High School</td>";
    var nama_sma;
    if (data["history_education"].nama_sma) {
        nama_sma = data["history_education"].nama_sma;
    } else {
        nama_sma = "";
    }
    html += '<td><input id="nama_sma' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + nama_sma + '"></td>';
    var City_sma;
    if (data["history_education"].City_sma) {
        City_sma = data["history_education"].City_sma;
    } else {
        City_sma = "";
    }
    html += '<td><input id="City_sma' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_sma + '"></td>';
    var jurusan_sma;
    if (data["history_education"].jurusan_sma) {
        jurusan_sma = data["history_education"].jurusan_sma;
    } else {
        jurusan_sma = "";
    }
    html += '<td><input id="jurusan_sma' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + jurusan_sma + '"></td>';
    var masuk_sma;
    if (data["history_education"].masuk_sma) {
        masuk_sma = data["history_education"].masuk_sma;
    } else {
        masuk_sma = "";
    }
    html += '<td><input id="masuk_sma' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + masuk_sma + '"></td>';
    var Passed_sma;
    if (data["history_education"].Passed_sma) {
        Passed_sma = data["history_education"].Passed_sma;
    } else {
        Passed_sma = "";
    }
    html += '<td><input id="Passed_sma' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + Passed_sma + '"></td>';
    html += "<td>";
    html += '<select id="status_sma' + data.id + '" class="input-sm form-control-sm form-control">';
    if ("1" == data["history_education"].status_sma) {
        html += '<option value="1" selected>Passed</option>';
        html += '<option value="2">No</option>';
    } else if ("2" == data["history_education"].status_sma) {
        html += '<option value="1">Passed</option>';
        html += '<option value="2" selected>No</option>';
    } else {
        html += '<option value="0" selected></option>';
        html += '<option value="1">Passed</option>';
        html += '<option value="2">No</option>';
    }
    html += "</select>";
    html += "</td>";
    html += "</tr>";
    html += "<tr>";
    html += "<td>Bachelor's Degree</td>";
    var nama_s1;
    if (data["history_education"].nama_s1) {
        nama_s1 = data["history_education"].nama_s1;
    } else {
        nama_s1 = "";
    }
    html += '<td><input id="nama_s1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + nama_s1 + '"></td>';
    var City_s1;
    if (data["history_education"].City_s1) {
        City_s1 = data["history_education"].City_s1;
    } else {
        City_s1 = "";
    }
    html += '<td><input id="City_s1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_s1 + '"></td>';
    var jurusan_s1;
    if (data["history_education"].jurusan_s1) {
        jurusan_s1 = data["history_education"].jurusan_s1;
    } else {
        jurusan_s1 = "";
    }
    html += '<td><input id="jurusan_s1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + jurusan_s1 + '"></td>';
    var masuk_s1;
    if (data["history_education"].masuk_s1) {
        masuk_s1 = data["history_education"].masuk_s1;
    } else {
        masuk_s1 = "";
    }
    html += '<td><input id="masuk_s1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + masuk_s1 + '"></td>';
    var Passed_s1;
    if (data["history_education"].Passed_s1) {
        Passed_s1 = data["history_education"].Passed_s1;
    } else {
        Passed_s1 = "";
    }
    html += '<td><input id="Passed_s1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + Passed_s1 + '"></td>';
    html += "<td>";
    html += '<select id="status_s1' + data.id + '" class="input-sm form-control-sm form-control">';
    if ("1" == data["history_education"].status_s1) {
        html += '<option value="1" selected>Passed</option>';
        html += '<option value="2">No</option>';
    } else if ("2" == data["history_education"].status_s1) {
        html += '<option value="1">Passed</option>';
        html += '<option value="2" selected>No</option>';
    } else {
        html += '<option value="0" selected></option>';
        html += '<option value="1">Passed</option>';
        html += '<option value="2">No</option>';
    }
    html += "</select>";
    html += "</td>";
    html += "</tr>";
    html += "<tr>";
    html += "<td>Master's Degree</td>";
    var nama_s2;
    if (data["history_education"].nama_s2) {
        nama_s2 = data["history_education"].nama_s2;
    } else {
        nama_s2 = "";
    }
    html += '<td><input id="nama_s2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + nama_s2 + '"></td>';
    var City_s2;
    if (data["history_education"].City_s2) {
        City_s2 = data["history_education"].City_s2;
    } else {
        City_s2 = "";
    }
    html += '<td><input id="City_s2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_s2 + '"></td>';
    var jurusan_s2;
    if (data["history_education"].jurusan_s2) {
        jurusan_s2 = data["history_education"].jurusan_s2;
    } else {
        jurusan_s2 = "";
    }
    html += '<td><input id="jurusan_s2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + jurusan_s2 + '"></td>';
    var masuk_s2;
    if (data["history_education"].masuk_s2) {
        masuk_s2 = data["history_education"].masuk_s2;
    } else {
        masuk_s2 = "";
    }
    html += '<td><input id="masuk_s2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + masuk_s2 + '"></td>';
    var Passed_s2;
    if (data["history_education"].Passed_s2) {
        Passed_s2 = data["history_education"].Passed_s2;
    } else {
        Passed_s2 = "";
    }
    html += '<td><input id="Passed_s2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + Passed_s2 + '"></td>';
    html += "<td>";
    html += '<select id="status_s2' + data.id + '" class="input-sm form-control-sm form-control">';
    if ("1" == data["history_education"].status_s2) {
        html += '<option value="1" selected>Passed</option>';
        html += '<option value="2">No</option>';
    } else if ("2" == data["history_education"].status_s2) {
        html += '<option value="1">Passed</option>';
        html += '<option value="2" selected>No</option>';
    } else {
        html += '<option value="0" selected></option>';
        html += '<option value="1">Passed</option>';
        html += '<option value="2">No</option>';
    }
    html += "</select>";
    html += "</td>";
    html += "</tr>";
    html += "<tr>";
    html += "<td>Doctoral Degree</td>";
    var nama_s3;
    if (data["history_education"].nama_s3) {
        nama_s3 = data["history_education"].nama_s3;
    } else {
        nama_s3 = "";
    }
    html += '<td><input id="nama_s3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + nama_s3 + '"></td>';
    var City_s3;
    if (data["history_education"].City_s3) {
        City_s3 = data["history_education"].City_s3;
    } else {
        City_s3 = "";
    }
    html += '<td><input id="City_s3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_s3 + '"></td>';
    var jurusan_s3;
    if (data["history_education"].jurusan_s3) {
        jurusan_s3 = data["history_education"].jurusan_s3;
    } else {
        jurusan_s3 = "";
    }
    html += '<td><input id="jurusan_s3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + jurusan_s3 + '"></td>';
    var masuk_s3;
    if (data["history_education"].masuk_s3) {
        masuk_s3 = data["history_education"].masuk_s3;
    } else {
        masuk_s3 = "";
    }
    html += '<td><input id="masuk_s3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + masuk_s3 + '"></td>';
    var Passed_s3;
    if (data["history_education"].Passed_s3) {
        Passed_s3 = data["history_education"].Passed_s3;
    } else {
        Passed_s3 = "";
    }
    html += '<td><input id="Passed_s3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + Passed_s3 + '"></td>';
    html += "<td>";
    html += '<select id="status_s3' + data.id + '" class="input-sm form-control-sm form-control">';
    if ("1" == data["history_education"].status_s3) {
        html += '<option value="1" selected>Passed</option>';
        html += '<option value="2">No</option>';
    } else if ("2" == data["history_education"].status_s3) {
        html += '<option value="1">Passed</option>';
        html += '<option value="2" selected>No</option>';
    } else {
        html += '<option value="0" selected></option>';
        html += '<option value="1">Passed</option>';
        html += '<option value="2">No</option>';
    }
    html += "</select>";
    html += "</td>";
    html += "</tr>";
    html += "</tbody>";
    html += "</table>";
    html += "</div>";
    html += '<div class="bordertop">';
    html += '<label class="control-label mb-1">Non-Formal Education</label>';
    html += "</div>";
    html += '<div class="table table-sm table-hover table-responsive table-bordered">';
    html += '<table id="trainingtable">';
    html += "<thead class='thead-light'>";
    html += "<tr>";
    html += "<th class='th-middle'>Field</th>";
    html += "<th class='th-middle'>Institution</th>";
    html += "<th class='th-middle'>City</th>";
    html += "<th class='th-middle'>Course Length</th>";
    html += "<th class='th-middle'>Year</th>";
    html += "<th class='th-middle'>Financed by</th>";
    html += "</tr>";
    html += "</thead>";
    html += "<tbody>";
    html += "<tr>";
    var bidang1;
    if (data["history_education"].bidang1) {
        bidang1 = data["history_education"].bidang1;
    } else {
        bidang1 = "";
    }
    html += '<td><input id="bidang1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + bidang1 + '"></td>';
    var penyelenggara1;
    if (data["history_education"].penyelenggara1) {
        penyelenggara1 = data["history_education"].penyelenggara1;
    } else {
        penyelenggara1 = "";
    }
    html += '<td><input id="penyelenggara1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + penyelenggara1 + '"></td>';
    var City_kursus1;
    if (data["history_education"].City_kursus1) {
        City_kursus1 = data["history_education"].City_kursus1;
    } else {
        City_kursus1 = "";
    }
    html += '<td><input id="City_kursus1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_kursus1 + '"></td>';
    var lama_kursus1;
    if (data["history_education"].lama_kursus1) {
        lama_kursus1 = data["history_education"].lama_kursus1;
    } else {
        lama_kursus1 = "";
    }
    html += '<td><input id="lama_kursus1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + lama_kursus1 + '"></td>';
    var tahun_masuk1;
    if (data["history_education"].tahun_masuk1) {
        tahun_masuk1 = data["history_education"].tahun_masuk1;
    } else {
        tahun_masuk1 = "";
    }
    html += '<td><input id="tahun_masuk1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + tahun_masuk1 + '"></td>';
    var biaya1;
    if (data["history_education"].biaya1) {
        biaya1 = data["history_education"].biaya1;
    } else {
        biaya1 = "";
    }
    html += '<td><input id="biaya1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + biaya1 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var bidang2;
    if (data["history_education"].bidang2) {
        bidang2 = data["history_education"].bidang2;
    } else {
        bidang2 = "";
    }
    html += '<td><input id="bidang2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + bidang2 + '"></td>';
    var penyelenggara2;
    if (data["history_education"].penyelenggara2) {
        penyelenggara2 = data["history_education"].penyelenggara2;
    } else {
        penyelenggara2 = "";
    }
    html += '<td><input id="penyelenggara2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + penyelenggara2 + '"></td>';
    var City_kursus2;
    if (data["history_education"].City_kursus2) {
        City_kursus2 = data["history_education"].City_kursus2;
    } else {
        City_kursus2 = "";
    }
    html += '<td><input id="City_kursus2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_kursus2 + '"></td>';
    var lama_kursus2;
    if (data["history_education"].lama_kursus2) {
        lama_kursus2 = data["history_education"].lama_kursus2;
    } else {
        lama_kursus2 = "";
    }
    html += '<td><input id="lama_kursus2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + lama_kursus2 + '"></td>';
    var tahun_masuk2;
    if (data["history_education"].tahun_masuk2) {
        tahun_masuk2 = data["history_education"].tahun_masuk2;
    } else {
        tahun_masuk2 = "";
    }
    html += '<td><input id="tahun_masuk2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + tahun_masuk2 + '"></td>';
    var biaya2;
    if (data["history_education"].biaya2) {
        biaya2 = data["history_education"].biaya2;
    } else {
        biaya2 = "";
    }
    html += '<td><input id="biaya2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + biaya2 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var bidang3;
    if (data["history_education"].bidang3) {
        bidang3 = data["history_education"].bidang3;
    } else {
        bidang3 = "";
    }
    html += '<td><input id="bidang3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + bidang3 + '"></td>';
    var penyelenggara3;
    if (data["history_education"].penyelenggara3) {
        penyelenggara3 = data["history_education"].penyelenggara3;
    } else {
        penyelenggara3 = "";
    }
    html += '<td><input id="penyelenggara3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + penyelenggara3 + '"></td>';
    var City_kursus3;
    if (data["history_education"].City_kursus3) {
        City_kursus3 = data["history_education"].City_kursus3;
    } else {
        City_kursus3 = "";
    }
    html += '<td><input id="City_kursus3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_kursus3 + '"></td>';
    var lama_kursus3;
    if (data["history_education"].lama_kursus3) {
        lama_kursus3 = data["history_education"].lama_kursus3;
    } else {
        lama_kursus3 = "";
    }
    html += '<td><input id="lama_kursus3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + lama_kursus3 + '"></td>';
    var tahun_masuk3;
    if (data["history_education"].tahun_masuk3) {
        tahun_masuk3 = data["history_education"].tahun_masuk3;
    } else {
        tahun_masuk3 = "";
    }
    html += '<td><input id="tahun_masuk3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + tahun_masuk3 + '"></td>';
    var biaya3;
    if (data["history_education"].biaya3) {
        biaya3 = data["history_education"].biaya3;
    } else {
        biaya3 = "";
    }
    html += '<td><input id="biaya3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + biaya3 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var bidang4;
    if (data["history_education"].bidang4) {
        bidang4 = data["history_education"].bidang4;
    } else {
        bidang4 = "";
    }
    html += '<td><input id="bidang4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + bidang4 + '"></td>';
    var penyelenggara4;
    if (data["history_education"].penyelenggara4) {
        penyelenggara4 = data["history_education"].penyelenggara4;
    } else {
        penyelenggara4 = "";
    }
    html += '<td><input id="penyelenggara4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + penyelenggara4 + '"></td>';
    var City_kursus4;
    if (data["history_education"].City_kursus4) {
        City_kursus4 = data["history_education"].City_kursus4;
    } else {
        City_kursus4 = "";
    }
    html += '<td><input id="City_kursus4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_kursus4 + '"></td>';
    var lama_kursus4;
    if (data["history_education"].lama_kursus4) {
        lama_kursus4 = data["history_education"].lama_kursus4;
    } else {
        lama_kursus4 = "";
    }
    html += '<td><input id="lama_kursus4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + lama_kursus4 + '"></td>';
    var tahun_masuk4;
    if (data["history_education"].tahun_masuk4) {
        tahun_masuk4 = data["history_education"].tahun_masuk4;
    } else {
        tahun_masuk4 = "";
    }
    html += '<td><input id="tahun_masuk4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + tahun_masuk4 + '"></td>';
    var biaya4;
    if (data["history_education"].biaya4) {
        biaya4 = data["history_education"].biaya4;
    } else {
        biaya4 = "";
    }
    html += '<td><input id="biaya4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + biaya4 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var bidang5;
    if (data["history_education"].bidang5) {
        bidang5 = data["history_education"].bidang5;
    } else {
        bidang5 = "";
    }
    html += '<td><input id="bidang5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + bidang5 + '"></td>';
    var penyelenggara5;
    if (data["history_education"].penyelenggara5) {
        penyelenggara5 = data["history_education"].penyelenggara5;
    } else {
        penyelenggara5 = "";
    }
    html += '<td><input id="penyelenggara5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + penyelenggara5 + '"></td>';
    var City_kursus5;
    if (data["history_education"].City_kursus5) {
        City_kursus5 = data["history_education"].City_kursus5;
    } else {
        City_kursus5 = "";
    }
    html += '<td><input id="City_kursus5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_kursus5 + '"></td>';
    var lama_kursus5;
    if (data["history_education"].lama_kursus5) {
        lama_kursus5 = data["history_education"].lama_kursus5;
    } else {
        lama_kursus5 = "";
    }
    html += '<td><input id="lama_kursus5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + lama_kursus5 + '"></td>';
    var tahun_masuk5;
    if (data["history_education"].tahun_masuk5) {
        tahun_masuk5 = data["history_education"].tahun_masuk5;
    } else {
        tahun_masuk5 = "";
    }
    html += '<td><input id="tahun_masuk5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + tahun_masuk5 + '"></td>';
    var biaya5;
    if (data["history_education"].biaya5) {
        biaya5 = data["history_education"].biaya5;
    } else {
        biaya5 = "";
    }
    html += '<td><input id="biaya5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + biaya5 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var bidang6;
    if (data["history_education"].bidang6) {
        bidang6 = data["history_education"].bidang6;
    } else {
        bidang6 = "";
    }
    html += '<td><input id="bidang6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + bidang6 + '"></td>';
    var penyelenggara6;
    if (data["history_education"].penyelenggara6) {
        penyelenggara6 = data["history_education"].penyelenggara6;
    } else {
        penyelenggara6 = "";
    }
    html += '<td><input id="penyelenggara6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + penyelenggara6 + '"></td>';
    var City_kursus6;
    if (data["history_education"].City_kursus6) {
        City_kursus6 = data["history_education"].City_kursus6;
    } else {
        City_kursus6 = "";
    }
    html += '<td><input id="City_kursus6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + City_kursus6 + '"></td>';
    var lama_kursus6;
    if (data["history_education"].lama_kursus6) {
        lama_kursus6 = data["history_education"].lama_kursus6;
    } else {
        lama_kursus6 = "";
    }
    html += '<td><input id="lama_kursus6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + lama_kursus6 + '"></td>';
    var tahun_masuk6;
    if (data["history_education"].tahun_masuk6) {
        tahun_masuk6 = data["history_education"].tahun_masuk6;
    } else {
        tahun_masuk6 = "";
    }
    html += '<td><input id="tahun_masuk6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + tahun_masuk6 + '"></td>';
    var biaya6;
    if (data["history_education"].biaya6) {
        biaya6 = data["history_education"].biaya6;
    } else {
        biaya6 = "";
    }
    html += '<td><input id="biaya6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + biaya6 + '"></td>';
    html += "</tr>";
    html += "</tbody>";
    html += "</table>";
    html += "</div>";
    html += "</div>";
    html += '<div class="modal-footer">';
    html += '<div class="items-link items-link2"><a onclick="editEdu(' + data.id + ')" style="cursor: pointer;"><i class="fa fa-check-square"></i> Save</a></div>';
    html += '<div class="items-link items-link2"><a data-dismiss="modal" style="cursor: pointer;"><i class="fa fa-times"></i> Cancel</a></div>';
    html += "</div>";
    html += "</div>";
    html += '<div class="tab-pane fade" id="nav-work' + data.id + '" role="tabpanel" aria-labelledby="nav-work-tab">';
    html += '<div class="card-body card-block">';
    html += '<div class="row">';
    html += '<div class="col-12">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">NPWP</label>';
    var npwp;
    if (data["job_experience"].npwp) {
        npwp = data["job_experience"].npwp;
    } else {
        npwp = "";
    }
    html += '<input type="text" name="npwp" id="npwp' + data.id + '" class="form-control" value="' + npwp + '">';
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">BPJS Ketenagakerjaan</label>';
    var bpjstk;
    if (data["job_experience"].bpjstk) {
        bpjstk = data["job_experience"].bpjstk;
    } else {
        bpjstk = "";
    }
    html += '<input type="text" name="bpjstk" id="bpjstk' + data.id + '" class="form-control" value="' + bpjstk + '">';
    html += "</div>";
    html += "</div>";
    html += '<div class="col-6">';
    html += '<div class="form-group">';
    html += '<label class="control-label mb-1">BPJS Kesehatan</label>';
    var bpjs;
    if (data["job_experience"].bpjs) {
        bpjs = data["job_experience"].bpjs;
    } else {
        bpjs = "";
    }
    html += '<input type="text" name="bpjs" id="bpjs' + data.id + '" class="form-control" value="' + bpjs + '">';
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += '<div class="bordertop">';
    html += '<label class="control-label mb-1">Sertifikat Keahlian Kerja (SKA)</label>';
    html += "</div>";
    html += '<div class="table table-sm table-hover table-responsive table-bordered">';
    html += '<table id="skatable">';
    html += "<thead class='thead-light'>";
    html += "<tr>";
    html += '<th class="th-middle" rowspan="2">Professional Association Members</th>';
    html += '<th class="th-middle" rowspan="2">TA Clasification</th>';
    html += '<th class="th-middle" rowspan="2">No. SKA</th>';
    html += '<th class="th-middle" colspan="2">SKA Validity Period</th>';
    html += "</tr>";
    html += "<tr>";
    html += "<th class='th-middle'>Start</th>";
    html += "<th class='th-middle'>End</th>";
    html += "</tr>";
    html += "</thead>";
    html += "<tbody>";
    html += "<tr>";
    var aap1;
    if (data["job_experience"].aap1) {
        aap1 = data["job_experience"].aap1;
    } else {
        aap1 = "";
    }
    html += '<td><input id="aap1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + aap1 + '"></td>';
    var klasifikasi1;
    if (data["job_experience"].klasifikasi1) {
        klasifikasi1 = data["job_experience"].klasifikasi1;
    } else {
        klasifikasi1 = "";
    }
    html += '<td><input id="klasifikasi1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + klasifikasi1 + '"></td>';
    var ska1;
    if (data["job_experience"].ska1) {
        ska1 = data["job_experience"].ska1;
    } else {
        ska1 = "";
    }
    html += '<td><input id="ska1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ska1 + '"></td>';
    var skastart1;
    if (data["job_experience"].skastart1) {
        skastart1 = data["job_experience"].skastart1;
    } else {
        skastart1 = "";
    }
    html += '<td><input id="skastart1' + data.id + '" type="date" class="input-sm form-control-sm form-control" value="' + skastart1 + '"></td>';
    var skaend1;
    if (data["job_experience"].skaend1) {
        skaend1 = data["job_experience"].skaend1;
    } else {
        skaend1 = "";
    }
    html += '<td><input id="skaend1' + data.id + '" type="date" class="input-sm form-control-sm form-control" value="' + skaend1 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var aap2;
    if (data["job_experience"].aap2) {
        aap2 = data["job_experience"].aap2;
    } else {
        aap2 = "";
    }
    html += '<td><input id="aap2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + aap2 + '"></td>';
    var klasifikasi2;
    if (data["job_experience"].klasifikasi2) {
        klasifikasi2 = data["job_experience"].klasifikasi2;
    } else {
        klasifikasi2 = "";
    }
    html += '<td><input id="klasifikasi2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + klasifikasi2 + '"></td>';
    var ska2;
    if (data["job_experience"].ska2) {
        ska2 = data["job_experience"].ska2;
    } else {
        ska2 = "";
    }
    html += '<td><input id="ska2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ska2 + '"></td>';
    var skastart2;
    if (data["job_experience"].skastart2) {
        skastart2 = data["job_experience"].skastart2;
    } else {
        skastart2 = "";
    }
    html += '<td><input id="skastart2' + data.id + '" type="date" class="input-sm form-control-sm form-control" value="' + skastart2 + '"></td>';
    var skaend2;
    if (data["job_experience"].skaend2) {
        skaend2 = data["job_experience"].skaend2;
    } else {
        skaend2 = "";
    }
    html += '<td><input id="skaend2' + data.id + '" type="date" class="input-sm form-control-sm form-control" value="' + skaend2 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var aap3;
    if (data["job_experience"].aap3) {
        aap3 = data["job_experience"].aap3;
    } else {
        aap3 = "";
    }
    html += '<td><input id="aap3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + aap3 + '"></td>';
    var klasifikasi3;
    if (data["job_experience"].klasifikasi3) {
        klasifikasi3 = data["job_experience"].klasifikasi3;
    } else {
        klasifikasi3 = "";
    }
    html += '<td><input id="klasifikasi3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + klasifikasi3 + '"></td>';
    var ska3;
    if (data["job_experience"].ska3) {
        ska3 = data["job_experience"].ska3;
    } else {
        ska3 = "";
    }
    html += '<td><input id="ska3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ska3 + '"></td>';
    var skastart3;
    if (data["job_experience"].skastart3) {
        skastart3 = data["job_experience"].skastart3;
    } else {
        skastart3 = "";
    }
    html += '<td><input id="skastart3' + data.id + '" type="date" class="input-sm form-control-sm form-control" value="' + skastart3 + '"></td>';
    var skaend3;
    if (data["job_experience"].skaend3) {
        skaend3 = data["job_experience"].skaend3;
    } else {
        skaend3 = "";
    }
    html += '<td><input id="skaend3' + data.id + '" type="date" class="input-sm form-control-sm form-control" value="' + skaend3 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var aap4;
    if (data["job_experience"].aap4) {
        aap4 = data["job_experience"].aap4;
    } else {
        aap4 = "";
    }
    html += '<td><input id="aap4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + aap4 + '"></td>';
    var klasifikasi4;
    if (data["job_experience"].klasifikasi4) {
        klasifikasi4 = data["job_experience"].klasifikasi4;
    } else {
        klasifikasi4 = "";
    }
    html += '<td><input id="klasifikasi4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + klasifikasi4 + '"></td>';
    var ska4;
    if (data["job_experience"].ska4) {
        ska4 = data["job_experience"].ska4;
    } else {
        ska4 = "";
    }
    html += '<td><input id="ska4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ska4 + '"></td>';
    var skastart4;
    if (data["job_experience"].skastart4) {
        skastart4 = data["job_experience"].skastart4;
    } else {
        skastart4 = "";
    }
    html += '<td><input id="skastart4' + data.id + '" type="date" class="input-sm form-control-sm form-control" value="' + skastart4 + '"></td>';
    var skaend4;
    if (data["job_experience"].skaend4) {
        skaend4 = data["job_experience"].skaend4;
    } else {
        skaend4 = "";
    }
    html += '<td><input id="skaend4' + data.id + '" type="date" class="input-sm form-control-sm form-control" value="' + skaend4 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var aap5;
    if (data["job_experience"].aap5) {
        aap5 = data["job_experience"].aap5;
    } else {
        aap5 = "";
    }
    html += '<td><input id="aap5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + aap5 + '"></td>';
    var klasifikasi5;
    if (data["job_experience"].klasifikasi5) {
        klasifikasi5 = data["job_experience"].klasifikasi5;
    } else {
        klasifikasi5 = "";
    }
    html += '<td><input id="klasifikasi5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + klasifikasi5 + '"></td>';
    var ska5;
    if (data["job_experience"].ska5) {
        ska5 = data["job_experience"].ska5;
    } else {
        ska5 = "";
    }
    html += '<td><input id="ska5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ska5 + '"></td>';
    var skastart5;
    if (data["job_experience"].skastart5) {
        skastart5 = data["job_experience"].skastart5;
    } else {
        skastart5 = "";
    }
    html += '<td><input id="skastart5' + data.id + '" type="date" class="input-sm form-control-sm form-control" value="' + skastart5 + '"></td>';
    var skaend5;
    if (data["job_experience"].skaend5) {
        skaend5 = data["job_experience"].skaend5;
    } else {
        skaend5 = "";
    }
    html += '<td><input id="skaend5' + data.id + '" type="date" class="input-sm form-control-sm form-control" value="' + skaend5 + '"></td>';
    html += "</tr>";
    html += "</tbody>";
    html += "</table>";
    html += "</div>";
    html += '<div class="bordertop">';
    html += '<label class="control-label mb-1">Work Experience</label>';
    html += "</div>";
    html += '<div class="table table-sm table-hover table-responsive table-bordered">';
    html += '<table id="worktable">';
    html += "<thead class='thead-light'>";
    html += "<tr>";
    html += '<th class="th-middle" rowspan="2">Company</th>';
    html += '<th class="th-middle" rowspan="2">Address</th>';
    html += '<th class="th-middle" rowspan="2">Position</th>';
    html += '<th class="th-middle" colspan="2">Period</th>';
    html += '<th class="th-middle" rowspan="2">Info</th>';
    html += "</tr>";
    html += "<tr>";
    html += '<th class="th-middle">Start</th>';
    html += '<th class="th-middle">End</th>';
    html += "</tr>";
    html += "</thead>";
    html += "<tbody>";
    html += "<tr>";
    var company1;
    if (data["job_experience"].company1) {
        company1 = data["job_experience"].company1;
    } else {
        company1 = "";
    }
    html += '<td><input id="company1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + company1 + '"></td>';
    var comaddress1;
    if (data["job_experience"].comaddress1) {
        comaddress1 = data["job_experience"].comaddress1;
    } else {
        comaddress1 = "";
    }
    html += '<td><input id="comaddress1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + comaddress1 + '"></td>';
    var work_position1;
    if (data["job_experience"].work_position1) {
        work_position1 = data["job_experience"].work_position1;
    } else {
        work_position1 = "";
    }
    html += '<td><input id="work_position1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + work_position1 + '"></td>';
    var starttime1;
    if (data["job_experience"].starttime1) {
        starttime1 = data["job_experience"].starttime1;
    } else {
        starttime1 = "";
    }
    html += '<td><input id="starttime1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + starttime1 + '"></td>';
    var endtime1;
    if (data["job_experience"].endtime1) {
        endtime1 = data["job_experience"].endtime1;
    } else {
        endtime1 = "";
    }
    html += '<td><input id="endtime1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + endtime1 + '"></td>';
    var ket1;
    if (data["job_experience"].ket1) {
        ket1 = data["job_experience"].ket1;
    } else {
        ket1 = "";
    }
    html += '<td><input id="ket1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket1 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var company2;
    if (data["job_experience"].company2) {
        company2 = data["job_experience"].company2;
    } else {
        company2 = "";
    }
    html += '<td><input id="company2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + company2 + '"></td>';
    var comaddress2;
    if (data["job_experience"].comaddress2) {
        comaddress2 = data["job_experience"].comaddress2;
    } else {
        comaddress2 = "";
    }
    html += '<td><input id="comaddress2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + comaddress2 + '"></td>';
    var work_position2;
    if (data["job_experience"].work_position2) {
        work_position2 = data["job_experience"].work_position2;
    } else {
        work_position2 = "";
    }
    html += '<td><input id="work_position2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + work_position2 + '"></td>';
    var starttime2;
    if (data["job_experience"].starttime2) {
        starttime2 = data["job_experience"].starttime2;
    } else {
        starttime2 = "";
    }
    html += '<td><input id="starttime2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + starttime2 + '"></td>';
    var endtime2;
    if (data["job_experience"].endtime2) {
        endtime2 = data["job_experience"].endtime2;
    } else {
        endtime2 = "";
    }
    html += '<td><input id="endtime2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + endtime2 + '"></td>';
    var ket2;
    if (data["job_experience"].ket2) {
        ket2 = data["job_experience"].ket2;
    } else {
        ket2 = "";
    }
    html += '<td><input id="ket2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket2 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var company3;
    if (data["job_experience"].company3) {
        company3 = data["job_experience"].company3;
    } else {
        company3 = "";
    }
    html += '<td><input id="company3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + company3 + '"></td>';
    var comaddress3;
    if (data["job_experience"].comaddress3) {
        comaddress3 = data["job_experience"].comaddress3;
    } else {
        comaddress3 = "";
    }
    html += '<td><input id="comaddress3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + comaddress3 + '"></td>';
    var work_position3;
    if (data["job_experience"].work_position3) {
        work_position3 = data["job_experience"].work_position3;
    } else {
        work_position3 = "";
    }
    html += '<td><input id="work_position3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + work_position3 + '"></td>';
    var starttime3;
    if (data["job_experience"].starttime3) {
        starttime3 = data["job_experience"].starttime3;
    } else {
        starttime3 = "";
    }
    html += '<td><input id="starttime3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + starttime3 + '"></td>';
    var endtime3;
    if (data["job_experience"].endtime3) {
        endtime3 = data["job_experience"].endtime3;
    } else {
        endtime3 = "";
    }
    html += '<td><input id="endtime3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + endtime3 + '"></td>';
    var ket3;
    if (data["job_experience"].ket3) {
        ket3 = data["job_experience"].ket3;
    } else {
        ket3 = "";
    }
    html += '<td><input id="ket3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket3 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var company4;
    if (data["job_experience"].company4) {
        company4 = data["job_experience"].company4;
    } else {
        company4 = "";
    }
    html += '<td><input id="company4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + company4 + '"></td>';
    var comaddress4;
    if (data["job_experience"].comaddress4) {
        comaddress4 = data["job_experience"].comaddress4;
    } else {
        comaddress4 = "";
    }
    html += '<td><input id="comaddress4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + comaddress4 + '"></td>';
    var work_position4;
    if (data["job_experience"].work_position4) {
        work_position4 = data["job_experience"].work_position4;
    } else {
        work_position4 = "";
    }
    html += '<td><input id="work_position4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + work_position4 + '"></td>';
    var starttime4;
    if (data["job_experience"].starttime4) {
        starttime4 = data["job_experience"].starttime4;
    } else {
        starttime4 = "";
    }
    html += '<td><input id="starttime4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + starttime4 + '"></td>';
    var endtime4;
    if (data["job_experience"].endtime4) {
        endtime4 = data["job_experience"].endtime4;
    } else {
        endtime4 = "";
    }
    html += '<td><input id="endtime4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + endtime4 + '"></td>';
    var ket4;
    if (data["job_experience"].ket4) {
        ket4 = data["job_experience"].ket4;
    } else {
        ket4 = "";
    }
    html += '<td><input id="ket4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket4 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var company5;
    if (data["job_experience"].company5) {
        company5 = data["job_experience"].company5;
    } else {
        company5 = "";
    }
    html += '<td><input id="company5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + company5 + '"></td>';
    var comaddress5;
    if (data["job_experience"].comaddress5) {
        comaddress5 = data["job_experience"].comaddress5;
    } else {
        comaddress5 = "";
    }
    html += '<td><input id="comaddress5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + comaddress5 + '"></td>';
    var work_position5;
    if (data["job_experience"].work_position5) {
        work_position5 = data["job_experience"].work_position5;
    } else {
        work_position5 = "";
    }
    html += '<td><input id="work_position5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + work_position5 + '"></td>';
    var starttime5;
    if (data["job_experience"].starttime5) {
        starttime5 = data["job_experience"].starttime5;
    } else {
        starttime5 = "";
    }
    html += '<td><input id="starttime5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + starttime5 + '"></td>';
    var endtime5;
    if (data["job_experience"].endtime5) {
        endtime5 = data["job_experience"].endtime5;
    } else {
        endtime5 = "";
    }
    html += '<td><input id="endtime5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + endtime5 + '"></td>';
    var ket5;
    if (data["job_experience"].ket5) {
        ket5 = data["job_experience"].ket5;
    } else {
        ket5 = "";
    }
    html += '<td><input id="ket5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket5 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var company6;
    if (data["job_experience"].company6) {
        company6 = data["job_experience"].company6;
    } else {
        company6 = "";
    }
    html += '<td><input id="company6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + company6 + '"></td>';
    var comaddress6;
    if (data["job_experience"].comaddress6) {
        comaddress6 = data["job_experience"].comaddress6;
    } else {
        comaddress6 = "";
    }
    html += '<td><input id="comaddress6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + comaddress6 + '"></td>';
    var work_position6;
    if (data["job_experience"].work_position6) {
        work_position6 = data["job_experience"].work_position6;
    } else {
        work_position6 = "";
    }
    html += '<td><input id="work_position6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + work_position6 + '"></td>';
    var starttime6;
    if (data["job_experience"].starttime6) {
        starttime6 = data["job_experience"].starttime6;
    } else {
        starttime6 = "";
    }
    html += '<td><input id="starttime6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + starttime6 + '"></td>';
    var endtime6;
    if (data["job_experience"].endtime6) {
        endtime6 = data["job_experience"].endtime6;
    } else {
        endtime6 = "";
    }
    html += '<td><input id="endtime6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + endtime6 + '"></td>';
    var ket6;
    if (data["job_experience"].ket6) {
        ket6 = data["job_experience"].ket6;
    } else {
        ket6 = "";
    }
    html += '<td><input id="ket6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket6 + '"></td>';
    html += "</tr>";
    html += "</tbody>";
    html += "</table>";
    html += "</div>";
    html += '<div class="bordertop">';
    html += '<label class="control-label mb-1">Project Experience (PT.ESTI YASAGAMA)</label>';
    html += "</div>";
    html += '<div class="table table-sm table-hover table-responsive table-bordered">';
    html += '<table id="projecttable">';
    html += "<thead class='thead-light'>";
    html += "<tr>";
    html += '<th class="th-middle" rowspan="2">Project</th>';
    html += '<th class="th-middle" rowspan="2">Location</th>';
    html += '<th class="th-middle" rowspan="2">Position</th>';
    html += '<th class="th-middle" colspan="2">Period</th>';
    html += '<th class="th-middle" rowspan="2">Info</th>';
    html += "</tr>";
    html += "<tr>";
    html += '<th class="th-middle">Start</th>';
    html += '<th class="th-middle">End</th>';
    html += "</tr>";
    html += "</thead>";
    html += "<tbody>";
    html += "<tr>";
    var project1;
    if (data["job_experience"].project1) {
        project1 = data["job_experience"].project1;
    } else {
        project1 = "";
    }
    html += '<td><input id="project1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project1 + '"></td>';
    var project_address1;
    if (data["job_experience"].project_address1) {
        project_address1 = data["job_experience"].project_address1;
    } else {
        project_address1 = "";
    }
    html += '<td><input id="project_address1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_address1 + '"></td>';
    var project_position1;
    if (data["job_experience"].project_position1) {
        project_position1 = data["job_experience"].project_position1;
    } else {
        project_position1 = "";
    }
    html += '<td><input id="project_position1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_position1 + '"></td>';
    var start_project1;
    if (data["job_experience"].start_project1) {
        start_project1 = data["job_experience"].start_project1;
    } else {
        start_project1 = "";
    }
    html += '<td><input id="start_project1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + start_project1 + '"></td>';
    var end_project1;
    if (data["job_experience"].end_project1) {
        end_project1 = data["job_experience"].end_project1;
    } else {
        end_project1 = "";
    }
    html += '<td><input id="end_project1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + end_project1 + '"></td>';
    var ket_project1;
    if (data["job_experience"].ket_project1) {
        ket_project1 = data["job_experience"].ket_project1;
    } else {
        ket_project1 = "";
    }
    html += '<td><input id="ket_project1' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket_project1 + '"></td>';
    html += "</tr>";
    var project2;
    if (data["job_experience"].project2) {
        project2 = data["job_experience"].project2;
    } else {
        project2 = "";
    }
    html += '<td><input id="project2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project2 + '"></td>';
    var project_address2;
    if (data["job_experience"].project_address2) {
        project_address2 = data["job_experience"].project_address2;
    } else {
        project_address2 = "";
    }
    html += '<td><input id="project_address2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_address2 + '"></td>';
    var project_position2;
    if (data["job_experience"].project_position2) {
        project_position2 = data["job_experience"].project_position2;
    } else {
        project_position2 = "";
    }
    html += '<td><input id="project_position2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_position2 + '"></td>';
    var start_project2;
    if (data["job_experience"].start_project2) {
        start_project2 = data["job_experience"].start_project2;
    } else {
        start_project2 = "";
    }
    html += '<td><input id="start_project2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + start_project2 + '"></td>';
    var end_project2;
    if (data["job_experience"].end_project2) {
        end_project2 = data["job_experience"].end_project2;
    } else {
        end_project2 = "";
    }
    html += '<td><input id="end_project2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + end_project2 + '"></td>';
    var ket_project2;
    if (data["job_experience"].ket_project2) {
        ket_project2 = data["job_experience"].ket_project2;
    } else {
        ket_project2 = "";
    }
    html += '<td><input id="ket_project2' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket_project2 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var project3;
    if (data["job_experience"].project3) {
        project3 = data["job_experience"].project3;
    } else {
        project3 = "";
    }
    html += '<td><input id="project3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project3 + '"></td>';
    var project_address3;
    if (data["job_experience"].project_address3) {
        project_address3 = data["job_experience"].project_address3;
    } else {
        project_address3 = "";
    }
    html += '<td><input id="project_address3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_address3 + '"></td>';
    var project_position3;
    if (data["job_experience"].project_position3) {
        project_position3 = data["job_experience"].project_position3;
    } else {
        project_position3 = "";
    }
    html += '<td><input id="project_position3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_position3 + '"></td>';
    var start_project3;
    if (data["job_experience"].start_project3) {
        start_project3 = data["job_experience"].start_project3;
    } else {
        start_project3 = "";
    }
    html += '<td><input id="start_project3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + start_project3 + '"></td>';
    var end_project3;
    if (data["job_experience"].end_project3) {
        end_project3 = data["job_experience"].end_project3;
    } else {
        end_project3 = "";
    }
    html += '<td><input id="end_project3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + end_project3 + '"></td>';
    var ket_project3;
    if (data["job_experience"].ket_project3) {
        ket_project3 = data["job_experience"].ket_project3;
    } else {
        ket_project3 = "";
    }
    html += '<td><input id="ket_project3' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket_project3 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var project4;
    if (data["job_experience"].project4) {
        project4 = data["job_experience"].project4;
    } else {
        project4 = "";
    }
    html += '<td><input id="project4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project4 + '"></td>';
    var project_address4;
    if (data["job_experience"].project_address4) {
        project_address4 = data["job_experience"].project_address4;
    } else {
        project_address4 = "";
    }
    html += '<td><input id="project_address4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_address4 + '"></td>';
    var project_position4;
    if (data["job_experience"].project_position4) {
        project_position4 = data["job_experience"].project_position4;
    } else {
        project_position4 = "";
    }
    html += '<td><input id="project_position4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_position4 + '"></td>';
    var start_project4;
    if (data["job_experience"].start_project4) {
        start_project4 = data["job_experience"].start_project4;
    } else {
        start_project4 = "";
    }
    html += '<td><input id="start_project4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + start_project4 + '"></td>';
    var end_project4;
    if (data["job_experience"].end_project4) {
        end_project4 = data["job_experience"].end_project4;
    } else {
        end_project4 = "";
    }
    html += '<td><input id="end_project4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + end_project4 + '"></td>';
    var ket_project4;
    if (data["job_experience"].ket_project4) {
        ket_project4 = data["job_experience"].ket_project4;
    } else {
        ket_project4 = "";
    }
    html += '<td><input id="ket_project4' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket_project4 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var project5;
    if (data["job_experience"].project5) {
        project5 = data["job_experience"].project5;
    } else {
        project5 = "";
    }
    html += '<td><input id="project5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project5 + '"></td>';
    var project_address5;
    if (data["job_experience"].project_address5) {
        project_address5 = data["job_experience"].project_address5;
    } else {
        project_address5 = "";
    }
    html += '<td><input id="project_address5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_address5 + '"></td>';
    var project_position5;
    if (data["job_experience"].project_position5) {
        project_position5 = data["job_experience"].project_position5;
    } else {
        project_position5 = "";
    }
    html += '<td><input id="project_position5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_position5 + '"></td>';
    var start_project5;
    if (data["job_experience"].start_project5) {
        start_project5 = data["job_experience"].start_project5;
    } else {
        start_project5 = "";
    }
    html += '<td><input id="start_project5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + start_project5 + '"></td>';
    var end_project5;
    if (data["job_experience"].end_project5) {
        end_project5 = data["job_experience"].end_project5;
    } else {
        end_project5 = "";
    }
    html += '<td><input id="end_project5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + end_project5 + '"></td>';
    var ket_project5;
    if (data["job_experience"].ket_project5) {
        ket_project5 = data["job_experience"].ket_project5;
    } else {
        ket_project5 = "";
    }
    html += '<td><input id="ket_project5' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket_project5 + '"></td>';
    html += "</tr>";
    html += "<tr>";
    var project6;
    if (data["job_experience"].project6) {
        project6 = data["job_experience"].project6;
    } else {
        project6 = "";
    }
    html += '<td><input id="project6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project6 + '"></td>';
    var project_address6;
    if (data["job_experience"].project_address6) {
        project_address6 = data["job_experience"].project_address6;
    } else {
        project_address6 = "";
    }
    html += '<td><input id="project_address6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_address6 + '"></td>';
    var project_position6;
    if (data["job_experience"].project_position6) {
        project_position6 = data["job_experience"].project_position6;
    } else {
        project_position6 = "";
    }
    html += '<td><input id="project_position6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + project_position6 + '"></td>';
    var start_project6;
    if (data["job_experience"].start_project6) {
        start_project6 = data["job_experience"].start_project6;
    } else {
        start_project6 = "";
    }
    html += '<td><input id="start_project6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + start_project6 + '"></td>';
    var end_project6;
    if (data["job_experience"].end_project6) {
        end_project6 = data["job_experience"].end_project6;
    } else {
        end_project6 = "";
    }
    html += '<td><input id="end_project6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + end_project6 + '"></td>';
    var ket_project6;
    if (data["job_experience"].ket_project6) {
        ket_project6 = data["job_experience"].ket_project6;
    } else {
        ket_project6 = "";
    }
    html += '<td><input id="ket_project6' + data.id + '" type="text" class="input-sm form-control-sm form-control" value="' + ket_project6 + '"></td>';
    html += "</tr>";
    html += "</tbody>";
    html += "</table>";
    html += "</div>";
    html += "</div>";
    html += '<div class="modal-footer">';
    html += '<div class="items-link items-link2"><a onclick="editJob(' + data.id + ')" style="cursor: pointer;"><i class="fa fa-check-square"></i> Save</a></div>';
    html += '<div class="items-link items-link2"><a data-dismiss="modal" style="cursor: pointer;"><i class="fa fa-times"></i> Cancel</a></div>';
    html += "</div>";
    html += "</div>";
    html += '<div class="tab-pane fade" id="nav-file' + data.id + '" role="tabpanel" aria-labelledby="nav-file-tab">';
    html += '<div class="card-body card-block">';
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group" id="ppicture' + data.id + '">';
    html += '</div>';
    html += '</div>';
    html += '<div class="col-6">';
    html += '<div class="form-group" id="ktphoto' + data.id + '">';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '<div class="row">';
    html += '<div class="col-6">';
    html += '<div class="form-group" id="npwphoto' + data.id + '">';
    html += '</div>';
    html += '</div>';
    html += '<div class="col-6">';
    html += '<div class="form-group" id="photocv' + data.id + '">';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '<div class="modal-footer">';
    html += '<div class="items-link items-link2"><a onclick="editFile(' + data.id + ')" style="cursor: pointer;"><i class="fa fa-check-square"></i> Save</a></div>';
    html += '<div class="items-link items-link2"><a data-dismiss="modal" style="cursor: pointer;"><i class="fa fa-times"></i> Cancel</a></div>';
    html += '</div>';
    html += '</div>';
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";
    html += "</div>";

    return html;
}

function fillcity(object) {
    var city = "city";
    editid = $("#idsetting").val();
    province = $("#" + object.id).val();
    checkcorr = object.id.split("-");
    checkedit = object.id.substr(-1);
    if (checkcorr.length == 2) city = "corr-" + city;
    if (!isNaN(checkedit)) city += editid;
    $.ajax({
        type: "POST",
        url: "/api/V1.0/listalluser",
        async: true,
        crossDomain: true,
        data: {
            keyword: "city",
            cur_user: sessionStorage.getItem("cur_user"),
            token: sessionStorage.getItem("token"),
            province_id: province,
        },
        success: function (response) {
            $("#" + city).empty();
            $("#" + city).append(
                $("<option>", {
                    value: "0",
                    text: "Select City",
                })
            );
            $.each(response["data"], function (i, item) {
                $("#" + city).append(
                    $("<option>", {
                        value: item.id,
                        text: item.name,
                    })
                );
            });
        },
    });
}

function fillkec(object) {
    var kec = "kec";
    editid = $("#idsetting").val();
    province = $("#" + object.id).val();
    checkcorr = object.id.split("-");
    checkedit = object.id.substr(-1);
    if (checkcorr.length == 2) kec = "corr-" + kec;
    if (!isNaN(checkedit)) kec += editid;
    $.ajax({
        type: "POST",
        url: "/api/V1.0/listalluser",
        async: true,
        crossDomain: true,
        data: {
            keyword: "kecamatan",
            cur_user: sessionStorage.getItem("cur_user"),
            token: sessionStorage.getItem("token"),
            city_id: province,
        },
        success: function (response) {
            $("#" + kec).empty();
            $("#" + kec).append(
                $("<option>", {
                    value: "0",
                    text: "Select Kecamatan",
                })
            );
            $.each(response["data"], function (i, item) {
                $("#" + kec).append(
                    $("<option>", {
                        value: item.id,
                        text: item.name,
                    })
                );
            });
        },
    });
}

function fillkel(object) {
    var kel = "kel";
    editid = $("#idsetting").val();
    province = $("#" + object.id).val();
    checkcorr = object.id.split("-");
    checkedit = object.id.substr(-1);
    if (checkcorr.length == 2) kel = "corr-" + kel;
    if (!isNaN(checkedit)) kel += editid;
    $.ajax({
        type: "POST",
        url: "/api/V1.0/listalluser",
        async: true,
        crossDomain: true,
        data: {
            keyword: "kelurahan",
            cur_user: sessionStorage.getItem("cur_user"),
            token: sessionStorage.getItem("token"),
            kecamatan_id: province,
        },
        success: function (response) {
            $("#" + kel).empty();
            $("#" + kel).append(
                $("<option>", {
                    value: "0",
                    text: "Select Kelurahan",
                })
            );
            $.each(response["data"], function (i, item) {
                $("#" + kel).append(
                    $("<option>", {
                        value: item.id,
                        text: item.name,
                    })
                );
            });
        },
    });
}

function fillpostalcode(object) {
    var postal = "postalcode";
    editid = $("#idsetting").val();
    province = $("#" + object.id).val();
    checkcorr = object.id.split("-");
    checkedit = object.id.substr(-1);
    if (checkcorr.length == 2) postal = "corr-" + postal;
    if (!isNaN(checkedit)) postal += editid;
    $.ajax({
        type: "POST",
        url: "/api/V1.0/listalluser",
        async: true,
        crossDomain: true,
        data: {
            keyword: "postalcode",
            cur_user: sessionStorage.getItem("cur_user"),
            token: sessionStorage.getItem("token"),
            kecamatan_id: province,
        },
        success: function (response) {
            $("#" + postal).empty();
            $("#" + postal).append(
                $("<option>", {
                    value: "0",
                    text: "Select Postalcode",
                })
            );
            $.each(response["data"], function (i, item) {
                $("#" + postal).append(
                    $("<option>", {
                        value: item.id,
                        text: item.name,
                    })
                );
            });
        },
    });
}

function editEmp(i) {
    var form = new FormData();
    valid = false;
    form.append("client_id", "1");
    if ($("#name" + i).val() == "") {
        $("#name" + i).focus();
        alert("Name not filled in");
        valid = false;
    } else {
        name = $("#name" + i).val();
        form.append("name", name);
        valid = true;
    }
    if ($("#nik" + i).val() == "") {
        $("#nik" + i).focus();
        alert("NIK not filled in");
        valid = false;
    } else {
        nik = $("#nik" + i).val();
        form.append("nik", nik);
        valid = true;
    }
    if ($("#gender" + i).val() == "0") {
        $("#gender" + i).focus();
        alert("Gender not filled in");
        valid = false;
    } else {
        gender = $("#gender" + i).val();
        form.append("gender", gender);
        valid = true;
    }
    if ($("#religion" + i).val() == "0") {
        $("#religion" + i).focus();
        alert("Religion not filled in");
        valid = false;
    } else {
        religion = $("#religion" + i).val();
        form.append("religion", religion);
        valid = true;
    }
    if ($("#address" + i).val() == "") {
        $("#address" + i).focus();
        alert("Address not filled in");
        valid = false;
    } else {
        address = $("#address" + i).val();
        form.append("address", address);
        valid = true;
    }
    if ($("#province" + i).val() == "0") {
        $("#province" + i).focus();
        alert("Province not filled in");
        valid = false;
    } else {
        province = $("#province" + i).val();
        form.append("province", province);
        valid = true;
    }
    if ($("#city" + i).val() == "0") {
        $("#city" + i).focus();
        alert("City not filled in");
        valid = false;
    } else {
        city = $("#city" + i).val();
        form.append("city", city);
        valid = true;
    }
    if ($("#kec" + i).val() == "0") {
        $("#kec" + i).focus();
        alert("Kecamatan not filled in");
        valid = false;
    } else {
        kecamatan = $("#kec" + i).val();
        form.append("kecamatan", kecamatan);
        valid = true;
    }
    if ($("#kel" + i).val() == "0") {
        $("#kel" + i).focus();
        alert("Kelurahan not filled in");
        valid = false;
    } else {
        kelurahan = $("#kel" + i).val();
        form.append("kelurahan", kelurahan);
        valid = true;
    }
    if ($("#postalcode" + i).val() == "0") {
        $("#postalcode" + i).focus();
        alert("Postalcode not filled in");
        valid = false;
    } else {
        postalcode = $("#postalcode" + i).val();
        form.append("postalcode", postalcode);
        valid = true;
    }
    if ($("#rt" + i).val() == "") {
        $("#rt" + i).focus();
        alert("RT not filled in");
        valid = false;
    } else {
        rt = $("#rt" + i).val();
        form.append("rt", rt);
        valid = true;
    }
    if ($("#rw" + i).val() == "") {
        $("#rw" + i).focus();
        alert("RW not filled in");
        valid = false;
    } else {
        rw = $("#rw" + i).val();
        form.append("rw", rw);
        valid = true;
    }
    birthdate = $("#birthdate" + i).val();
    form.append("birthdate", birthdate);
    birthplace = $("#birthplace" + i).val();
    form.append("birthplace", birthplace);
    if ($("#phonenumber" + i).val() == "") {
        $("#phonenumber" + i).focus();
        alert("Phone number not filled in");
        valid = false;
    } else {
        phone = $("#phonenumber" + i).val();
        form.append("phonenumber", phone);
        valid = true;
    }
    if ($("#email" + i).val() == "") {
        $("#email" + i).focus();
        alert("Email not filled in");
        valid = false;
    } else {
        email = $("#email" + i).val();
        form.append("email", email);
        valid = true;
    }
    marital = $("#marital" + i).val();
    form.append("marital", marital);
    form.append("user_id", i);
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/insertuser",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    alert("Data Updated Successfully");
                    $("#user_setting" + i).modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                }
            },
        });
    }
}

function editCorres(i) {
    var form = new FormData();
    valid = false;
    id = $("#addid" + i).val();
    if ($("#corr-address" + i).val() == "") {
        $("#corr-address" + i).focus();
        alert("Correspondance Address not filled in");
        valid = false;
    } else {
        corraddress = $("#corr-address" + i).val();
        form.append("cor-address", corraddress);
        valid = true;
    }
    if ($("#statusaddress" + i).val() == "0") {
        $("#statusaddress" + i).focus();
        alert("Status Address not filled in");
        valid = false;
    } else {
        statusaddress = $("#statusaddress" + i).val();
        form.append("statusaddress", statusaddress);
        valid = true;
    }
    if ($("#corr-province" + i).val() == "0") {
        $("#corr-province" + i).focus();
        alert("Province not filled in");
        valid = false;
    } else {
        corrprovince = $("#corr-province" + i).val();
        form.append("cor-province", corrprovince);
        valid = true;
    }
    if ($("#corr-city" + i).val() == "0") {
        $("#corr-city" + i).focus();
        alert("City not filled in");
        valid = false;
    } else {
        corrcity = $("#corr-city" + i).val();
        form.append("cor-city", corrcity);
        valid = true;
    }
    if ($("#corr-kec" + i).val() == "0") {
        $("#corr-kec" + i).focus();
        alert("Kecamatan not filled in");
        valid = false;
    } else {
        corrkecamatan = $("#corr-kec" + i).val();
        form.append("cor-kecamatan", corrkecamatan);
        valid = true;
    }
    if ($("#corr-kel" + i).val() == "0") {
        $("#corr-kel" + i).focus();
        alert("Kelurahan not filled in");
        valid = false;
    } else {
        corrkelurahan = $("#corr-kel" + i).val();
        form.append("cor-kelurahan", corrkelurahan);
        valid = true;
    }
    if ($("#corr-postalcode" + i).val() == "0") {
        $("#corr-postalcode" + i).focus();
        alert("Postalcode not filled in");
        valid = false;
    } else {
        corrpostalcode = $("#corr-postalcode" + i).val();
        form.append("cor-postalcode", corrpostalcode);
        valid = true;
    }
    if ($("#corr-rt" + i).val() == "") {
        $("#corr-rt" + i).focus();
        alert("RT not filled in");
        valid = false;
    } else {
        corrrt = $("#corr-rt" + i).val();
        form.append("cor-rt", corrrt);
        valid = true;
    }
    if ($("#corr-rw" + i).val() == "") {
        $("#corr-rw" + i).focus();
        alert("RW not filled in");
        valid = false;
    } else {
        corrrw = $("#corr-rw" + i).val();
        form.append("cor-rw", corrrw);
        valid = true;
    }
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    form.append("user_id", i);
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/insert_user_corespon",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    alert("Data Updated Successfully");
                    $("#user_setting" + i).modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                }
            },
        });
    }
}

function editEdu(i) {
    var form = new FormData();
    valid = false;
    id = $("#addid" + i).val();
    if ($("#lastedu" + i).val() == "0") {
        $("#lastedu" + i).focus();
        alert("Last Education not filled in");
        valid = false;
    } else {
        lastedu = $("#lastedu" + i).val();
        form.append("lastedu", lastedu);
        valid = true;
    }
    form.append("level_education_id", lastedu);
    nama_sd = $("#nama_sd" + i).val();
    form.append("nama_sd", nama_sd);
    kota_sd = $("#kota_sd" + i).val();
    form.append("kota_sd", kota_sd);
    jurusan_sd = $("#jurusan_sd" + i).val();
    form.append("jurusan_sd", jurusan_sd);
    masuk_sd = $("#masuk_sd" + i).val();
    form.append("masuk_sd", masuk_sd);
    lulus_sd = $("#lulus_sd" + i).val();
    form.append("lulus_sd", lulus_sd);
    status_sd = $("#status_sd" + i).val();
    form.append("status_sd", status_sd);
    nama_smp = $("#nama_smp" + i).val();
    form.append("nama_smp", nama_smp);
    kota_smp = $("#kota_smp" + i).val();
    form.append("kota_smp", kota_smp);
    jurusan_smp = $("#jurusan_smp" + i).val();
    form.append("jurusan_smp", jurusan_smp);
    masuk_smp = $("#masuk_smp" + i).val();
    form.append("masuk_smp", masuk_smp);
    lulus_smp = $("#lulus_smp" + i).val();
    form.append("lulus_smp", lulus_smp);
    status_smp = $("#status_smp" + i).val();
    form.append("status_smp", status_smp);
    nama_sma = $("#nama_sma" + i).val();
    form.append("nama_sma", nama_sma);
    kota_sma = $("#kota_sma" + i).val();
    form.append("kota_sma", kota_sma);
    jurusan_sma = $("#jurusan_sma" + i).val();
    form.append("jurusan_sma", jurusan_sma);
    masuk_sma = $("#masuk_sma" + i).val();
    form.append("masuk_sma", masuk_sma);
    lulus_sma = $("#lulus_sma" + i).val();
    form.append("lulus_sma", lulus_sma);
    status_sma = $("#status_sma" + i).val();
    form.append("status_sma", status_sma);
    nama_s1 = $("#nama_s1" + i).val();
    form.append("nama_s1", nama_s1);
    kota_s1 = $("#kota_s1" + i).val();
    form.append("kota_s1", kota_s1);
    jurusan_s1 = $("#jurusan_s1" + i).val();
    form.append("jurusan_s1", jurusan_s1);
    masuk_s1 = $("#masuk_s1" + i).val();
    form.append("masuk_s1", masuk_s1);
    lulus_s1 = $("#lulus_s1" + i).val();
    form.append("lulus_s1", lulus_s1);
    status_s1 = $("#status_s1" + i).val();
    form.append("status_s1", status_s1);
    nama_s2 = $("#nama_s2" + i).val();
    form.append("nama_s2", nama_s2);
    kota_s2 = $("#kota_s2" + i).val();
    form.append("kota_s2", kota_s2);
    jurusan_s2 = $("#jurusan_s2" + i).val();
    form.append("jurusan_s2", jurusan_s2);
    masuk_s2 = $("#masuk_s2" + i).val();
    form.append("masuk_s2", masuk_s2);
    lulus_s2 = $("#lulus_s2" + i).val();
    form.append("lulus_s2", lulus_s2);
    status_s2 = $("#status_s2" + i).val();
    form.append("status_s2", status_s2);
    nama_s3 = $("#nama_s3" + i).val();
    form.append("nama_s3", nama_s3);
    kota_s3 = $("#kota_s3" + i).val();
    form.append("kota_s3", kota_s3);
    jurusan_s3 = $("#jurusan_s3" + i).val();
    form.append("jurusan_s3", jurusan_s3);
    masuk_s3 = $("#masuk_s3" + i).val();
    form.append("masuk_s3", masuk_s3);
    lulus_s3 = $("#lulus_s3" + i).val();
    form.append("lulus_s3", lulus_s3);
    status_s3 = $("#status_s3" + i).val();
    form.append("status_s3", status_s3);
    bidang1 = $("#bidang1" + i).val();
    form.append("bidang1", bidang1);
    penyelenggara1 = $("#penyelenggara1" + i).val();
    form.append("penyelenggara1", penyelenggara1);
    kota_kursus1 = $("#kota_kursus1" + i).val();
    form.append("kota_kursus1", kota_kursus1);
    lama_kursus1 = $("#lama_kursus1" + i).val();
    form.append("lama_kursus1", lama_kursus1);
    tahun_masuk1 = $("#tahun_masuk1" + i).val();
    form.append("tahun_masuk1", tahun_masuk1);
    biaya1 = $("#biaya1" + i).val();
    form.append("biaya1", biaya1);
    bidang2 = $("#bidang2" + i).val();
    form.append("bidang2", bidang2);
    penyelenggara2 = $("#penyelenggara2" + i).val();
    form.append("penyelenggara2", penyelenggara2);
    kota_kursus2 = $("#kota_kursus2" + i).val();
    form.append("kota_kursus2", kota_kursus2);
    lama_kursus2 = $("#lama_kursus2" + i).val();
    form.append("lama_kursus2", lama_kursus2);
    tahun_masuk2 = $("#tahun_masuk2" + i).val();
    form.append("tahun_masuk2", tahun_masuk2);
    biaya2 = $("#biaya2" + i).val();
    form.append("biaya2", biaya2);
    bidang3 = $("#bidang3" + i).val();
    form.append("bidang3", bidang3);
    penyelenggara3 = $("#penyelenggara3" + i).val();
    form.append("penyelenggara3", penyelenggara3);
    kota_kursus3 = $("#kota_kursus3" + i).val();
    form.append("kota_kursus3", kota_kursus3);
    lama_kursus3 = $("#lama_kursus3" + i).val();
    form.append("lama_kursus3", lama_kursus3);
    tahun_masuk3 = $("#tahun_masuk3" + i).val();
    form.append("tahun_masuk3", tahun_masuk3);
    biaya3 = $("#biaya3" + i).val();
    form.append("biaya3", biaya3);
    bidang4 = $("#bidang4" + i).val();
    form.append("bidang4", bidang4);
    penyelenggara4 = $("#penyelenggara4" + i).val();
    form.append("penyelenggara4", penyelenggara4);
    kota_kursus4 = $("#kota_kursus4" + i).val();
    form.append("kota_kursus4", kota_kursus4);
    lama_kursus4 = $("#lama_kursus4" + i).val();
    form.append("lama_kursus4", lama_kursus4);
    tahun_masuk4 = $("#tahun_masuk4" + i).val();
    form.append("tahun_masuk4", tahun_masuk4);
    biaya4 = $("#biaya4" + i).val();
    form.append("biaya4", biaya4);
    bidang5 = $("#bidang5" + i).val();
    form.append("bidang5", bidang5);
    penyelenggara5 = $("#penyelenggara5" + i).val();
    form.append("penyelenggara5", penyelenggara5);
    kota_kursus5 = $("#kota_kursus5" + i).val();
    form.append("kota_kursus5", kota_kursus5);
    lama_kursus5 = $("#lama_kursus5" + i).val();
    form.append("lama_kursus5", lama_kursus5);
    tahun_masuk5 = $("#tahun_masuk5" + i).val();
    form.append("tahun_masuk5", tahun_masuk5);
    biaya5 = $("#biaya5" + i).val();
    form.append("biaya5", biaya5);
    bidang6 = $("#bidang6" + i).val();
    form.append("bidang6", bidang6);
    penyelenggara6 = $("#penyelenggara6" + i).val();
    form.append("penyelenggara6", penyelenggara6);
    kota_kursus6 = $("#kota_kursus6" + i).val();
    form.append("kota_kursus6", kota_kursus6);
    lama_kursus6 = $("#lama_kursus6" + i).val();
    form.append("lama_kursus6", lama_kursus6);
    tahun_masuk6 = $("#tahun_masuk6" + i).val();
    form.append("tahun_masuk6", tahun_masuk6);
    biaya6 = $("#biaya6" + i).val();
    form.append("biaya6", biaya6);
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    form.append("user_id", i);
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/insert_user_education",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    alert("Data Updated Successfully");
                    $("#user_setting" + i).modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                }
            },
        });
    }
}

function editJob(i) {
    var form = new FormData();
    valid = true;
    id = $("#addid" + i).val();
    npwp = $("#npwp" + i).val();
    form.append("npwp", npwp);
    bpjstk = $("#bpjstk" + i).val();
    form.append("bpjstk", bpjstk);
    bpjs = $("#bpjs" + i).val();
    form.append("bpjs", bpjs);
    aap1 = $("#aap1" + i).val();
    form.append("aap1", aap1);
    klasifikasi1 = $("#klasifikasi1" + i).val();
    form.append("klasifikasi1", klasifikasi1);
    ska1 = $("#ska1" + i).val();
    form.append("ska1", ska1);
    skastart1 = $("#skastart1" + i).val();
    form.append("skastart1", skastart1);
    skaend1 = $("#skaend1" + i).val();
    form.append("skaend1", skaend1);
    aap2 = $("#aap2" + i).val();
    form.append("aap2", aap2);
    klasifikasi2 = $("#klasifikasi2" + i).val();
    form.append("klasifikasi2", klasifikasi2);
    ska2 = $("#ska2" + i).val();
    form.append("ska2", ska2);
    skastart2 = $("#skastart2" + i).val();
    form.append("skastart2", skastart2);
    skaend2 = $("#skaend2" + i).val();
    form.append("skaend2", skaend2);
    aap3 = $("#aap3" + i).val();
    form.append("aap3", aap3);
    klasifikasi3 = $("#klasifikasi3" + i).val();
    form.append("klasifikasi3", klasifikasi3);
    ska3 = $("#ska3" + i).val();
    form.append("ska3", ska3);
    skastart3 = $("#skastart3" + i).val();
    form.append("skastart3", skastart3);
    skaend3 = $("#skaend3" + i).val();
    form.append("skaend3", skaend3);
    aap4 = $("#aap4" + i).val();
    form.append("aap4", aap4);
    klasifikasi4 = $("#klasifikasi4" + i).val();
    form.append("klasifikasi4", klasifikasi4);
    ska4 = $("#ska4" + i).val();
    form.append("ska4", ska4);
    skastart4 = $("#skastart4" + i).val();
    form.append("skastart4", skastart4);
    skaend4 = $("#skaend4" + i).val();
    form.append("skaend4", skaend4);
    aap5 = $("#aap5" + i).val();
    form.append("aap5", aap5);
    klasifikasi5 = $("#klasifikasi5" + i).val();
    form.append("klasifikasi5", klasifikasi5);
    ska5 = $("#ska5" + i).val();
    form.append("ska5", ska5);
    skastart5 = $("#skastart5" + i).val();
    form.append("skastart5", skastart5);
    skaend5 = $("#skaend5" + i).val();
    form.append("skaend5", skaend5);
    company1 = $("#company1" + i).val();
    form.append("company1", company1);
    comaddress1 = $("#comaddress1" + i).val();
    form.append("comaddress1", comaddress1);
    work_position1 = $("#work_position1" + i).val();
    form.append("work_position1", work_position1);
    starttime1 = $("#starttime1" + i).val();
    form.append("starttime1", starttime1);
    endtime1 = $("#endtime1" + i).val();
    form.append("endtime1", endtime1);
    ket1 = $("#ket1" + i).val();
    form.append("ket1", ket1);
    project1 = $("#project1" + i).val();
    form.append("project1", project1);
    project_address1 = $("#project_address1" + i).val();
    form.append("project_address1", project_address1);
    project_position1 = $("#project_position1" + i).val();
    form.append("project_position1", project_position1);
    start_project1 = $("#start_project1" + i).val();
    form.append("start_project1", start_project1);
    end_project1 = $("#end_project1" + i).val();
    form.append("end_project1", end_project1);
    ket_project1 = $("#ket_project1" + i).val();
    form.append("ket_project1", ket_project1);
    company2 = $("#company2" + i).val();
    form.append("company2", company2);
    comaddress2 = $("#comaddress2" + i).val();
    form.append("comaddress2", comaddress2);
    work_position2 = $("#work_position2" + i).val();
    form.append("work_position2", work_position2);
    starttime2 = $("#starttime2" + i).val();
    form.append("starttime2", starttime2);
    endtime2 = $("#endtime2" + i).val();
    form.append("endtime2", endtime2);
    ket2 = $("#ket2" + i).val();
    form.append("ket2", ket2);
    project2 = $("#project2" + i).val();
    form.append("project2", project2);
    project_address2 = $("#project_address2" + i).val();
    form.append("project_address2", project_address2);
    project_position2 = $("#project_position2" + i).val();
    form.append("project_position2", project_position2);
    start_project2 = $("#start_project2" + i).val();
    form.append("start_project2", start_project2);
    end_project2 = $("#end_project2" + i).val();
    form.append("end_project2", end_project2);
    ket_project2 = $("#ket_project2" + i).val();
    form.append("ket_project2", ket_project2);
    company3 = $("#company3" + i).val();
    form.append("company3", company3);
    comaddress3 = $("#comaddress3" + i).val();
    form.append("comaddress3", comaddress3);
    work_position3 = $("#work_position3" + i).val();
    form.append("work_position3", work_position3);
    starttime3 = $("#starttime3" + i).val();
    form.append("starttime3", starttime3);
    endtime3 = $("#endtime3" + i).val();
    form.append("endtime3", endtime3);
    ket3 = $("#ket3" + i).val();
    form.append("ket3", ket3);
    project3 = $("#project3" + i).val();
    form.append("project3", project3);
    project_address3 = $("#project_address3" + i).val();
    form.append("project_address3", project_address3);
    project_position3 = $("#project_position3" + i).val();
    form.append("project_position3", project_position3);
    start_project3 = $("#start_project3" + i).val();
    form.append("start_project3", start_project3);
    end_project3 = $("#end_project3" + i).val();
    form.append("end_project3", end_project3);
    ket_project3 = $("#ket_project3" + i).val();
    form.append("ket_project3", ket_project3);
    company4 = $("#company4" + i).val();
    form.append("company4", company4);
    comaddress4 = $("#comaddress4" + i).val();
    form.append("comaddress4", comaddress4);
    work_position4 = $("#work_position4" + i).val();
    form.append("work_position4", work_position4);
    starttime4 = $("#starttime4" + i).val();
    form.append("starttime4", starttime4);
    endtime4 = $("#endtime4" + i).val();
    form.append("endtime4", endtime4);
    ket4 = $("#ket4" + i).val();
    form.append("ket4", ket4);
    project4 = $("#project4" + i).val();
    form.append("project4", project4);
    project_address4 = $("#project_address4" + i).val();
    form.append("project_address4", project_address4);
    project_position4 = $("#project_position4" + i).val();
    form.append("project_position4", project_position4);
    start_project4 = $("#start_project4" + i).val();
    form.append("start_project4", start_project4);
    end_project4 = $("#end_project4" + i).val();
    form.append("end_project4", end_project4);
    ket_project4 = $("#ket_project4" + i).val();
    form.append("ket_project4", ket_project4);
    company5 = $("#company5" + i).val();
    form.append("company5", company5);
    comaddress5 = $("#comaddress5" + i).val();
    form.append("comaddress5", comaddress5);
    work_position5 = $("#work_position5" + i).val();
    form.append("work_position5", work_position5);
    starttime5 = $("#starttime5" + i).val();
    form.append("starttime5", starttime5);
    endtime5 = $("#endtime5" + i).val();
    form.append("endtime5", endtime5);
    ket5 = $("#ket5" + i).val();
    form.append("ket5", ket5);
    project5 = $("#project5" + i).val();
    form.append("project5", project5);
    project_address5 = $("#project_address5" + i).val();
    form.append("project_address5", project_address5);
    project_position5 = $("#project_position5" + i).val();
    form.append("project_position5", project_position5);
    start_project5 = $("#start_project5" + i).val();
    form.append("start_project5", start_project5);
    end_project5 = $("#end_project5" + i).val();
    form.append("end_project5", end_project5);
    ket_project5 = $("#ket_project5" + i).val();
    form.append("ket_project5", ket_project5);
    company6 = $("#company6" + i).val();
    form.append("company6", company6);
    comaddress6 = $("#comaddress6" + i).val();
    form.append("comaddress6", comaddress6);
    work_position6 = $("#work_position6" + i).val();
    form.append("work_position6", work_position6);
    starttime6 = $("#starttime6" + i).val();
    form.append("starttime6", starttime6);
    endtime6 = $("#endtime6" + i).val();
    form.append("endtime6", endtime6);
    ket6 = $("#ket6" + i).val();
    form.append("ket6", ket6);
    project6 = $("#project6" + i).val();
    form.append("project6", project6);
    project_address6 = $("#project_address6" + i).val();
    form.append("project_address6", project_address6);
    project_position6 = $("#project_position6" + i).val();
    form.append("project_position6", project_position6);
    start_project6 = $("#start_project6" + i).val();
    form.append("start_project6", start_project6);
    end_project6 = $("#end_project6" + i).val();
    form.append("end_project6", end_project6);
    ket_project6 = $("#ket_project6" + i).val();
    form.append("ket_project6", ket_project6);
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    form.append("user_id", i);
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/insert_user_job",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    alert("Data Updated Successfully");
                    $("#user_setting" + i).modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                }
            },
        });
    }
}

function editFile(i) {
    var form = new FormData();
    valid = true;
    profile = $("#profile" + i).val();
    var pictureInput = document.getElementById("profile" + i).files[0];
    form.append("imgfile", pictureInput);
    fotoktp = $("#fotoktp" + i).val();
    var pictureInput = document.getElementById("fotoktp" + i).files[0];
    form.append("fotoktp", pictureInput);
    fotonpwp = $("#fotonpwp" + i).val();
    var pictureInput = document.getElementById("fotonpwp" + i).files[0];
    form.append("fotonpwp", pictureInput);
    imgcv = $("#cv" + i).val();
    var pictureInput = document.getElementById("cv" + i).files[0];
    form.append("imgcv", pictureInput);
    picid = $("#picid" + i).val();
    form.append("pic_id", picid);
    cvid = $("#cvid" + i).val();
    form.append("cv_id", cvid);
    ktpid = $("#ktpid" + i).val();
    form.append("ktp_id", ktpid);
    npwpid = $("#npwpid" + i).val();
    form.append("npwp_id", npwpid);
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    form.append("user_id", i);
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/insert_user_file",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    alert("Data Updated Successfully");
                    $("#user_setting" + i).modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                }
            },
        });
    }
}

function getcv(cvid, id) {
    $.ajax({
        type: "POST",
        url: "/user_uploads",
        async: true,
        crossDomain: true,
        data: {
            cur_user: sessionStorage.getItem("cur_user"),
            token: sessionStorage.getItem("token"),
            cv: cvid,
            id: id,
        },
        success: function (response) {
            var objbuilder = "";
            objbuilder += '<object width="100%" height="100%" data="data:application/pdf;base64,';
            objbuilder += response;
            objbuilder += '" type="application/pdf" class="internal">';
            objbuilder += '<embed src="data:application/pdf;base64,';
            objbuilder += response;
            objbuilder += '" type="application/pdf"  />';
            objbuilder += "</object>";

            var win = window.open("#", "_blank");
            var title = "CV";
            win.document.write("<html><title>" + title + '</title><body style="margin-top: 0px; margin-left: 0px; margin-right: 0px; margin-bottom: 0px;">');
            win.document.write(objbuilder);
            win.document.write("</body></html>");
            layer = jQuery(win.document);
        },
    });
}

function fillattachment(data) {
    var form = new FormData();
    form.append("file_id", data.profile_picture.id);
    form.append("token", sessionStorage.getItem("token"));
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    $.ajax({
        async: true,
        crossDomain: true,
        url: "/user_images/" + data.profile_picture.name,
        method: "POST",
        processData: false,
        contentType: false,
        datatype: "JSON",
        mimeType: "multipart/form-data",
        data: form,
        success: function (response) {
            $("#ppicture" + data.id).html(
                '<label for="images" class="control-label mb-1">Foto Profil</label><br/><img src="data:image/jpeg;base64,' +
                    response + '" style="width: 213px; height: 213px;"/><input type="file" name="profile" id="profile' +
                    data.id + '" class="form-control"/><input type="hidden" id="picid' + data.id + '" value="' + data.profile_picture.id + '"><p class="small">Max upload file: 2MB</p>'
            );
        },
    });

    var form = new FormData();
    form.append("file_id", data.fotoktp.id);
    form.append("token", sessionStorage.getItem("token"));
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    $.ajax({
        async: true,
        crossDomain: true,
        url: "/user_images/" + data.fotoktp.name,
        method: "POST",
        processData: false,
        contentType: false,
        datatype: "JSON",
        mimeType: "multipart/form-data",
        data: form,
        success: function (response) {
            $("#ktphoto" + data.id).html(
                '<label for="images" class="control-label mb-1">KTP</label><br/><img src="data:image/jpeg;base64,' +
                    response + '" style="width: 213px; height: 213px;"/><input type="file" name="fotoktp" id="fotoktp' +
                    data.id + '" class="form-control"/><input type="hidden" id="ktpid' + data.id + '" value="' +
                    data.fotoktp.id + '"><p class="small">Max upload file: 2MB</p>'
            );
        },
    });

    var form = new FormData();
    form.append("file_id", data.fotonpwp.id);
    form.append("token", sessionStorage.getItem("token"));
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    $.ajax({
        async: true,
        crossDomain: true,
        url: "/user_images/" + data.fotonpwp.name,
        method: "POST",
        processData: false,
        contentType: false,
        datatype: "JSON",
        mimeType: "multipart/form-data",
        data: form,
        success: function (response) {
            $("#npwphoto" + data.id).html(
                '<label for="images" class="control-label mb-1">NPWP</label><br/><img src="data:image/jpeg;base64,' +
                    response + '" style="width: 213px; height: 213px;"/><input type="file" name="fotonpwp" id="fotonpwp' +
                    data.id + '" class="form-control"/><input type="hidden" id="npwpid' + data.id + '" value="' +
                    data.fotonpwp.id + '"><p class="small">Max upload file: 2MB</p>'
            );
        },
    });

    if (data.cv.id) {
        $("#photocv" + data.id).html(
            '<label class="control-label mb-1">Curriculum Vitae</label><input type="file" name="cv" id="cv' + data.id + '" class="form-control"/><a href="javascript:getcv(' + data.cv.id + "," + data.id + ');" >' + data.cv.name +
                '</a><input type="hidden" id="cvid' + data.id + '" value="' + data.cv.id + '"><p class="small">Jenis file: PDF, DOC, DOCX. Max: 5MB</p>'
        );
    } else {
        $("#photocv" + data.id).html('<label class="control-label mb-1">Curriculum Vitae</label><br/><input type="file" name="cv" id="cv' + data.id + '" class="form-control"/>');
    }
}