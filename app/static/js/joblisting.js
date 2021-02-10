var listing = {
    async: true,
    crossDomain: true,
    url: "/api/V1.0/joblisting",
    method: "POST"
};

function datalisting() {
    $('.btn.head-btn1').remove();
    $('.btn.head-btn2').remove();
    $('#navigation.account').remove();
    $.ajax(listing).done(function (response) {
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
                    $('.header-btn.d-none.f-right.d-lg-block').append('<ul id="navigation" class="account"><li><a href="#">Hello, '+ sessionStorage.name +'</a><ul class="submenu"><li><a href="#"><i class="fa fa-info-circle"></i>  Account Info</a></li><li><a onclick="logout_user();" style="cursor: pointer;"><i class="fa fa-unlock-alt"></i>  Logout</a></li></ul></li></ul>');
                }else{
                    $('.header-btn.d-none.f-right.d-lg-block').append('<a onclick="modalRegister();" class="btn head-btn1" style="color: #fff; cursor: pointer;">Register</a><a onclick="modalLogin();" class="btn head-btn2" style="cursor: pointer;">Login</a>');
                }
            }
        });

        $("body").append(createmodallogin());
        $("body").append(createmodalregister());
        data = response["joblisting"]["data"];
        // console.log(data[0].jobtype_id.name);
        $('#list').pagination({
          dataSource: data,
          pageSize: 5,
          callback: function(data, pagination) {
              var wrapper = $('#list .wrapper').empty();
              var currentdate = new Date();
                $.each(data, function (i, item) {
                    if(Date.parse(currentdate) < Date.parse(item.applicationdate)){
                        $('#list .wrapper').append('<div class="single-job-items mb-30 cd-item '+item.jobtype_id.name+' '+item.experience_id.name+'"><div class="job-items"><div class="job-tittle job-tittle2" id="'+item.id+'"><a onclick="modalDetail('+item.id +');" style="cursor: pointer;"><h4>'+item.jobposition+'</h4></a><ul><li>'+item.division_id.name+'</li><li><i class="fas fa-map-marker-alt"></i>'+item.branch_id.name+'</li><li>'+item.salary+'</li></ul></div></div><div class="items-link items-link2 f-right"><a onclick="modalDetail('+item.id +');" style="cursor: pointer;">'+item.jobtype_id.name+'</a></div></div>');
                    }else{
                        $('#list .wrapper').append('');
                    }
                });
          }
        });

        type = response["jobtype"]["data"];
        $.each(type, function(i, item) {
        $('<label class="container">'+item.name+'<input type="checkbox" data-filter="'+item.name+'" class="filter_jobtype"><span class="checkmark"></span></label>').appendTo('div.select-Categories.pt-10.pb-50')
        });

        experiences = response["experience"]["data"];
        $.each(experiences, function(i, item) {
            $('<label class="container">'+item.name+'<input type="checkbox" data-filter="'+item.name+'" class="filter_experience"><span class="checkmark"></span></label>').appendTo('div.select-Categories.pt-10.pb-40')
        });

        // filter jobtype
        var $mediaElements = $(".cd-item");
        $(".filter_jobtype").click(function(e) {
          e.preventDefault();
          var filterVal = $(this).data("filter");
          if (filterVal === "all") {
            $mediaElements.slideDown("slow");
          } else {
            $mediaElements
              .hide("slow")
              .filter("." + filterVal)
              .slideDown("slow");
          }
        });

        //filter jobexperience
        var $mediaElements = $(".cd-item");
        $(".filter_experience").click(function(e) {
          e.preventDefault();
          var filterVal = $(this).data("filter");
          if (filterVal === "all") {
            $mediaElements.slideDown("slow");
          } else {
            $mediaElements
              .hide("slow")
              .filter("." + filterVal)
              .slideDown("slow");
          }
        });
    });
}

function applyjob(i){
    var form = new FormData();
    form.append("applicantstatus_id", "1");
    form.append("jobposition_id", i);
    form.append("user_id", sessionStorage.getItem("cur_user"));
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    $.ajax({
        type: 'POST',
        url: "/api/V1.0/applyjob",
        async: true,
        crossDomain: true,
        data: form,
        processData: false,
        contentType: false,
        success: function(response) {
            if(response['status'] == '200'){
                alert(response['message'])
                $("#viewDetail"+ i).modal("hide");
            }else{
                alert(response['message'])
                $("#viewDetail"+ i).modal("hide");
                $("#login").modal("show");
            }
        }
    });
}

function modalDetail(i) {
    if ($("#viewDetail" + i).length) {
        $("#viewDetail" + i).modal("show");
    } else {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/jobdetail",
            async: true,
            crossDomain: true,
            data: {
                jobvacancy_id: i,
            },
            beforeSend: function () {
                $("#preloader-active").show();
            },
            complete: function () {
                $("#preloader-active").hide();
            },
            success: function (response) {
                $("body").append(createmodaldetail(response["jobvacancy"], response["dataform"]));
                $("#viewDetail" + i).modal("show");
            },
        });
    }
}

