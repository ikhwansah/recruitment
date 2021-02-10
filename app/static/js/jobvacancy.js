var list_vacancy = {
    async: true,
    crossDomain: true,
    url: "/api/V1.0/jobvacancy",
    method: "POST",
    data: {
        cur_user: sessionStorage.getItem("cur_user"),
        token: sessionStorage.getItem("token"),
    },
    beforeSend: function () {
        $(".spinner").show();
    },
    complete: function () {
        $(".spinner").hide();
    },
};

function reloaddata() {
    $.ajax(list_vacancy).done(function (response) {
        // biodata
        $("#client").val("");
        $("#jobposition").val("");
        $("#salary").val("");
        $("#applicationdate").val("");
        $("#description").val("");
        $("#requirement").val("");
        $("#experience").val("");

        $("#branch").empty();
        $("#branch").append(
            $("<option>", {
                value: "0",
                text: "",
            })
        );
        $.each(response["branch"]["data"], function (i, item) {
            $("#branch").append(
                $("<option>", {
                    value: item.id,
                    text: item.name,
                })
            );
        });

        $("#jobdivision").empty();
        $("#jobdivision").append(
            $("<option>", {
                value: "0",
                text: "",
            })
        );
        $.each(response["division"]["data"], function (i, item) {
            $("#jobdivision").append(
                $("<option>", {
                    value: item.id,
                    text: item.name,
                })
            );
        });

        $("#jobtype").empty();
        $("#jobtype").append(
            $("<option>", {
                value: "0",
                text: "",
            })
        );
        $.each(response["jobtype"]["data"], function (i, item) {
            $("#jobtype").append(
                $("<option>", {
                    value: item.id,
                    text: item.name,
                })
            );
        });

        $("#experience_id").empty();
        $("#experience_id").append(
            $("<option>", {
                value: "0",
                text: "",
            })
        );
        $.each(response["experience"]["data"], function (i, item) {
            $("#experience_id").append(
                $("<option>", {
                    value: item.id,
                    text: item.name,
                })
            );
        });

        jobvacancy = response["jobvacancy"]["data"];
        $.fn.dataTable.ext.errMode = "none";
        $("#jobtable").append("<thead><tr><th>Job Title</th><th>Branch</th><th>Description</th><th>Action</th></tr></thead>");
        $('#jobtable thead tr').clone(true).appendTo( '#jobtable thead' );
        $('#jobtable thead tr:eq(1) th').each( function (i) {
            var title = $(this).text();
            $(this).html( '<input type="text" placeholder="Search" />' );
     
            $( 'input', this ).on( 'keyup change', function () {
                if ( table.column(i).search() !== this.value ) {
                    table
                        .column(i)
                        .search( this.value )
                        .draw();
                }
            } );

            $('input', this).css({'width':'60px' ,'display':'inline-block'});
            $(this).css({'background':'white', 'border':'none'});
        } );
        function strtrunc(str, max, add){
           add = add || '...';
           return (typeof str === 'string' && str.length > max ? str.substring(0, max) + add : str);
        };
        var table = $("#jobtable").DataTable({
            orderCellsTop: true,
            fixedHeader: true,
            data: jobvacancy,
            language: {
                emptyTable: "Tidak Ada Data",
            },
            columns: [
                {
                    data: "jobposition",
                    defaultContent: ""
                },
                {
                    data: "branch_id.name",
                    defaultContent: "",
                    render: function(data, type, full, meta){
                      if(type === 'display'){
                         data = strtrunc(data, 20);
                      }                     
                      return data;
                   }
                },
                {
                    data: "description",
                    defaultContent: "",
                    render: function(data, type, full, meta){
                      if(type === 'display'){
                         data = strtrunc(data, 50);
                      }                     
                      return data;
                   }
                },
                {
                    data: null,
                    className: "dt-body-center",
                    width: "10%",
                    defaultContent: "",
                    render: function (data, type, full, meta) {
                        if (type === "filter") {
                            $("#editJobVacancy" + data.id).empty();
                            $("#editJobVacancy" + data.id).remove();
                            $("#deleteJob" + data.id).empty();
                            $("#deleteJob" + data.id).remove();
                            $("body").append(createmodaldelete(data));
                        }
                        return (
                            '<div class="table-data-feature"><button data-toggle="modal" class="item" data-toggle="tooltip" data-placement="top" title="Edit" onclick="modalEdit('+data.id+');"><i class="zmdi zmdi-edit"></i></button> <button class="item" data-toggle="tooltip" data-placement="top" title="Delete" onclick="modalDelete('+data.id+');"><i class="zmdi zmdi-delete"></i></button></div>'
                        );
                    },
                },
            ]
        });
               
    }); //list_employee

    if ($.fn.DataTable.isDataTable("#jobtable")) {
        $("#jobtable").dataTable().fnDestroy();
        $("#jobtable").empty();
    }
} //reloaddata

