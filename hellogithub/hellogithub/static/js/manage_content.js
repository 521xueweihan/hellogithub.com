/**
 * Created by XueWeiHan on 17/7/14 下午11:40.
 */
var csrftoken = $('meta[name=csrf-token]').attr('content');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});

$(document).ready(function() {
    // {# 动态展示对应的 subset #}
    $("#type").change(function(){
        var type_value = $(this).val();
        if (type_value == "volume"){
            $("#subset-volume").removeAttr("hidden");
            $("#subset-category").attr("hidden", "hidden");
        }
        else if (type_value == "category")
        {
            $("#subset-category").removeAttr("hidden");
            $("#subset-volume").attr("hidden", "hidden");
        }
    });

    // {# 异步展示 content-list #}
    $("#type-submit").click(function() {
        var type_value = $("#type").val();
        var request_params = {
            type: type_value,
            subset: $("#subset-"+type_value).val()
        };
        $.ajax({
            url: "/manage/list/",
            type: "GET",
            data: request_params,
            success: function (result) {
                var contents = "";
                $.each(result.payload, function(i, item){
                    i = i+1;
                    var content_status = '';
                    if (item.status == 1) {
                        content_status = "<td><span style=\'color: #33b045\'>"+
                                         "已上线"+
                                         "</span></td>"
                    }
                    else {
                        content_status = "<td><span style=\'color: red\'>"+
                                         "未上线"+
                                         "</span></td>"
                    }

                    contents += "<tr>"+
                        "<td>"+i+"</td>" +
                        "<td id=\"project-title\">"+item.title+"</td>" +
                        "<td>"+item.category.name+"</td>" +
                        "<td>"+item.volume.name+"</td>" +
                        content_status +
                        "<td><button type=\"button\" id=\"edit-project-button\" value=\""+ item.id +"\" class=\"button-warning button-xsmall pure-button\">编辑</button>" +
                        "&nbsp;" +
                        "<button type=\"button\" id=\"delete-project-submit\" value=\""+ item.id +"\" class=\"button-error button-xsmall pure-button\">删除</button></td>" +
                    "</tr>";
                });
                contents = "<table class=\"pure-table\">"+
                    "<thead>"+
                        "<tr>"+
                            "<th>#</th>"+
                            "<th>Title</th>"+
                            "<th>Category</th>"+
                            "<th>Vol.</th>"+
                            "<th>状态</th>"+
                            "<th>操作</th>"+
                        "</tr>"+
                    "</thead>"+
                    "<tbody>"+
                        contents+
                    "</tbody>"+
                    "</table>";
                $("#result").html(contents);
            },
            error: function (jqXHR) {
               alert(jqXHR.responseJSON.message);
            }});
    });

    // {# Search #}
    $("#search-submit").click(function() {
        $.ajax({
            url: "/manage/search/",
            type: "GET",
            data: {project_url: $("#search-project-url").val()},
            success: function (result) {
                if(!result.payload){
                    $("#result").html(result.message);
                    return;
                }
                var item = result.payload;
                var content_status = '';
                if (item.status == 1) {
                    content_status = "<td><span style=\'color: #33b045\'>"+
                                     "已上线"+
                                     "</span></td>"
                }
                else {
                    content_status = "<td><span style=\'color: red\'>"+
                                     "未上线"+
                                     "</span></td>"
                }
                $("#result").html(
                    "<table class=\"pure-table\">"+
                    "<thead>"+
                        "<tr>"+
                            "<th>ID</th>"+
                            "<th>Title</th>"+
                            "<th>Category</th>"+
                            "<th>Vol.</th>"+
                            "<th>状态</th>"+
                            "<th>操作</th>"+
                        "</tr>"+
                    "</thead>"+
                    "<tbody>"+
                        "<tr>"+
                            "<td>"+item.id+"</td>" +
                            "<td id=\"project-title\">"+item.title+"</td>" +
                            "<td>"+item.category.name+"</td>" +
                            "<td>"+item.volume.name+"</td>" +
                            content_status +
                            "<td><button type=\"button\" id=\"edit-project-button\" value=\""+ item.id +"\" class=\"button-warning button-xsmall pure-button\">编辑</button>" +
                            "&nbsp;" +
                            "<button type=\"button\" id=\"delete-project-submit\" value=\""+ item.id +"\" class=\"button-error button-xsmall pure-button\">删除</button></td>" +
                        "</tr>"+
                    "</tbody>"+
                    "</table>"
                );
            },
            error: function (jqXHR) {
               alert(jqXHR.responseJSON.message);
            }});
    });
});


