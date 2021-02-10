function createmodallogin() {
    var html = '<div class="modal fade" id="login" tabindex="-1" role="dialog" aria-hidden="true">';
            html += '<div class="modal-dialog modal-md" role="document">';
                html += '<div class="modal-content">';
                    html += '<div class="modal-header">';
                        html += '<h5 class="modal-title">Login</h5>';
                        html += '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
                            html += '<span aria-hidden="true">&times;</span>';
                        html += "</button>";
                    html += "</div>";
                        html += '<div class="col-lg-12">';
                            html += '<div class="row" style="margin: 30px;">';
                                html += '<div class="col-lg-6">';
                                        html += '<input type="email" class="form-control form-control-lg" id="email" placeholder="Email">';
                                html += "</div>";
                                html += '<div class="col-lg-6">';
                                        html += '<input type="password" class="form-control form-control-lg" id="password" placeholder="Password">';
                                html += "</div>";
                            html += "</div>";
                            html += '<div class="row" style="padding: 0 10em;">';
                                html += '<div class="col-md-12">';
                                    html += '<div class="items-link items-link2"><a onclick="login()" style="cursor: pointer;"><i class="fas fa-key"></i> Login</a></div>';
                                html += "</div>";
                            html += "</div>";
                        html += "</div>";
                    html += "<div>";
                        html += '<div class="modal-footer" style="display: block !important; text-align: center">';
                            // html += '<a href="" style="color: steelblue">Forgot Your Password?</a>';
                            html += '<p>Dont have an account? <a onclick="modalRegister();" style="color: steelblue; cursor: pointer;">Sign-up</a></p>';
                        html += "</div>";
                    html += "</div>";
                html += "</div>";
            html += "</div>";
        html += "</div>";

    return html;
}

function modalLogin() {
    $("#login").modal("show");
}

function modalRegister() {
    $("#register_user").modal("show");
    $("#login").modal("hide");
}

var attempt = 3;
function login(){
    form = new FormData();
    email = $("#email").val();
    password = $("#password").val();
    if (email == "" && password == "") {
        alert("Please Enter Your Email and Password");
    } else {
        form.append("email", email);
        form.append("password", password);
        $.ajax({
            type : 'POST',
            url : "/api/V1.0/loginuser",
            processData: false,
            contentType: false,
            data: form,
            success : function(response){
                if( response['status'] == '200' ){
                    client = response['client'];
                    email = response['email'];
                    name = response['name'];
                    cur_user = response['cur_user'];
                    token = response['token'];
                    list_access = response['list_access'];
                    response = response['response'];
                    sessionStorage.setItem("client", client);
                    sessionStorage.setItem("name", name);
                    sessionStorage.setItem("email", email);
                    sessionStorage.setItem("cur_user", cur_user);
                    sessionStorage.setItem("token", token);
                    sessionStorage.setItem("list_access", JSON.stringify(list_access.data[0]));
                    sessionStorage.setItem("response", response);
                    alert("Login Success");
                    $("#login").modal("hide");
                    reloaddata();
                    return false;
                }
                else {
                    attempt --;
                    alert("You have left "+attempt+" attempt;");
                    if( attempt == 0) {
                        document.getElementById("email").disabled = true;
                        document.getElementById("password").disabled = true;
                        document.getElementById("btn_login").disabled = true;
                        return false;
                    }
                }
            }
        });
    }
};

function registeruser(){
    var form = new FormData();
    valid = false;
    if ($("#reg-name").val() == "") {
        $("#reg-name").focus();
        alert("Name not filled");
        valid = false;
    } else {
        name = $("#reg-name").val();
        form.append("name", name);
        valid = true;
    }
    if ($("#reg-phonenumber").val() == "") {
        $("#reg-phonenumber").focus();
        alert("Phone Number not filled");
        valid = false;
    } else {
        phonenumber = $("#reg-phonenumber").val();
        form.append("phonenumber", phonenumber);
        valid = true;
    }
    if ($("#reg-password").val() == "") {
        $("#reg-password").focus();
        alert("Password not filled");
        valid = false;
    } else {
        password = $("#reg-password").val();
        form.append("password", password);
        valid = true;
    }    
    if ($("#reg-email").val() == "") {
        $("#reg-email").focus();
        alert("Email not filled");
        valid = false;
    } else {
        email = $("#reg-email").val();
        form.append("email", email);
        valid = true;
    }
    if ($("#reg-gender").val() == "0") {
        $("#reg-gender").focus();
        alert("Gender not filled");
        valid = false;
    } else {
        gender = $("#reg-gender").val();
        form.append("gender", gender);
        valid = true;
    }
    if ($("#reg-religion").val() == "0") {
        $("#reg-religion").focus();
        alert("Religion not filled");
        valid = false;
    } else {
        religion = $("#reg-religion").val();
        form.append("religion", religion);
        valid = true;
    }
    form.append("client_id", "1");
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/registeruser",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    alert("Create New Account is Success");
                    $("#register_user").modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                }
            },
        });
    }
}

function createmodalregister() {
    var html = '<div class="modal fade" id="register_user" tabindex="-1" role="dialog" aria-hidden="true">';
            html += '<div class="modal-dialog modal-md" role="document">';
                html += '<div class="modal-content">';
                    html += '<div class="modal-header">';
                        html += '<h5 class="modal-title">Create A New Account</h5>';
                        html += '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
                            html += '<span aria-hidden="true">&times;</span>';
                        html += "</button>";
                    html += "</div>";
                    html += '<form name="register" method="POST">';
                        html += '<div class="col-lg-12">';
                            html += '<div class="col-lg-12" style="padding-bottom: 15px; padding-top: 15px;">';
                                html += '<input type="text" class="form-control" id="reg-name" placeholder="Name">';
                            html += "</div>";
                            html += '<div class="col-lg-12" style="padding-bottom: 15px;">';
                                html += '<input type="email" class="form-control" id="reg-email" placeholder="Email">';
                            html += "</div>";
                            html += '<div class="col-lg-12" style="padding-bottom: 15px;">';
                                html += '<input class="form-control" id="reg-phonenumber" placeholder="Phone Number">';
                            html += "</div>";
                            html += '<div class="col-12" style="padding-bottom: 15px;">';
                                html += '<select id="reg-gender" class="form-control">';
                                    html += '<option value="0">Select Gender</option>';
                                    html += '<option value="1">Male</option>';
                                    html += '<option value="2">Female</option>';
                                html += "</select>";
                            html += "</div>";
                            html += '<div class="col-12" style="padding-bottom: 15px;">';
                                html += '<select id="reg-religion" class="form-control">';
                                    html += '<option value="0">Select Religion</option>';
                                    html += '<option value="1">Islam</option>';
                                    html += '<option value="2">Christian</option>';
                                    html += '<option value="3">Catholic</option>';
                                    html += '<option value="4">Hindu</option>';
                                    html += '<option value="5">Buddha</option>';
                                html += "</select>";
                            html += "</div>";
                            html += '<div class="col-lg-12" style="padding-bottom: 15px;">';
                                html += '<input type="password" class="form-control" id="reg-password" placeholder="Password">';
                            html += "</div>";
                            html += '<div class="row" style="padding: 0 8em;">';
                                html += '<div class="col-md-12">';
                                    html += '<div class="items-link items-link2"><a onclick="registeruser()" style="cursor: pointer;"><i class="fa fa-user-plus"></i> Sign Up</a></div>';
                                html += "</div>";
                            html += "</div>";
                        html += "</div>";
                    html += '</form>';
                html += "</div>";
            html += "</div>";
        html += "</div>";

    return html;
}