function modalEdit(i) {
    if ($("#editJobVacancy" + i).length) {
        $("#editJobVacancy" + i).modal("show");
        $("#idedit").val(i);
    } else {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/jobvacancydetail",
            async: true,
            crossDomain: true,
            data: {
                cur_user: sessionStorage.getItem("cur_user"),
                token: sessionStorage.getItem("token"),
                jobvacancy_id: i,
            },
            success: function (response) {
                $("body").append(createmodaledit(response["jobvacancy"], response["dataform"]));
                $("#editJobVacancy" + i).modal("show");
                $("#idedit").val(i);
            },
        });
    }
}

function modalDelete(i) {
    $("#deleteJob" + i).modal("show");
}

function createmodaledit(data, dataform) {
    var html = '<div class="modal fade" id="editJobVacancy' + data.id + '" tabindex="-1" role="dialog" aria-labelledby="largeModalLabel" aria-hidden="true">';
    html += '<div class="modal-dialog modal-lg" role="document">';
        html += '<div class="modal-content">';
            html += '<div class="modal-header">';
                html += '<h5 class="modal-title" id="largeModalLabel">Input Job Vacancy</h5>';
                html += '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
            html += '</div>';
            html += '<div class="modal-body">';
                html += '<div class="card">';
                    html += '<div class="card-body">';
                        html += '<div class="default-tab">';
                            html += '<nav>';
                                html += '<div class="nav nav-tabs" id="nav-tab" role="tablist">';
                                    html += '<a class="nav-item nav-link active" id="nav-job-tab" data-toggle="tab" href="#nav-job' + data.id + '" role="tab" aria-controls="nav-job" aria-selected="true">Job Vacancy</a>';
                                html += '</div>';
                            html += '</nav>';
                            html += '<div class="tab-content pl-3 pt-2" id="nav-tabContent">';
                                html += '<div class="tab-pane fade show active" id="nav-job' + data.id + '" role="tabpanel" aria-labelledby="nav-job-tab">';
                                    html += '<div class="card-body card-block">';
                                        html += '<div class="row">';
                                            html += '<div class="col-12">';
                                                html += '<div class="form-group">';
                                                    html += '<label class="control-label mb-1">Job Title</label>';
                                                        var jobposition;
                                                        if (data.jobposition) {
                                                            jobposition = data.jobposition;
                                                        } else {
                                                            jobposition = "";
                                                        }
                                                    html += '<input id="jobposition' + data.id + '" type="text" class="form-control" value="' + jobposition + '">';
                                                html += '</div>';
                                            html += '</div>';
                                        html += '</div>';
                                        html += '<div class="row">';
                                            html += '<div class="col-6">';
                                                html += '<div class="form-group">';
                                                    html += '<label class="control-label mb-1">Branch</label>';
                                                    html += '<select id="branch' + data.id + '" class="form-control">';
                                                        html += '<option value = "0">Select Branch</option>';
                                                        $.each(dataform["branch"]["data"], function (key, value) {
                                                            selected = "";
                                                            if (value.id == data.branch_id.id) {
                                                                selected = "selected";
                                                            } else {
                                                                selected = "";
                                                            }
                                                            html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
                                                        });
                                                    html += "</select>";
                                                html += '</div>';
                                            html += '</div>';
                                            html += '<div class="col-6">';
                                                html += '<div class="form-group">';
                                                    html += '<label class="control-label mb-1">Division</label>';
                                                    html += '<select id="jobdivision' + data.id + '" class="form-control">';
                                                        html += '<option value = "0">Select Division</option>';
                                                        $.each(dataform["division"]["data"], function (key, value) {
                                                            selected = "";
                                                            if (value.id == data.division_id.id) {
                                                                selected = "selected";
                                                            } else {
                                                                selected = "";
                                                            }
                                                            html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
                                                        });
                                                    html += "</select>";
                                                html += '</div>';
                                            html += '</div>';
                                        html += '</div>';
                                        html += '<div class="row">';
                                            html += '<div class="col-6">';
                                                html += '<div class="form-group">';
                                                    html += '<label class="control-label mb-1">Job type</label>';
                                                    html += '<select id="jobtype' + data.id + '" class="form-control">';
                                                        html += '<option value = "0">Select Job Type</option>';
                                                        $.each(dataform["jobtype"]["data"], function (key, value) {
                                                            selected = "";
                                                            if (value.id == data.jobtype_id.id) {
                                                                selected = "selected";
                                                            } else {
                                                                selected = "";
                                                            }
                                                            html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
                                                        });
                                                    html += "</select>";
                                                html += '</div>';
                                            html += '</div>';
                                            html += '<div class="col-6">';
                                                html += '<div class="form-group">';
                                                    html += '<label class="control-label mb-1">Salary</label>';
                                                    var salary;
                                                        if (data.salary) {
                                                            salary = data.salary;
                                                        } else {
                                                            salary = "";
                                                        }
                                                    html += '<input id="salary' + data.id + '" type="text" class="form-control" value="' + salary + '">';
                                                html += '</div>';
                                            html += '</div>';
                                        html += '</div>';
                                        html += '<div class="row">';
                                            html += '<div class="col-6">';
                                                html += '<div class="form-group">';
                                                    html += '<label class="control-label mb-1">Application date</label>';
                                                    var applicationdate;
                                                    if (data.applicationdate) {
                                                        applicationdate = data.applicationdate;
                                                    } else {
                                                        applicationdate = "";
                                                    }
                                                    html += '<input type="date" id="applicationdate' + data.id + '" class="form-control" value="' + applicationdate + '">';
                                                html += '</div>';
                                            html += '</div>';
                                            html += '<div class="col-6">';
                                                html += '<div class="form-group">';
                                                    html += '<label class="control-label mb-1">Experience</label>';
                                                    html += '<select id="experience_id' + data.id + '" class="form-control">';
                                                        html += '<option value = "0">Select Experience</option>';
                                                        $.each(dataform["experience"]["data"], function (key, value) {
                                                            selected = "";
                                                            if (value.id == data.experience_id.id) {
                                                                selected = "selected";
                                                            } else {
                                                                selected = "";
                                                            }
                                                            html += '<option value="' + value.id + '" ' + selected + ">" + value.name + "</option>";
                                                        });
                                                    html += "</select>";
                                                html += '</div>';
                                            html += '</div>';
                                        html += '</div>';
                                        html += '<div class="row">';
                                            html += '<div class="col-12">';
                                                html += '<label>Description</label>';
                                                    var description;
                                                    if (data.description) {
                                                        description = data.description;
                                                    } else {
                                                        description = "";
                                                    }
                                                html += '<textarea name="textarea-input" id="description' + data.id + '" rows="9" placeholder="Input Job Description" class="form-control">' + description + '</textarea>';
                                            html += '</div>';
                                        html += '</div>';
                                        html += '<div class="row">';
                                            html += '<div class="col-12">';
                                                html += '<label>Requirements</label>';
                                                    var requirement;
                                                    if (data.requirement) {
                                                        requirement = data.requirement;
                                                    } else {
                                                        requirement = "";
                                                    }
                                                html += '<textarea name="textarea-input" id="requirement' + data.id + '" rows="9" placeholder="Input Required Knowledge, Skills, and Abilities" class="form-control">' + requirement + '</textarea>';
                                            html += '</div>';
                                        html += '</div>';
                                        html += '<div class="row">';
                                            html += '<div class="col-12">';
                                                html += '<label>Education & Experience</label>';
                                                    var experience;
                                                    if (data.experience) {
                                                        experience = data.experience;
                                                    } else {
                                                        experience = "";
                                                    }
                                                html += '<textarea name="textarea-input" id="experience' + data.id + '" rows="9" placeholder="Input Education & Experience" class="form-control">' + experience + '</textarea>';
                                            html += '</div>';
                                        html += '</div>';
                                    html += '</div>';
                                    html += '<div class="modal-footer">';
                                        html += '<button onclick="editJobvacancy(' + data.id + ')" id="submit-button" class="btn btn-info"><i class="fa fa-check-square"></i><span> Save</span></button>';
                                        html += '<button type="button" class="btn btn-secondary" data-dismiss="modal"><i class="fa fa-times"></i><span> Cancel</span></button>';
                                    html += '</div>';
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

function createmodaldelete(data) {
    var html = '<div class="modal fade" id="deleteJob' + data.id + '" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">';
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
    html += '<button id="delete" onclick="DeleteJob(' + data.id + ')" class="btn btn-info">';
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

function addJobVacancy() {
    var form = new FormData();
    valid = false;
    form.append("jobvacancy_id", '');
    form.append("client_id", "1");
    if ($("#jobposition").val() == "") {
        $("#jobposition").focus();
        alert("Job title not filled in");
        valid = false;
    } else {
        jobposition = $("#jobposition").val();
        form.append("jobposition", jobposition);
        valid = true;
    }
    if ($("#branch").val() == "0") {
        $("#branch").focus();
        alert("Branch not filled in");
        valid = false;
    } else {
        branch = $("#branch").val();
        form.append("branch_id", branch);
        valid = true;
    }
    if ($("#jobdivision").val() == "0") {
        $("#jobdivision").focus();
        alert("Division not filled in");
        valid = false;
    } else {
        jobdivision = $("#jobdivision").val();
        form.append("division_id", jobdivision);
        valid = true;
    }
    if ($("#jobtype").val() == "0") {
        $("#jobtype").focus();
        alert("Job type not filled in");
        valid = false;
    } else {
        jobtype = $("#jobtype").val();
        form.append("jobtype_id", jobtype);
        valid = true;
    }
    salary = $("#salary").val();
    form.append("salary", salary);
    if ($("#applicationdate").val() == "0") {
        $("#applicationdate").focus();
        alert("Application date not filled in");
        valid = false;
    } else {
        applicationdate = $("#applicationdate").val();
        form.append("applicationdate", applicationdate);
        valid = true;
    }
    if ($("#experience_id").val() == "0") {
        $("#experience_id").focus();
        alert("Experience not filled in");
        valid = false;
    } else {
        experience_id = $("#experience_id").val();
        form.append("experience_id", experience_id);
        valid = true;
    }
    if ($("#description").val() == "") {
        $("#description").focus();
        alert("Job description not filled in");
        valid = false;
    } else {
        description = $("#description").val();
        form.append("description", description);
        valid = true;
    }
    requirement = $("#requirement").val();
    form.append("requirement", requirement);
    experience = $("#experience").val();
    form.append("experience", experience);
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/insertjobvacancy",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    $("#addid").val(response.jobvacancy_id);
                    alert("Job Vacancy Successfully Added");
                    $("#job").modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                }
            },
        });
    }
}