// {# 生成编辑 project 表单 #}
$(document).on("click", "#edit-project-button", function() {
    $.ajax({
        url: "/manage/",
        type: "GET",
        data: {project_id: $(this).val()},
        success: function(result) {
            var data = result.payload;
            var category_list = data.category_list;
            var volume_list = data.volume_list;
            var category_str = "";
            for (var category_i=0,category_len=category_list.length;
                 category_i<category_len; category_i++)
            {
                if (data.category.id == category_list[category_i][0]){
                    category_str+= "<option selected value=\""+
                        category_list[category_i][0]+ "\">"+
                        category_list[category_i][1]+"</option>"
                }
                else {
                    category_str+= "<option value=\""+
                        category_list[category_i][0]+ "\">"+
                        category_list[category_i][1]+"</option>"
                }
            }

            var volume_str = "";
            for (var volume_i=0,volume_len=volume_list.length;
                 volume_i<volume_len; volume_i++)
            {
                if (data.volume.id == volume_list[volume_i][0]){
                    volume_str+= "<option selected value=\""+
                        volume_list[volume_i][0]+ "\">"+
                        volume_list[volume_i][1]+ "</option>"
                }
                else {
                    volume_str+= "<option value=\""+
                        volume_list[volume_i][0]+ "\">"+
                        volume_list[volume_i][1]+"</option>"
                }

            }

            $("#result").html(
                "<form class=\"pure-form\">"+
                "<fieldset>"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"project-title\">Project Title：</label>"+
                        "<input id=\"project-title\" value=\""+data.title+"\" type=\"text\" class=\"pure-input-1-2\">"+
                    "</div>"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"project-url\">Project URL：</label>"+
                        "<input id=\"project-url\" value=\""+data.project_url+"\" type=\"text\" class=\"pure-input-1-2\">"+
                    "</div>"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"project-image\">Project Image：</label>"+
                        "<input id=\"project-image\"  value=\""+data.image_name+"\" type=\"text\" class=\"pure-input-1-2\">"+
                    "</div>"+
                "</fieldset>"+
                "<fieldset class=\"pure-group\">"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"project-category\">Category：</label>"+
                        "<select id=\"project-category\">"+
                            category_str+
                        "</select>"+
                    "</div>"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"project-volume\">Volume：</label>"+
                        "<select id=\"project-volume\">"+
                            volume_str+
                        "</select>"+
                    "</div>"+
                "</fieldset>"+
                "<fieldset class=\"pure-group\">"+
                    "<textarea id=\"project-description\" class=\"pure-input-1\" rows=\"10\">"+data.description+"</textarea>"+
                "</fieldset>"+
                "<button id=\"edit-project-submit\" value=\""+data.id+"\" type=\"button\" class=\"pure-button pure-input-1 pure-button-primary\">Submit</button>"+
                "</form>"
            );
        }
    });
});

// {# 更新 project 数据 #}
$(document).on("click", "#edit-project-submit", function() {
    var request_params={
        project_id: $(this).val(),
        volume_id: $("#project-volume").val(),
        description: $("#project-description").val(),
        category_id: $("#project-category").val(),
        title: $("#project-title").val(),
        project_url: $("#project-url").val(),
        image_name: $("#project-image").val()
    };
    $.ajax({
        url: "/manage/",
        type: "PUT",
        data: request_params,
        success: function(result) {
            $("#result").html(result.message);
        },
        error: function (jqXHR) {
           alert(jqXHR.responseJSON.message);
        }});
});

// {# 生成增加 project 表单 #}
$(document).on("click", "#create-project-button", function () {
    var all_volume_html = $("#subset-volume").html();
    var all_category_html = $("#subset-category").html();
    $("#result").html(
                "<form class=\"pure-form\">"+
                "<fieldset>"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"project-title\">Project Title：</label>"+
                        "<input id=\"project-title\" type=\"text\" class=\"pure-input-1-2\">"+
                    "</div>"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"project-url\">Project URL：</label>"+
                        "<input id=\"project-url\" type=\"text\" class=\"pure-input-1-2\">"+
                    "</div>"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"project-image\">Project Image：</label>"+
                        "<input id=\"project-image\" type=\"text\" class=\"pure-input-1-2\">"+
                    "</div>"+
                "</fieldset>"+
                "<fieldset class=\"pure-group\">"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"project-category\">Category：</label>"+
                        "<select id=\"project-category\">"+
                            all_category_html+
                        "</select>"+
                    "</div>"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"project-volume\">Volume：</label>"+
                        "<select id=\"project-volume\">"+
                            all_volume_html+
                        "</select>"+
                    "</div>"+
                "</fieldset>"+
                "<fieldset class=\"pure-group\">"+
                    "<textarea id=\"project-description\" class=\"pure-input-1\" rows=\"10\"></textarea>"+
                "</fieldset>"+
                "<button id=\"create-project-submit\" type=\"button\" class=\"pure-button pure-input-1 pure-button-primary\">Submit</button>"+
                "</form>"
            );
});

// {# 新增 project 数据 #}
$(document).on("click", "#create-project-submit", function() {
    var request_params={
        volume_id: $("#project-volume").val(),
        description: $("#project-description").val(),
        category_id: $("#project-category").val(),
        title: $("#project-title").val(),
        project_url: $("#project-url").val(),
        image_name: $("#project-image").val()
    };
    $.ajax({
        url: "/manage/",
        type: "POST",
        data: request_params,
        success: function(result) {
            $("#result").html(result.message);
        },
       error: function (jqXHR) {
           alert(jqXHR.responseJSON.message);
        }});
});

// {# 删除 project #}
$(document).on("click", "#delete-project-submit", function() {
    var project_title = $(this).parent().siblings("#project-title").text();
    var project_id = $(this).val();
    var user_choice = window.confirm("确定删除："+ project_title+"?");
    if(user_choice) {
        $.ajax({
            url: '/manage/',
            type: 'DELETE',
            data: {
                project_title: project_title,
                project_id: project_id
            },
            success: function (result) {
                $("#result").html(result.message);
            },
            error: function (jqXHR) {
                alert(jqXHR.responseJSON.message);
            }
        });
    }
});
