$('<div class="row"><div class="col-lg-12"><h4>Change Password</h4><br/><div class="row"><div class="col-6"><div class="form-group"><label class="control-label mb-1">New Password:</label><input type="password" id="changePass' + sessionStorage.cur_user + '" class="form-control"></div><input type="checkbox" onclick="showPass()"> Show Password</div></div><div class="footer"><button onclick="changePassBtnClick(' + sessionStorage.cur_user + ')" id="submit-button" class="btn btn-info"><i class="fa fa-check-square"></i><span> Save</span></button><button type="button" class="btn btn-secondary" onclick="back()"><i class="fa fa-times"></i><span> Cancel</span></button></div> </div></div>').appendTo($('.container-fluid1')[0]);

function logout() {    
    window.location = "logout";
    sessionStorage.removeItem("password");
    sessionStorage.removeItem("client");
    sessionStorage.removeItem("cur_user");
    sessionStorage.removeItem("list_access");
    sessionStorage.removeItem("response");
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("name");
    sessionStorage.removeItem("email");
    sessionStorage.removeItem("nik");
    sessionStorage.removeItem("phone");
}

function back(){
    window.location = "dashboard";
}

function changePassBtnClick(i){
 	var form = new FormData();
    valid = false;
    if ($("#changePass" + i).val() == "") {
        $("#changePass" + i).focus();
        alert("Password not filled in");
        valid = false;
    } else {
        password = $("#changePass" + i).val();
        form.append("password_hash", password);
        valid = true;
    }
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
    form.append("user_id", i);
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/updatepassword",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    alert("Changes Password Success!");
                    logout();
                }
            },
        });
    }
}

function showPass() {
  var x = document.getElementById("changePass" + sessionStorage.cur_user);
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}