function logout_user() {
    sessionStorage.removeItem("client");
    sessionStorage.removeItem("cur_user");
    sessionStorage.removeItem("list_access");
    sessionStorage.removeItem("response");
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("name");
    sessionStorage.removeItem("email");
    alert("Logout Success");
    reloaddata();
}