/**
 * Created by XueWeiHan on 17/7/14 下午11:57.
 */
var csrftoken = $('meta[name=csrf-token]').attr('content');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});

// {# 新增Vol. #}
$(document).ready(function() {
    $("#create-volume-submit").click(function () {
        $.ajax({
            url: '/manage/volume/',
            type: 'POST',
            data: {
                volume_name: $("#create-volume-name").val()
            },
            success: function (result) {
                $("#result").html(result.message);
            },
            error: function (jqXHR) {
                alert(jqXHR.responseJSON.message);
            }
        });
    });
});

// {# 生成编辑 volume 表单#}
$(document).on("click", "#edit-volume-button", function() {
    $.ajax({
        url: "/manage/volume/",
        type: "GET",
        data: { volume_id: $(this).val() },
        success: function(result) {
            $("#result").html("<form class=\"pure-form\">"+
                "<fieldset class=\"pure-group\">"+
                    "<div class=\"pure-control-group\">"+
                        "<label for=\"volume-name\">Volume Name：</label>"+
                        "<input id=\"volume-name\" value=\""+result.payload.name+"\" type=\"text\" class=\"pure-input-1-2\">"+
                    "</div>"+
                "</fieldset>"+

                "<button id=\"edit-volume-submit\" value=\""+result.payload.id+"\" type=\"button\" class=\"pure-button pure-input-1 pure-button-primary\">Submit</button>"+
            "</form>");
        }
    });
});

// {# 编辑 volume #}
$(document).on("click", "#edit-volume-submit", function() {
    $.ajax({
        url: "/manage/volume/",
        type: "PUT",
        data: {
            volume_id: $(this).val(),
            volume_name: $("#volume-name").val()
        },
        success: function(result) {
            $("#result").html(result.message);
        },
        error: function (jqXHR) {
            alert(jqXHR.responseJSON.message);
        }
    });
});

// {# 删除 volume #}
$(document).on("click", "#delete-volume-submit", function() {
    var volume_name = $(this).parent().siblings("#volume-name").text();
    var volume_id = $(this).parent().siblings("#volume-id").text();
    var user_choice = window.confirm("确定删除 Vol.："+ volume_name +"?");
    if(user_choice) {
        $.ajax({
            url: "/manage/volume/",
            type: "DELETE",
            data: {
                volume_name: volume_name,
                volume_id: volume_id
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

// {# 发布 volume #}
$(document).on("click", "#publish-volume-submit", function() {
    $.ajax({
        url: "/manage/publish/volume/",
        type: "POST",
        data: {
            volume_id: $(this).val()
        },
        success: function(result) {
            $("#result").html(result.message);
        },
        error: function (jqXHR) {
            alert(jqXHR.responseJSON.message);
        }
    });
});

// {# 生成 github markdown #}
$(document).on("click", "#outpout-markdown-github-submit", function() {
    $.ajax({
        url: "/manage/output/",
        type: "GET",
        data: { volume_id: $(this).val(), output_type: "github" },
        success: function(result) {
            $("#result").html("<form class=\"pure-form\">"+
                "<fieldset class=\"pure-group\">"+
                    "<fieldset class=\"pure-group\">"+
                    "<textarea id=\"project-description\" class=\"pure-input-1\" rows=\"20\">"+result.payload+"</textarea>"+
                "</fieldset>"+
            "</form>");
        }
    });
});

// {# 生成 gitbook markdown #}
$(document).on("click", "#outpout-markdown-gitbook-submit", function() {
    $.ajax({
        url: "/manage/output/",
        type: "GET",
        data: { volume_id: $(this).val(), output_type: "gitbook" },
        success: function(result) {
            $("#result").html("<form class=\"pure-form\">"+
                "<fieldset class=\"pure-group\">"+
                    "<fieldset class=\"pure-group\">"+
                    "<textarea id=\"project-description\" class=\"pure-input-1\" rows=\"20\">"+result.payload+"</textarea>"+
                "</fieldset>"+
            "</form>");
        }
    });
});