function addJobFile() {
    var form = new FormData();
    valid = true;
    fotojob = $("#fotojob").val();
    var pictureInput = document.getElementById("fotojob").files[0];
    form.append("fotojob", pictureInput);
    filejob = $("#filejob").val();
    var pictureInput = document.getElementById("filejob").files[0];
    form.append("filejob", pictureInput);
    idfilejob = $("#idfilejob").val();
    form.append("filejob_id", idfilejob);
    jobid = $("#jobid").val();
    form.append("fotojob_id", jobid);
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    addid = $("#addid").val();
    form.append("jobvacancy_id", addid);
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/insertfilejv",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    alert("Job Vacancy Successfully Added");
                    $("#job").modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                }
            },
        });
    }
}

function editJobFile(i) {
    var form = new FormData();
    valid = true;
    fotojob = $("#fotojob" + i).val();
    var pictureInput = document.getElementById("fotojob" + i).files[0];
    form.append("fotojob", pictureInput);
    filejob = $("#filejob" + i).val();
    var pictureInput = document.getElementById("filejob" + i).files[0];
    form.append("filejob", pictureInput);
    idfilejob = $("#idfilejob" + i).val();
    form.append("filejob_id", idfilejob);
    jobid = $("#jobid" + i).val();
    form.append("fotojob_id", jobid);
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    form.append("jobvacancy_id", i);
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/insertfilejv",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    alert("Job Vacancy Successfully Added");
                    $("#editJobVacancy" + i).modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                }
            },
        });
    }
}

