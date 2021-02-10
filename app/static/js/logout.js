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