function createmodaldetail(item, dataform) {
    var html = '<div class="modal fade" id="viewDetail' + item.id + '" tabindex="-1" role="dialog" aria-labelledby="largeModalLabel" aria-hidden="true">';
    html += '<div class="modal-dialog modal-lg" role="document">';
        html += '<div class="modal-content">';
            html += '<div class="modal-header">';
                html += '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
            html += '</div>';
            html += '<div class="modal-body">';
                html += '<div class="card">';
                    html += '<div class="card-body">';
                        html += '<div class="default-tab">';
                            html += '<div class="tab-content pl-3" id="nav-tabContent">';
                                    html += '<div class="card-body card-block">';
                                         html += '<div class="job-post-company">';
                                             html += '<div class="container">';
                                                 html += '<div class="row justify-content-between">';
                                                     html += '<div class="col-lg-12">';
                                                         html += '<div class="single-job-items mb-10">';
                                                             html += '<div class="job-items">';
                                                                 html += '<div class="job-tittle">';
                                                                     html += '<h4>'+item.jobposition+'</h4>';
                                                                     html += '<ul>';
                                                                         html += '<li>'+item.division_id.name+'</li>';
                                                                         html += '<li><i class="fas fa-map-marker-alt"></i>'+item.branch_id.name+'</li>';
                                                                     html += '</ul>';
                                                                 html += '</div>';
                                                             html += '</div>';
                                                         html += '</div>';                             
                                                         html += '<div class="job-post-details">';
                                                             html += '<div class="post-details2 mb-50">';
                                                                 html += '<div class="small-section-tittle">';
                                                                     html += '<h4>Job Description</h4>';
                                                                 html += '</div>';
                                                                    var description;
                                                                    if (item.description) {
                                                                        description = item.description;
                                                                    } else {
                                                                        description = "";
                                                                    }
                                                                 html += '<p>'+description+'</p>';
                                                             html += '</div>';
                                                             html += '<div class="post-details2 mb-50">';
                                                                 html += '<div class="small-section-tittle">';
                                                                     html += '<h4>Required Knowledge, Skills, and Abilities</h4>';
                                                                 html += '</div>';
                                                                    var requirement;
                                                                    if (item.requirement) {
                                                                        requirement = item.requirement;
                                                                    } else {
                                                                        requirement = "";
                                                                    }
                                                                 html += '<p>'+requirement+'</p>';
                                                             html += '</div>';
                                                             html += '<div class="post-details2 mb-50">';
                                                                 html += '<div class="small-section-tittle">';
                                                                     html += '<h4>Education & Experience</h4>';
                                                                 html += '</div>';
                                                                    var experience;
                                                                    if (item.experience) {
                                                                        experience = item.experience
                                                                    } else {
                                                                        experience = "";
                                                                    }
                                                                 html += '<p>'+experience+'</p>';
                                                             html += '</div>';
                                                         html += '</div>';
                                                     html += '</div>';
                                                     html += '<div class="col-lg-12">';
                                                         html += '<div class="post-details3 mb-10">';
                                                            html += '<div class="small-section-tittle">';
                                                                html += '<h4>Job Overview</h4>';
                                                            html += '</div>';
                                                           html += '<ul>';
                                                                var datetime;
                                                                if (item.datetime) {
                                                                    const d = new Date(item.datetime);
                                                                    const ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d);
                                                                    const mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(d);
                                                                    const da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(d);
                                                                    datetime = (`${da}-${mo}-${ye}`);
                                                                } else {
                                                                    datetime = "";
                                                                }
                                                               html += '<li>Posted date : <span>'+datetime+'</span></li>';
                                                               html += '<li>Job type : <span>'+item.jobtype_id.name+'</span></li>';
                                                                    var salary;
                                                                    if (item.salary) {
                                                                        salary = item.salary;
                                                                    } else {
                                                                        salary = "";
                                                                    }
                                                               html += '<li>Salary :  <span>'+salary+'</span></li>';
                                                                var date;
                                                                if (item.applicationdate) {
                                                                    const d = new Date(item.applicationdate);
                                                                    const ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d);
                                                                    const mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(d);
                                                                    const da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(d);
                                                                    date = (`${da}-${mo}-${ye}`);
                                                                } else {
                                                                    date = "";
                                                                }
                                                               html += '<li>Application date : <span>'+date+'</span></li>';
                                                           html += '</ul>';
                                                        html += '</div>';
                                                     html += '</div>';
                                                 html += '</div>';
                                             html += '</div>';
                                         html += '</div>';
                                    html += '</div>';
                                    html += '<div class="modal-footer">';
                                        html += '<div class="items-link items-link2 f-right"><a onclick="applyjob('+item.id+');" style="cursor: pointer;">Apply Now</a></div>';
                                    html += '</div>';
                            html += '</div>';
                        html += '</div>';
                    html += '</div>';
                html += '</div>';
            html += '</div>';
        html += '</div>';
    html += '</div>';
html += '</div>';

return html;
}