var detail = {
    async: true,
    crossDomain: true,
    url: "/api/V1.0/jobdetail",
    method: "POST"
};

function reloaddata() {
    $.ajax(detail).done(function (response) {
        
    });
}