function editJobvacancy(i) {
    var form = new FormData();
    valid = false;
    form.append("client_id", "1");
    if ($("#jobposition" + i).val() == "") {
        $("#jobposition" + i).focus();
        alert("Job title not filled in");
        valid = false;
    } else {
        jobposition = $("#jobposition" + i).val();
        form.append("jobposition", jobposition);
        valid = true;
    }
    if ($("#branch" + i).val() == "0") {
        $("#branch" + i).focus();
        alert("Branch not filled in");
        valid = false;
    } else {
        branch = $("#branch" + i).val();
        form.append("branch_id", branch);
        valid = true;
    }
    if ($("#jobdivision" + i).val() == "0") {
        $("#jobdivision" + i).focus();
        alert("Division not filled in");
        valid = false;
    } else {
        jobdivision = $("#jobdivision" + i).val();
        form.append("division_id", jobdivision);
        valid = true;
    }
    if ($("#jobtype" + i).val() == "0") {
        $("#jobtype" + i).focus();
        alert("Job type not filled in");
        valid = false;
    } else {
        jobtype = $("#jobtype" + i).val();
        form.append("jobtype_id", jobtype);
        valid = true;
    }
    salary = $("#salary" + i).val();
    form.append("salary", salary);
    if ($("#applicationdate" + i).val() == "0") {
        $("#applicationdate" + i).focus();
        alert("Application date not filled in");
        valid = false;
    } else {
        applicationdate = $("#applicationdate" + i).val();
        form.append("applicationdate", applicationdate);
        valid = true;
    }
    if ($("#experience_id" + i).val() == "0") {
        $("#experience_id" + i).focus();
        alert("Experience not filled in");
        valid = false;
    } else {
        experience_id = $("#experience_id" + i).val();
        form.append("experience_id", experience_id);
        valid = true;
    }
    if ($("#description" + i).val() == "") {
        $("#description" + i).focus();
        alert("Job description not filled in");
        valid = false;
    } else {
        description = $("#description" + i).val();
        form.append("description", description);
        valid = true;
    }
    requirement = $("#requirement" + i).val();
    form.append("requirement", requirement);
    experience = $("#experience" + i).val();
    form.append("experience", experience);
    form.append("jobvacancy_id", i);
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    if (valid == true) {
        $.ajax({
            type: "POST",
            url: "/api/V1.0/insertjobvacancy",
            async: true,
            crossDomain: true,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response["status"] == "400") {
                    alert(response["message"]);
                } else {
                    alert("Job Vacancy Successfully Edited");
                    $("#editJobVacancy" + i).modal("hide");
                    $(".modal-backdrop.fade.show").remove();
                    reloaddata();
                }
            },
        });
    }
}

