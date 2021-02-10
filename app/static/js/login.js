var attempt = 3;

function validate(){
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
            url : "/api/V1.0/login",
            processData: false,
            contentType: false,
            data: form,
            success : function(response){
                if( response['status'] == '200' ){
                    window.location = "dashboard";
                    client = response['client'];
                    email = response['email'];
                    name = response['name'];
                    nik = response['nik'];
                    phone = response['phone'];
                    cur_user = response['cur_user'];
                    token = response['token'];
                    password = response['password'];
                    list_access = response['list_access'];
                    response = response['response'];
                    sessionStorage.setItem("client", client);
                    sessionStorage.setItem("name", name);
                    sessionStorage.setItem("nik", nik);
                    sessionStorage.setItem("email", email);
                    sessionStorage.setItem("phone", phone);
                    sessionStorage.setItem("cur_user", cur_user);
                    sessionStorage.setItem("token", token);
                    sessionStorage.setItem("password", password);
                    sessionStorage.setItem("list_access", JSON.stringify(list_access.data[0]));
                    sessionStorage.setItem("response", response);
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