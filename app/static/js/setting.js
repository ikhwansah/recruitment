$('<div class="row"><div class="col-lg-12"><h4>Settings</h4><br/><div class="row"><div class="col-6"><div class="form-group"><label class="control-label mb-1">Name</label><input id="name' + sessionStorage.cur_user + '" type="text" class="form-control" value="'+ sessionStorage.name +'"></div></div><div class="col-6"><div class="form-group"><label class="control-label mb-1">NIK(KTP)</label><input id="nik' + sessionStorage.cur_user + '" type="text" class="form-control" value="'+ sessionStorage.nik +'"></div></div></div><div class="row"><div class="col-6"><div class="form-group"><label class="control-label mb-1">Phone Number</label><input id="phonenumber' + sessionStorage.cur_user + '" type="text" class="form-control" value="'+ sessionStorage.phone +'" disabled></div></div><div class="col-6"><div class="form-group"><label class="control-label mb-1">Email</label><input type="email" id="email' + sessionStorage.cur_user + '" class="form-control" value="'+ sessionStorage.email +'" disabled></div></div></div><div class="footer"><button onclick="editAccount('+ sessionStorage.cur_user +')" id="submit-button" class="btn btn-info"><i class="fa fa-check-square"></i><span> Save</span></button></div> </div></div>').appendTo($('.container-fluid1')[0]);

function editAccount(i) {
    var form = new FormData();
    valid = false;
    form.append("client_id", "1");
    if ($("#name" + i).val() == "") {
        $("#name" + i).focus();
        alert("Name not filled");
        valid = false;
    } else {
        name = $("#name" + i).val();
        form.append("name", name);
        valid = true;
    }
    if ($("#nik" + i).val() == "") {
        $("#nik" + i).focus();
        alert("NIK not filled");
        valid = false;
    } else {
        nik = $("#nik" + i).val();
        form.append("nik", nik);
        valid = true;
    }
    if ($("#phonenumber" + i).val() == "") {
        $("#phonenumber" + i).focus();
        alert("Phone Number not filled");
        valid = false;
    } else {
        phone = $("#phonenumber" + i).val();
        form.append("phonenumber", phone);
        valid = true;
    }
    if ($("#email" + i).val() == "") {
        $("#email" + i).focus();
        alert("Email not filled");
        valid = false;
    } else {
        email = $("#email" + i).val();
        form.append("email", email);
        valid = true;
    }
    form.append("user_id", i);
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/insertaccount",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    alert("Edit Info Personal Berhasil!");
                }
            },
        });
    }
}