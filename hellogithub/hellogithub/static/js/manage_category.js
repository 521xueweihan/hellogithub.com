/**
 * Created by XueWeiHan on 17/7/14 下午11:54.
 */
// {# 新增分类 #}
$(document).ready(function() {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });
    $("#create-category-submit").click(function() {
        $.ajax({
            url: '/manage/category/',
            type: 'POST',
            data: {
                category_name: $("#create-category-name").val()
            },
            success: function (result) {
                if (result.code == 200){
                    $("#result").html(result.message);
                }
                else {
                    alert(result.message);
                }
            }
        });
    });
});

// {# 生成编辑 category 表单#}
$(document).on("click", "#edit-category-button", function() {
    $.ajax({
        url: "/manage/category/",
        type: "GET",
        data: { category_id: $(this).val() },
        success: function(result) {
            $("#result").html("<form class=\"pure-form\">"+
                "<fieldset class=\"pure-group\">"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"category-name\">Category Name：</label>"+
                        "<input id=\"category-name\" value=\""+result.message.name+"\" type=\"text\" class=\"pure-input-1-2\">"+
                    "</div>"+
                "</fieldset>"+

                "<button id=\"edit-category-submit\" value=\""+result.message.id+"\" type=\"button\" class=\"pure-button pure-input-1 pure-button-primary\">Submit</button>"+
            "</form>");
        }
    });
});

// {# 编辑 category #}
$(document).on("click", "#edit-category-submit", function() {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });
    $.ajax({
        url: "/manage/category/",
        type: "PUT",
        data: {
            category_id: $(this).val(),
            category_name: $("#category-name").val()
        },
        success: function(result) {
            if (result.code == 200){
                $("#result").html(result.message);
            }
            else {
                alert(result.message);
            }
        }
    });
});

// {# 删除 category #}
$(document).on("click", "#delete-category-submit", function() {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });
    var category_name = $(this).parent().siblings("#category-name").text();
    var category_id = $(this).parent().siblings("#category-id").text();
    $.ajax({
        url: "/manage/category/",
        type: "DELETE",
        data: {
            category_name: category_name,
            category_id: category_id
        },
        success: function (result) {
            if (result.code == 200){
                $("#result").html(result.message);
            }
            else {
                alert(result.message);
            }
        }
    });
});