function DeleteJob(i) {
    id = i;
    var form = new FormData();
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    form.append("token", sessionStorage.getItem("token"));
    form.append("id", id);
    $.ajax({
        type: "POST",
        url: "/api/V1.0/removejobvacancy",
        async: true,
        crossDomain: true,
        data: form,
        mimeType: "multipart/form-data",
        processData: false,
        contentType: false,
        success: function (response) {
            if (response["status"] == "400") {
                alert(response["message"]);
            } else {
                $("#deleteJob" + i).modal("hide");
                reloaddata();
            }
        },
    });
}

function getfilejob(filejobid, id) {
    $.ajax({
        type: "POST",
        url: "/upload_pdf",
        async: true,
        crossDomain: true,
        data: {
            cur_user: sessionStorage.getItem("cur_user"),
            token: sessionStorage.getItem("token"),
            filejob: filejobid,
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
            var title = "File";
            win.document.write("<html><title>" + title + '</title><body style="margin-top: 0px; margin-left: 0px; margin-right: 0px; margin-bottom: 0px;">');
            win.document.write(objbuilder);
            win.document.write("</body></html>");
            layer = jQuery(win.document);
        },
    });
}

function fillattachment(data) {
    var form = new FormData();
    form.append("file_id", data.fotojob.id);
    form.append("token", sessionStorage.getItem("token"));
    form.append("cur_user", sessionStorage.getItem("cur_user"));
    $.ajax({
        async: true,
        crossDomain: true,
        url: "/vacancy_images/" + data.fotojob.name,
        method: "POST",
        processData: false,
        contentType: false,
        datatype: "JSON",
        mimeType: "multipart/form-data",
        data: form,
        success: function (response) {
            $("#jobphoto" + data.id).html(
                '<label for="images" class="control-label mb-1">Upload Image</label><br/><img src="data:image/jpeg;base64,'+
                    response +'" style="width: 213px; height: 213px;"/><input type="file" name="fotojob" id="fotojob'+ data.id +'" class="form-control"/><input type="hidden" id="jobid'+ data.id +'" value="'+ data.fotojob.id +'"><p class="small">Max upload file: 2MB</p>'
            );
        },
    });

    if (data.filejob.id) {
        $("#filejobphoto" + data.id).html(
            '<label class="control-label mb-1">Upload File</label><input type="file" name="filejob" id="filejob'+ data.id +'" class="form-control"/><a href="javascript:getfilejob('+ data.filejob.id +"," + data.id +');" >'+ data.filejob.name +'</a><input type="hidden" id="idfilejob'+ data.id +'" value="'+ data.filejob.id +'"><p class="small">Jenis file: PDF, Max: 5MB</p>'
        );
    } else {
        $("#filejobphoto" + data.id).html('<label class="control-label mb-1">Upload File</label><br/><input type="file" name="filejob" id="filejob' + data.id + '" class="form-control"/>');
    }
}