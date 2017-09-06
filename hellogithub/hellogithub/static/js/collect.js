var csrftoken = $('meta[name=csrf-token]').attr('content');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});

var show_projects_func = function show_projects() {
    var $collection_project = $(this).parent().next();
    if ($collection_project.attr("hidden")!=null){
        $collection_project.removeAttr("hidden");
    }
    else {
        $collection_project.attr("hidden","hidden");
    }
};


var uncollect_project_func = function uncollect_project() {
    var $this = $(this);
    var collect_project_id = $this.next().text();
    $.ajax({
        url: "/profile/collection/project/",
        type: "DELETE",
        data: {"project_id": collect_project_id},
        success: function(result) {
            $this.removeClass("fa-heart").addClass("fa-heart-o");
            $this.unbind("click");
            $this.on("click", collect_project_func);
            alert(result.message);
        },
        error: function (jqXHR) {
            alert(jqXHR.responseJSON.message);
        }
    });
    if($this.parent().attr("class") == "collection-project-info"){
        $this.parent().remove();
    }
};

var collect_project_func = function collect_project(e) {
    var $favourite = $(".favourite");
    var $collection_name = $("#collection_name");
    var selected_project_name = $(this).prev().html();
    var selected_project_url = $(this).prev().attr("href");
    // 获取该用户的所有收藏夹
    $.ajax({
        url: '/profile/collection/project/',
        type: 'GET',
        success: function (result) {
            $("#project_name").val(selected_project_name);
            $("#project_url").val(selected_project_url);
            var option_str = "";
            $.each(result.payload, function(i, item){
                option_str += "<option value=\""+item.id+"\">"+item.name+"</option>";
            });
            $collection_name.html(option_str);
            // 获取鼠标位置，并显示收藏表单
            $favourite.css({
                left: e.pageX,
                top: e.pageY,
                display: 'block'
            });
        },
        error: function (jqXHR) {
            if (jqXHR.status==401){
                $(".modal").show();
            }
            else {
                alert(jqXHR.responseJSON.message);
            }
        }
    });
};


$(document).ready(function() {

    // 点击空白，隐藏收藏表单
    $(document).mouseup(function(e){
      var _con = $(".favourite");   // 设置目标区域
      if(!_con.is(e.target) && _con.has(e.target).length === 0){ // Mark 1
          _con.hide();
      }
    });
    // 收藏项目
    $("#favourite_submit").click(function() {
        var request_params={
            collection_id: $("#collection_name").val(),
            project_name: $("#project_name").val(),
            project_url: $("#project_url").val()
        };
        $.ajax({
            url: "/profile/collection/project/",
            type: "POST",
            data: request_params,
            success: function(result) {
                var project_id = result.payload.project_id;
                var collect_project_id = result.payload.collect_project_id;
                var $collect_project = $("#collect_"+project_id);
                var $collect_project_id = $collect_project.next();
                $collect_project.removeClass("fa fa-heart-o").addClass("fa fa-heart");
                $collect_project_id.text(collect_project_id);

                // 解绑 click 事件
                $collect_project.unbind("click");
                $collect_project.on("click", uncollect_project_func);
                $(".favourite").hide();
            },
            error: function (jqXHR) {
                $(".favourite").hide();
                alert(jqXHR.responseJSON.message);
            }
        });
    });

    // 点击收藏图标 显示收藏表单
    $(".fa-heart-o").click(collect_project_func);

    // 点击已收藏 绑定取消收藏事件
    $(".fa-heart").click(uncollect_project_func);

    // 点击 取消 按钮的时候，表单消失
    $("#favourite_cancel").click(function() {
        $(".favourite").hide();
    });

    // 登录框 登录按钮
    $("#login_box_submit").click(function() {
        $(this).attr("class", "pure-button pure-button-disabled");
        $(this).text("登录中");
    });
    // 登录框 取消按钮
    $("#login_box_cancel").click(function() {
        $(".modal").hide();
    });


    // 以下为 "我的收藏"
    // 展示收藏夹下的所有项目
    $(".item-name").click(show_projects_func);
    // 创建收藏夹
    $(".collection-form button").click(function () {
        var collection_name = $(".collection-form input").val();
        $.ajax({
            url: "/profile/collection/",
            type: "POST",
            data: {'name': collection_name},
            success: function(result) {
              window.location.reload();
            },
            error: function (jqXHR) {
                alert(jqXHR.responseJSON.message);
            }
        });
    });
    // 删除收藏夹
    $(".item-del.fa.fa-window-close").click(function () {
        var $this = $(this);
        var collection_name = $this.siblings(".item-name").text();
        var collection_id = $this.siblings(".item-id").text();
        var user_choice = window.confirm("确定删除收藏夹："+ collection_name+"?");
        if (user_choice){
            $.ajax({
                url: "/profile/collection/",
                type: "DELETE",
                data: {'collection_id': collection_id},
                success: function(result) {
                    alert(result.message);
                    $this.parent().parent().remove();
                },
                error: function (jqXHR) {
                    alert(jqXHR.responseJSON.message);
                }
            });
        }
    });
});