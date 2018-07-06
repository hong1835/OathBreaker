/*--------------------------------
 * Author: luozh@snail.com
 * Date: 2015-08-03
 * Usage:
 *--------------------------------
 */


$(function () {

    var urlArr = ['/restart/', '/modify_pwd/',
        '/script/', '/send_file/',
        '/md_manage/', '/example_manage/', '/job_manage/', '/script_manage/', '/timing_manage/', '/account/',
        '/history/', '/agent/',
        '/view_status/',
    ];

    var valueArr = ['批量重启', '批量改密',
        '执行脚本', '分发文件',
        '作业模板管理', '作业实例管理', '作业实例管理', '作业脚本管理', '定时调度管理', '执行账户管理',
        '作业执行历史', '查看agent状态',
        '查看系统状态',
    ];

    var tabArr = ['restart', 'modify_pwd',
        'script', 'send_file',
        'md_manage', 'example_manage', 'job_manage', 'script_manage', 'timing_manage', 'account',
        'history', 'agent',
        'view_status'
    ];

    $('.nav-list li a').each(function (i) {
        $(this).click(function () {
            if ($(this).hasClass("no-permission")) {
                return false;
            }

            var index = i + 1;

            if (i > -1) {
                index = i + 2;
            } 
            if (i > 4) {
                index = i + 3;
            } 
            if (i > 9) {
                index = i + 5;
            } 
            if (i > 11) {
                index = i + 6;
            } 
            if (i > 12) {
                index = i + 7;
            } 

            $('.nav-list li:eq(' + index + ')').addClass('active');

            $("#loading-panel").show().css({
                "z-index": 1000
            }).animate({
                opacity: "1"
            }, 100);

            if (urlArr[i] == '//') {
                return false;
            }

            // ajax load page
            if (urlArr[i] == '/script/') {
                $.ajax({
                    type: "GET",
                    url: urlArr[i],
                    data: {
                        done: 'ok'
                    },
                    dataType: 'json',
                    success: function (data) {
                        if ($('#li_' + tabArr[i]).length && $('#li_' + tabArr[i]).length > 0) {
                            $('#myTab a[aria-controls="' + tabArr[i] + '"]').tab('show');
                        } else {
                            $('#myTab').prepend('<li id="li_' + tabArr[i] + '" role="presentation" style="  position: relative;" ><i onclick="close_tab(this)" class="icon-remove mytab-close"></i><a href="#' + tabArr[i] + '" aria-controls="' + tabArr[i] + '" role="tab" data-toggle="tab" onclick="active_menu(this);" style="padding-right: 24px;"><label class="tab-ellipsis">' + valueArr[i] + '</label></a></li>');
                            $('#tabs>.tab-content').prepend('<div role="tabpanel" class="tab-pane show-already" id="' + tabArr[i] + '">' + data.html + '</div>');
                            $('#myTab a:first').tab('show');
                        }

                        show_tab_arrow();

                        $("#loading-panel").animate({
                            opacity: "0"
                        }, 200).hide().css({
                            "z-index": -999
                        });

                        $("#script").removeClass("show-already");
                    },
                    error: function (re, status) {}
                });
            } else {
                if ($('#li_' + tabArr[i]).length && $('#li_' + tabArr[i]).length > 0) {
                    $('#myTab a[aria-controls="' + tabArr[i] + '"]').tab('show');
                } else {
                    $('#myTab').prepend('<li id="li_' + tabArr[i] + '" role="presentation" style="  position: relative;" ><i onclick="close_tab(this)" class="icon-remove mytab-close"></i><a href="#' + tabArr[i] + '" aria-controls="' + tabArr[i] + '" role="tab" data-toggle="tab" onclick="active_menu(this);" style="padding-right: 24px;"><label class="tab-ellipsis">' + valueArr[i] + '</label></a></li>');

                    $('#tabs>.tab-content').prepend('<div role="tabpanel" class="tab-pane" id="' + tabArr[i] + '"></div>');
                    $('#' + tabArr[i]).load(urlArr[i]);
                    $('#myTab a:first').tab('show');
                }

                show_tab_arrow();

                $("#loading-panel").animate({
                    opacity: "0"
                }, 200).hide().css({
                    "z-index": -999
                });
            }
        });
    });
 
    $(".popovers").popover();

    $.fn.dataTableExt.oApi.fnReloadAjax = function (oSettings, sNewSource, fnCallback, bStandingRedraw) {
        if (typeof sNewSource != 'undefined' && sNewSource != null) {
            oSettings.sAjaxSource = sNewSource;
        }

        if (oSettings.oFeatures.bServerSide) {
            this.fnDraw();
            return;
        }

        this.oApi._fnProcessingDisplay(oSettings, true);
        var that = this;
        var iStart = oSettings._iDisplayStart;
        var aData = [];

        this.oApi._fnServerParams(oSettings, aData);

        oSettings.fnServerData.call(oSettings.oInstance, oSettings.sAjaxSource, aData, function(json) {

            that.oApi._fnClearTable(oSettings);

            var aData = (oSettings.sAjaxDataProp !== "") ?
                that.oApi._fnGetObjectDataFn(oSettings.sAjaxDataProp)(json) : json;

            for (var i = 0; i < aData.length; i++) {
                that.oApi._fnAddData(oSettings, aData[i]);
            }

            oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();

            if (typeof bStandingRedraw != 'undefined' && bStandingRedraw === true) {
                oSettings._iDisplayStart = iStart;
                that.fnDraw(false);
            } else {
                that.fnDraw();
            }

            that.oApi._fnProcessingDisplay(oSettings, false);

            if (typeof fnCallback == 'function' && fnCallback != null) {
                fnCallback(oSettings);
            }
        }, oSettings);
    }

    /*// 本地存储访客是否第一次访问
    var strModel = "startJobs";
    var storeDisplay = function() {
        var modelDisplay = 1;

        // 存储，IE6~IE7 cookie 其他浏览器HTML5本地存储
        if (window.localStorage) {
            localStorage.setItem(strModel, modelDisplay);
        } else {
            Cookie.write(strModel, modelDisplay);
        }
    };

    // 检测触发是否显示弹窗
    var strStoreDate = window.localStorage ? localStorage.getItem(strModel) : Cookie.read(strModel);

    if (strStoreDate == "1" || strStoreDate == undefined) {
        $('#startJobs').removeClass("hide");

        $('#startJobs').modal({
            show: true
        });  

        ani_start();
    }

    storeDisplay();*/

    // 导航隐藏
    $("#nav-hide-menu").bind("click", function() {
        $(this).toggleClass("on");

        $(".bar-side, .nav-header > span").toggleClass("slim-header");
        $(".bar-side, .nav-header > span > span").toggleClass("hide");

        $(".menu-lis > li > a").toggleClass("slim");

        $(".menu-lis > li > i").toggleClass("hide");

        $("#menu_ul .nav-header .icomoon").toggleClass("pull-right");

        $(".bggray .span2, .ujobs-logo").toggleClass("slim-left");

        $(".ujobs-logo img").toggleClass("slim-logo");

        $(".bggray .span10").toggleClass("slim-right");

        if ($(this).hasClass('on')) {
            $(".tips").tooltip();
        } else {
            $(".tips").tooltip('destroy');
        }
    });

    // 导航显示
    $(".nav-show-menu").click(function () {
        var wLogo = $(".ujobs-logo").width();

        $(".nav-show-menu").hide();

        $(".bggray").animate({
            "margin-left": "0%"
        }, 400, function () {
            $("#nav-hide-menu").show();
        });
        $(".span10").animate({
            "padding-left": "2.564102564102564%",
            "padding-right": "0%"
        });
    });


    // 右键菜单效果
    $("#myTab").on("contextmenu", "li:not('#li_help1')", function (e) {
        if (typeof e.preventDefault === "function") {
            e.preventDefault();
            e.stopPropagation();
        } else {
            e.returnValue = false;
            e.cancelBubble = true;
        }

        $(this).addClass("an").siblings("li").removeClass("an");

        var side_width = $("#menu_ul").width();
        var move_left = $(".bggray").css("margin-left");

        if (move_left == "0%" || move_left == "0px") {
            $("#menu-context").css({
                "left": e.clientX - side_width,
                "top": e.clientY - 65
            }).fadeIn();
        } else {
            $("#menu-context").css({
                "left": e.clientX,
                "top": e.clientY - 65
            }).fadeIn();
        }

        $(".close-tab1").bind("click", function () {
            $(".an i").trigger("click");
            show_tab_arrow();
        });

        $(".close-tab2").bind("click", function () {
            $(".an").siblings().find("i").trigger("click");
            show_tab_arrow();
        });

        $(".close-tab3").bind("click", function () {
            $("#myTab>li").find("i").trigger("click");

            show_tab_arrow();

            if ($("#loading-panel").length != 0) {
                $("#loading-panel").animate({
                    opacity: "0"
                }, 200).hide();
            }
        });
    });

    // 菜单隐藏
    $(document).bind("click", function (e) {
        $("#menu-context").hide();
        $("#myTab li.an").removeClass("an");

    });

    // 侧边栏宽度和logo对齐
    var wside = $("#menu_ul").width();

    $(".ujobs-logo").css("width", wside);

    $(window).resize(function () {
        var wside = $("#menu_ul").width();

        $(".ujobs-logo").css("width", wside);
    });

    // 新手引导效果
    $("#new_hand_step").on("click", function () {
        ani_start();
    });

    $(document).on("click", "#startJobs .close", function () {
        $(".step-show1 span").prop("class", "");
        $(".step-show1 span").prop("class", "");
    });

    // 查询栏显示隐藏
    $(document).on("click", ".caret-arrow-up", function () {
        $(this).parent().siblings().hide();
        $(this).removeClass("caret-arrow-up").addClass("caret-arrow-down");
    });

    $(document).on("click", ".caret-arrow-down", function () {
        $(this).parent().siblings().show();
        $(this).removeClass("caret-arrow-down").addClass("caret-arrow-up");
    });

    // 查询重置
    $(document).on("click", ".reset", function () {
        $(this).parents(".form-search").find(".controls input,.controls textarea").val('');

        $(this).parents(".form-search").find(".controls select").each(function () {
            $(this).find("option").eq(0).prop("selected", true);
        });
    });

    // 全选全不选 
    var example_checked_all = ".edit_checked_all";
    var example_checked_it = ".edit_checked_it";

    check_all(example_checked_all, example_checked_it);

    // 重置
    $(document).on("click", "#update_script_reset", function () {
        $(".md-search-txt").val('');
        return false;
    });

    // 全程设定及返回
    $(document).on("click", ".full-set", function () {
        var data = $(this).attr("data-msg");

        $(this).parents("." + data).addClass("hide").siblings(".full-set-wrap").removeClass("hide");
    });

    $(document).on("click", ".full-set-back", function () {
        var data = $(this).attr("data-msg");

        $(this).parents(".full-set-wrap").addClass("hide").siblings("." + data).removeClass("hide");
        return false;
    });

    // 增加步骤
    $(document).off("click", ".add_step_choose li a").on("click", ".add_step_choose li a", function () {
        var $this = $(this);
        var $parents = $this.parents(".edit-md-wrap");
        var $tbody = $parents.find(".edit_md_table tbody");

        $parents.find(".edit_md_table .dataTables_empty").parent().remove();

        var add_type = $this.text();
        var index = $tbody.find('tr').length;
        var add_type_value = $this.parent('li').attr("value");
        var template_id = $tbody.attr("template_id");

        $.ajax({
            type: 'POST',
            url: "/md_manage/template_step/add/",
            data: {
                'index': index,
                'type_value': add_type_value,
                'template_id': template_id
            },
            dataType: 'json',
            success: function (data) {
                if (data.status == 200) {
                    var step_id = data.result.step_id;

                    // 简化版
                    $tbody.append("<tr class='checknow' step_id=" + step_id + "><td><input value='" + step_id + "' class='jobview-checked-it-" + template_id + "' type='checkbox' checked></td><td></td><td><a href='javascript:void(0)' onclick='template_step_edit_v2(" + step_id + ");'>" + add_type + "</a></td><td>" + add_type + "</td><td><div class='btn-group'><a class='dropdown-toggle' data-toggle='dropdown' href='#'>增加步骤</a><ul class='dropdown-menu add-step-list'><li value='1'><a>执行脚本</a></li><li value='2'><a>分发文件</a></li><li value='3'><a>拉取文件</a></li><li value='4'><a>文本步骤</a></li></ul></div>&nbsp;&nbsp;<a href='javascript:void(0)' class='remove-step' step_id=" + step_id + ">删除</a></td></tr>");
                    sort_step($this);
                    if ($tbody.find(":checked").length == $tbody.find('tr').length) {
                        $parents.find("table thead :checkbox").prop("checked", true);
                    }
                } else {
                    jError('操作失败！');
                }
            },
        });

    });

    $(document).off("click", ".add-step-list li a").on("click", ".add-step-list li a", function () {

        var $this = $(this);
        var $parents = $this.parents(".edit-md-wrap");
        var $tbody = $parents.find(".edit_md_table tbody");

        $parents.find(".edit_md_table .dataTables_empty").parent().remove();

        var add_type = $this.text();
        var index = $this.parents('tr').prevAll().length + 1;
        var add_type_value = $this.parent('li').attr("value");
        var template_id = $tbody.attr("template_id");

        $.ajax({
            type: 'POST',
            url: "/md_manage/template_step/add/",
            data: {
                'index': index,
                'type_value': add_type_value,
                'template_id': template_id
            },
            dataType: 'json',
            success: function(data) {
                if (data.status == 200) {
                    var step_id = data.result.step_id;
                    
                    // 简化版
                    $this.parents('tr').after("<tr class='checknow' step_id=" + step_id + "><td><input value='" + step_id + "' class='jobview-checked-it-" + template_id + "' type='checkbox' checked></td><td></td><td><a href='javascript:void(0)' onclick='template_step_edit_v2(" + step_id + ");'>" + add_type + "</a></td><td>" + add_type + "</td><td><div class='btn-group'><a class='dropdown-toggle' data-toggle='dropdown' href='#'>增加步骤</a><ul class='dropdown-menu add-step-list'><li value='1'><a>执行脚本</a></li><li value='2'><a>分发文件</a></li><li value='3'><a>拉取文件</a></li><li value='4'><a>文本步骤</a></li></ul></div>&nbsp;&nbsp;<a href='javascript:void(0)' class='remove-step' step_id=" + step_id + ">删除</a></td></tr>");
                    sort_step($this);
                } else {
                    jError('操作失败！');
                }
            },
        });
    });

    // 删除步骤
    $(document).off("click", ".remove-step").on("click", ".remove-step", function () {
        var $this = $(this);

        if (confirm("是否真的要删除该步骤？") == true) {
            var template_step_id = $this.attr("step_id");

            $.ajax({
                url: '/md_manage/template_step/delete/' + template_step_id + '/',
                dataType: 'json',
                success: function (data) {
                    if (data.status == 200) {

                        //简化版
                        var $parents = $this.parents(".edit-md-wrap");

                        $this.parents("tr").remove();
                        $parents.find(".edit_md_table tbody tr").each(function() {
                            var $index = $(this).index() + 1;
                            $(this).find('td').eq(1).html("第" + $index + "步");
                        });

                        jSuccess(data.result.msg);
                    } else if (data.status == 500) {
                        jError(data.result.msg);
                    }
                },
                error: function (re, status) {
                    jError("出错了");
                }
            });
        } else {
            jNotify("操作已取消");
        }

    });

    // jstree 选择授权用户
    $(document).off("click", ".select-power").on("click", ".select-power", function () {
        $.jstree.destroy();

        var data_type = $(this).attr("data-auth-type"),
            data_msg = $(this).attr("data-msg"),
            $parents = $(".edit-" + data_msg + "-wrap"),
            checked_box = $parents.find("." + data_msg + "_checked_it:checked"),
            $model = $parents.siblings(".set-model"),
            tree_id = $model.find(".ujobs-power-tree"),
            checked_arr = [];

        for (var i = 0; i < checked_box.length; i++) {
            checked_arr.push(checked_box.eq(i).prop("value"));
        }

        nodeid = '';
        tree_id.on('changed.jstree', function (e, data) {
            nodeid = data.selected;
        }).jstree({
            "plugins": ["checkbox"],
            'core': {
                "themes": {
                    "theme": "classic",
                    "dots": true,
                    "icons": true
                },
                'dataType': 'json',
                'data': {
                    'url': '/usual/ajax_get_auth_emp_list_returns/',
                    'data': function (node) {
                        return {
                            'nodeid': node.id,
                            'auth_type': data_type,
                            'obj_list': checked_arr
                        };
                    }
                }
            }
        });
    });

    // 确认授权
    $(document).off("click", ".power-comfirm").on("click", ".power-comfirm", function () {
        var data_msg = $(this).attr("data-msg"),
            $parents = $(this).parents(".set-model").siblings(".edit-" + data_msg + "-wrap"),
            $servers_btn = $parents.find(".select-power"),
            power_type = $servers_btn.attr("data-auth-type"),
            checked_box = $parents.find("." + data_msg + "_checked_it:checked"),
            checked_arr = [];

        for (var i = 0; i < checked_box.length; i++) {
            checked_arr.push(checked_box.eq(i).prop("value"));
        }

        $servers_btn.prop("disabled", true);

        $.ajax({
            type: "post",
            url: '/usual/update_auth/',
            data: {
                "obj_list": checked_arr,
                "user_list": nodeid,
                "auth_type": power_type
            },
            dataType: "json",
            success: function (data) {
                if (data.status == 200) {
                    jSuccess(data.result.msg);
                    $servers_btn.prop("disabled", false);
                } else {
                    jError(data.result.msg);
                    $servers_btn.prop("disabled", false);
                }
            },
            error: function (data) {
                jError(data.result.msg);
                $servers_btn.prop("disabled", false);
            }
        });
    });

    // jstree 选择目标机器
    var nodeid;

    $(document).on("click", ".select-servers", function () {
        var wrap_name = '.' + $(this).attr('data-msg'),
            $wrap = $(this).parents(wrap_name),
            $parents = $wrap.siblings(".set-model"),
            tree_id = $parents.find(".ujobs-cmdb-tree");

        tree_id.on('changed.jstree', function (e, data) {
            nodeid = data.selected;
        }).jstree({
            "plugins": ["checkbox"],
            'core': {
                "themes": {
                    "theme": "classic",
                    "dots": true,
                    "icons": true
                },
                'dataType': 'json',
                'data': {
                    'url': '/usual/ajax_get_cmdb_node_returns/',
                    'data': function (node) {
                        return {
                            'nodeid': node.id
                        };
                    }
                }
            }
        });

        // 条件选择
        var fliter_tab = $parents.find(".fliter-tab"),
            set = $parents.find(".set-fliter"),
            module = $parents.find(".module-fliter"),
            product = $parents.find(".product-fliter"),
            clear_fliter = $parents.find(".clear-fliter"),
            set_value = $parents.find(".set-value"),
            module_value = $parents.find(".module-value"),
            add_fliter = $parents.find(".add-fliter"),
            set_arr = [],
            module_arr = [];

        fliter_tab.off("click").on("click", function () {
            product_from(product, 'sss');
        });

        set.on("focus", function () {
            if (!product.val()) {
                jNotify("请先选择所属产品！");
                $(this).blur();
            }
        });

        module.on("focus", function () {
            if (!product.val()) {
                jNotify("请先选择所属产品！");
                $(this).blur();
            }
        });

        // set 模糊匹配
        set.autocomplete({
            source: function (request, response) {
                var product_id = product.find("option:selected").attr("data-id");
                $.ajax({
                    type: "POST",
                    url: "/usual/ajax_get_cmdb_set_or_module/",
                    dataType: "json",
                    data: {
                        'productid': product_id,
                        'type': 'set',
                        'value': request.term
                    },
                    success: function (data) {
                        response($.map(data, function(item) {
                            item.unshift("ALL");
                            return item;
                        }));
                    }
                });
            },
            select: function (event, ui) {
                var value = ui.item.value;
                if (value == 'ALL') {
                    set_arr = ["ALL"];
                    set_value.val("ALL");
                } else if ($.inArray(value, set_arr) == -1 && set_value.val() != "ALL") {
                    set_arr.push(value);
                    set_value.val(set_arr);
                } else if ($.inArray(value, set_arr) == -1 && set_value.val() == "ALL") {
                    set_arr = [];
                    set_arr.push(value);
                    set_value.val(set_arr);
                }
            },
            change: function (event, ui) {
                if (!$(this).val() && !set_value.val()) {
                    $(this).val('');
                }
            }
        });

        // module模糊匹配
        module.autocomplete({
            source: function (request, response) {
                var product_id = product.find("option:selected").attr("data-id");

                $.ajax({
                    type: "POST",
                    url: "/usual/ajax_get_cmdb_set_or_module/",
                    dataType: "json",
                    data: {
                        'productid': product_id,
                        'type': 'module',
                        'value': request.term
                    },
                    success: function (data) {
                        response($.map(data, function(item) {
                            item.unshift("ALL");
                            return item;
                        }));
                    }
                });
            },
            select: function (event, ui) {
                var value2 = ui.item.value;

                if (value2 == 'ALL') {
                    module_arr = ["ALL"];
                    module_value.val("ALL");
                } else if ($.inArray(value2, module_arr) == -1 && module_value.val() != "ALL") {
                    module_arr.push(value2);
                    module_value.val(module_arr);
                } else if ($.inArray(value2, module_arr) == -1 && module_value.val() == "ALL") {
                    module_arr = [];
                    module_arr.push(value2);
                    module_value.val(module_arr);
                }
            },
            change: function (event, ui) {
                if (!$(this).val() && !module_value.val()) {
                    $(this).val('');
                }
            }
        });

        // 清空
        clear_fliter.off("click").on("click", function () {
            if ($(this).attr("data-msg") == "set") {
                set_arr = [];
                set_value.val('');
                set.val('');
            } else {
                module_arr = [];
                module_value.val('');
                module.val('');
            }
        });

        // 添加
        add_fliter.off("click").on("click", function () {
            if (!product.val() || !set_value.val() || !module_value.val()) {
                jNotify("存在未完成的输入项，请检查！");
                return false;
            }

            var product_id = product.find("option:selected").attr("data-id"),
                data_msg = $(this).attr("data-msg"),
                $servers_btn = $wrap.find(".select-servers"),
                $ip_show = $wrap.find(".edit-" + data_msg + "-ip-result"),
                $ip_hide = $wrap.find(".edit-" + data_msg + "-ip-hide"),
                $ip_add = $wrap.find(".add-btn-status"),
                $save_set = $wrap.find(".edit-" + data_msg + "-save"),
                $ip_wrap = $wrap.find(".edit-" + data_msg + "-ip-wrap");

            $.ajax({
                type: "POST",
                url: "/usual/ajax_get_cmdb_ip_by_expression_v2/",
                dataType: "json",
                data: {
                    'productid': product_id,
                    'set': set_value.val(),
                    'module': module_value.val()
                },
                success: function (data) {
                    if (!data) {
                        jNotify("所选信息下无ip数据！");
                    } else {
                        $ip_show.parent().removeClass("hide");
                        $ip_show.empty();
                        vaild_ipfree_v2(data, $ip_show);

                        var total = $ip_show.find(".ipconfig").length;
                        var num = total - $ip_show.find(".diswork").length;

                        data.total = total;
                        data.num = num;
                        $ip_hide.val(JSON.stringify(data));
                        $ip_wrap.find("b").html("涉及服务器[" + data.total + "]台，仅[" + data.num + "]台支持操作");
                        $ip_add.removeClass("disabled");
                        $save_set.removeClass("disabled");
                        $servers_btn.button('complete').html("<i class='icon-th-list'></i>选择目标机器 ");

                    }
                },
                error: function () {
                    jError("获取数据失败！");
                }
            })
        });
    });

    //CMDB获取ip
    $(document).off("click", ".add-servers-ip").on("click", ".add-servers-ip", function () {
        var data_msg = $(this).attr("data-msg");
        var $parents = $(this).parents(".set-model").siblings(".edit-" + data_msg + "-wrap");
        var $servers_btn = $parents.find(".select-servers");
        var $ip_show = $parents.find(".edit-" + data_msg + "-ip-result");
        var $ip_hide = $parents.find(".edit-" + data_msg + "-ip-hide");
        var $ip_add = $parents.find(".add-btn-status");
        var $save_set = $parents.find(".edit-" + data_msg + "-save");
        var $ip_wrap = $parents.find(".edit-" + data_msg + "-ip-wrap");

        $ip_show.parent().removeClass("hide");
        $ip_show.empty();

        $.ajax({
            type: "post",
            url: '/usual/ajax_get_cmdb_subnode_returns/',
            data: {
                "nodeid": nodeid
            },
            dataType: "json",
            success: function (data) {
                if (data == '') {
                    jNotify("所选机器下没有ip信息");
                    return false;
                } else {
                    $ip_hide.val('');

                    var hidetxt = $ip_hide.val();
                    var ip_arr = data.split(',');

                    for (var i = 0; i < ip_arr.length; i++) {
                        $ip_show.append("<li><i class='ipconfig'>" + ip_arr[i] + "</i><i i class='loading'><img width='20px' src='/static/assets/img/loading.gif'></i></li>");
                    }

                    $ip_add.addClass("disabled");
                    $save_set.addClass("disabled");
                    $servers_btn.button('loading');

                    // IP验证
                    $.ajax({
                        type: 'POST',
                        url: '/ajax_cmdb_valid_v2/',
                        data: {
                            'iptxt': data,
                            'hidetxt': hidetxt
                        },
                        dataType: 'json',
                        error: function (XMLHttpRequest) {
                            jError(XMLHttpRequest.responseText);

                            $ip_add.removeClass("disabled");
                            $save_set.removeClass("disabled");
                            $servers_btn.button('complete').html("<i class='icon-th-list'></i>选择目标机器 ");
                            $ip_wrap.empty();

                            return false;
                        },
                        success: function (result) {
                            $ip_show.parent().removeClass("hide");
                            $ip_hide.val(result.ip_dict);

                            var res = $.parseJSON(result.ip_dict);
                            
                            $ip_wrap.find("b").html("涉及服务器[" + res.total + "]台，仅[" + res.num + "]台支持操作");
                            $ip_show.empty();

                            vaild_ipfree_v2(res, $ip_show);

                            $ip_add.removeClass("disabled");
                            $save_set.removeClass("disabled");
                            $servers_btn.button('complete').html("<i class='icon-th-list'></i>选择目标机器 ");
                        }
                    });
                    return true;
                }
            },
            error: function () {
                jError('请求失败！选择目标机器失败！');
            }
        });
    });

    // 编辑脚本复选框显示隐藏
    $(document).on("ifClicked", ".check-toggle", function () {
        var $parents = $(this).parents(".edit-script-wrap");
        var toggle_data = $(this).attr("data-msg");
        var toggle_box = ".check-toggle-" + toggle_data;

        check_toggle($(this), $parents, toggle_box);
    });

    $(document).on("ifClicked", ".check-toggle3", function () {
        var $parents = $(this).parents(".edit-sendfile-wrap");
        var toggle_box = ".check-toggle-box3";

        check_toggle($(this), $parents, toggle_box);
    });

    // 编辑分发文件单选框显示隐藏
    $(document).on("ifClicked", ".edit-sendfile-btn", function () {
        var $parents = $(this).parents(".edit-sendfile-wrap");
        var data_msg = $(this).attr("data-msg");
        var data_msg2 = $(this).attr("data-msg2");
        var data_msg3 = $(this).attr("data-msg3");

        $parents.find('.edit-sendfile-' + data_msg).removeClass("hide");
        $parents.find('.edit-sendfile-' + data_msg2).addClass("hide");
        $parents.find('.edit-sendfile-' + data_msg3).addClass("hide");
    });

    // 分发文件单选框显示隐藏
    $(document).on("ifChecked", "#send_file_location_remote", function () {
        $("#local-doc, #url-doc").addClass("hide");
        $("#far-doc").removeClass("hide");
    });

    $(document).on("ifChecked", "#send_file_location_local", function () {
        $("#local-doc").removeClass("hide");
        $("#far-doc, #url-doc").addClass("hide");
    });

    $(document).on("ifChecked", "#send_file_location_url", function () {
        $("#url-doc").removeClass("hide");
        $("#far-doc, #local-doc").addClass("hide");
    });

    // 编辑拉取文件复选框显示隐藏
    $(document).on("ifClicked", ".check-toggle4", function () {
        var $parents = $(this).parents(".edit-pullfile-wrap");
        var toggle_box = ".check-toggle-box4";

        check_toggle($(this), $parents, toggle_box);
    });

    // 浏览文件
    $(document).on("click", ".p-filefind", function () {
        var data = $(this).attr("data-msg");
        var $parents = $(this).parents(".edit-" + data + "-wrap");
        var obj_upload = $parents.find(".edit-" + data + "-upField");
        var textfield = $parents.find(".edit-" + data + "-docfield");

        flie_upload2(obj_upload, textfield);
    });

    // 执行脚本上传类型选择
    $(document).on("ifChecked", ".localscript", function () {
        $(this).parents(".row-fluid").find(".local-find").removeClass("hide");
    });

    $(document).on("ifChecked", ".handscript", function () {
        $(this).parents(".row-fluid").find(".local-find").addClass("hide");
    });

    // 定时规则显示隐藏
    $(document).on("ifClicked", ".rule-show", function() {
        var $parents = $(this).parents(".modify-timing-modal");
        var toggle_box = '.rule-txt';

        check_toggle($(this), $parents, toggle_box);
    });

    var onswitch = 1; //开关--0为开启密码输入,1为关闭密码输入;

    // ip添加
    $(document).on("click", '.ip-add-btn', function () {
        var data_msg = $(this).attr('data-msg');
        var $parents = $(this).parents('.edit-' + data_msg + '-wrap');
        var $ip_hide = $parents.find('.edit-' + data_msg + '-ip-hide');
        var $ip_area = $parents.find('.edit-' + data_msg + '-ip-area');
        var $ip_show = $parents.find('.edit-' + data_msg + '-ip-result');
        var $ip_add = $parents.find('.ip-add-btn');
        var $save_set = $parents.find('.edit-' + data_msg + '-save');
        var $scroll_wrap = $('.edit-' + data_msg + '-ip-wrap b');

        $ip_hide.val('');

        if (onswitch == 1) {
            // 无需输入密码
            add_ipfree($ip_area, $ip_hide, $ip_show, $ip_add, $save_set, $scroll_wrap, data_msg);
        } else {
            if (data_msg == 'pwd') {
                // 需要输入密码
                var url = '/ajax_pwd_valid_v2/0/';

                add_ip($ip_area, $ip_hide, $ip_show, $ip_add, $save_set, $scroll_wrap, url);
            } else {
                // 需要输入密码
                add_ip($ip_area, $ip_hide, $ip_show, $ip_add, $save_set, $scroll_wrap, url);
            }
        }

    });

    // 编辑分发文件 ip添加
    $(document).on("click", '.ip-add-btn2', function () {
        var data_msg = $(this).attr('data-msg');
        var $parents = $(this).parents('.edit-' + data_msg + '-wrap');
        var $ip_hide = $parents.find('.edit-' + data_msg + '-ip-hide');
        var $ip_area = $parents.find('.edit-' + data_msg + '-ip-area');
        var $ip_show = $parents.find('.edit-' + data_msg + '-ip-result');
        var $ip_add = $parents.find('.ip-add-btn2');
        var $save_set = $parents.find('.edit-' + data_msg + '-save');
        var $scroll_wrap = $('.edit-' + data_msg + '-ip-wrap b');

        $ip_hide.val('');

        if (onswitch == 1) {
            // 无需输入密码
            add_ipfree($ip_area, $ip_hide, $ip_show, $ip_add, $save_set, $scroll_wrap);
        } else {
            // 需要输入密码
            add_ip2($ip_area, $ip_hide, $ip_show, $ip_add, $save_set, $scroll_wrap);
        }
    });

    // 删除列表ip及隐藏框ip
    $(document).on("click", '.ip-style span', function () {
        var data_msg = $(this).parents(".ip-style").attr("data-msg");
        var $parents = $(this).parents('.edit-' + data_msg + '-wrap');
        var ip_config = $(this).siblings(".ipconfig").prop("id");
        var ip_hide = $parents.find('.edit-' + data_msg + '-ip-hide');

        delete_ip_hide(ip_hide, $(this), $('.edit-' + data_msg + '-ip-wrap b'), ip_config);
    });

    // hash检测
    $(document).on("change", ".p-upField", function () {
        var data = $(this).attr("data-msg");
        var $parents = $(this).parents(".edit-" + data + "-wrap");
        var find = $parents.find(".edit-" + data + "-find");
        var upload = $parents.find(".edit-" + data + "-upload");
        var hash = $parents.find(".edit-" + data + "-hash");
        var upField = $parents.find(".edit-" + data + "-upField");

        hash_get(find, upload, hash, upField);
    });

    // 导入文件
    $(document).on("click", ".edit-sendfile-upload", function () {
        var size = $(this).attr("data-size");
        var data = $(this).attr("data-msg");
        var $parents = $(this).parents(".edit-" + data + "-wrap");
        var docfield = $parents.find(".edit-" + data + "-docfield");
        var upfield = $parents.find(".edit-" + data + "-upField");
        var hash = $parents.find(".edit-" + data + "-hash");
        var upload_btn = $parents.find(".edit-sendfile-upload");
        var ip_show = $parents.find(".edit-" + data + "-ip");
        var records = $parents.find(".edit_" + data + "_record");
        var file_form = $parents.find(".edit-" + data + "-form");
        var file_url = $("#nav-hide-menu").attr("data-url");

        load_file($parents, docfield, upfield, hash, upload_btn, ip_show, records, file_form, file_url, size);
    });

    //添加待分发文件
    $(document).on("click", ".p-addfile", function () {
        var data = $(this).attr("data-msg");
        var $parents = $(this).parents(".edit-" + data + "-wrap");
        var ipserver = $parents.find(".edit-" + data + "-ipserver");
        var hidelists = $parents.find(".edit-" + data + "-hidelists");
        var filelists = $parents.find(".edit-" + data + "-filelists");
        var sendfile_btn = $parents.find(".p-addfile");
        var file_show = $parents.find(".edit-" + data + "-ip");
        var server_account = $parents.find(".edit-" + data + "-account option:selected");

        add_filelists(ipserver, hidelists, filelists, sendfile_btn, file_show, server_account);
    });

    // 添加待分发url文件
    $(document).on("click", ".p-addurl", function () {
        var data = $(this).attr("data-msg");
        var $parents = $(this).parents(".edit-" + data + "-wrap");
        var hidelists = $parents.find(".edit-" + data + "-hideurls");
        var filelists = $parents.find(".edit-" + data + "-fileurls");
        var sendfile_btn = $parents.find(".p-addurl");
        var file_show = $parents.find(".edit-" + data + "-ip");
        var server_account = $parents.find(".edit-" + data + "-account option:selected");

        add_fileurls(hidelists, filelists, sendfile_btn, file_show, server_account);
    })

    // 添加待拉取文件
    $(document).off("click", ".edit-pullfile-addfile").on("click", ".edit-pullfile-addfile", function () {
        var $parents = $(this).parents(".edit-pullfile-wrap");
        var file_lists = $parents.find(".edit-pullfile-filelists");
        var file_li = $parents.find(".edit-pullfile-list");
        var file_txt = file_lists.val().trim();
        var add_btn = $parents.find(".edit-pullfile-addfile");

        if (!file_txt || file_txt == ' ') {
            jNotify('请输入文件名！');
            return false;
        }

        var file_arr = file_txt.split('\n');
        var file_length = file_arr.length;
        var new_arr = [];

        for (var i = 0; i < file_length; i++) {
            if (file_arr[i] != ' ' && file_arr[i] != '') {
                new_arr.push(file_arr[i]);
            }
        }

        var new_file_length = new_arr.length;
        var file = '';

        for (var i = 0; i < new_file_length; i++) {
            file += "<li class='clearfix list2'>拉取文件：<i class='file-road'>" + new_arr[i] + "</i><i class='ipconfig'></i><i class='server-account'></i><span onclick='del_file(this)'>删除</span></li>";
        }

        file_li.append(file);
        file_lists.val('');
    });

    // 分发文件  删除隐藏域
    $(document).on("click", ".delete2", function () {
        var $parents = $(this).parents(".file-box");
        var msg = $parents.attr('data-msg');
        var send_file_hide = $parents.find(".edit-" + msg +"-hidelists");
        var e = $(this);

        del_filelists(e, send_file_hide);
    });

    // 分发文件 删除隐藏域文件id
    $(document).on("click", ".delete1", function () {
        var $parents = $(this).parents(".file-box");
        var msg = $parents.attr('data-msg');
        var record = $parents.find(".edit_" + msg + "_record");
        var e = $(this);

        del_filelists2(e, record);
    });

    // 分发文件  删除url隐藏域
    $(document).on("click", ".delete3", function() {
        var $parents = $(this).parents(".file-box");
        var msg = $parents.attr('data-msg');
        var send_file_hide = $parents.find(".edit-" + msg + "-hideurls");
        var e = $(this);

        del_fileurls(e, send_file_hide);
    });

    // 超时最大值限定
    $(document).on("keyup", ".ujobs_timeout", function () {
        if ($(this).val() >= 259200) {
            $(this).val("259200");
        }
    });

    // logo效果（webkit下有效）
    $(".ujobs-logo img").mouseover(function () {
        var b = 0,
            c = $(this),
            d = setInterval(function() {
                if (b > parseInt(c.width() + 50)) {
                    clearInterval(d);
                }
                c.css({
                    "-webkit-mask": "-webkit-gradient(radial, 88 53," + b + ", 88 53, " + (b + 15) + ", from(rgba(255, 255, 255,0.9)), color-stop(0.5, rgba(255, 255, 255, 0.2)), to(rgba(255, 255, 255,1)))"
                });
                b++;
            }, 0);
    });

    // 翻页、排序去除checked
    $(document).on("click", ".paginate_button,.paginate_active,.sorting,.sorting_asc,.sorting_desc", function () {
        var $parents = $(this).parents(".dataTables_wrapper");
        var checkbox = $parents.find("tbody input:checkbox");
        var check_all = $parents.find("thead input:checkbox");

        checkbox.prop("checked", false);
        check_all.prop("checked", false);
    });

    // 高级选项切换(执行脚本)
    $(document).on("ifClicked", "#more-choose", function () {
        if ($("#more-choose").prop('checked') == false) {
            $('#timeout').css('display', 'block');
            $('#parameter').css('display', 'block');
        } else {
            $('#timeout').css('display', 'none');
            $('#parameter').css('display', 'none');
            $("#script_once_timeout").val('');
            $("#script_once_parameter").val('');
        }
    });

    // 更新详情跳转
    $(document).on("click", "#view_update", function () {
        $('#myTab a[aria-controls="update"]').tab('show');
    });

    // 高度自适应
    (function () {
        var h = $(window).height();

        $(".tab-content.tab-main").outerHeight(h - 153);

        $(window).resize(function() {
            var h = $(window).height();

            $(".tab-content.tab-main").outerHeight(h - 153);
        });
    })();

    //===============第二版简化版==================

    // 新建执行账户
    $(document).on("click", "#menu_li_account_add", function () {
        $.ajax({
            type: 'GET',
            url: '/account/add/',
            data: {},
            success: function (data) {
                var tabArr = 'account_add';
                var valueArr = '新建执行账户';
                var dataArr = data;
                tab_href(tabArr, valueArr, dataArr);
            },
            error: function () {
                jError('出错了');
            }
        });
    });

    // 跳转至全程设定
    $(document).on("click", "#goto_fullset", function () {
        var $parents = $(this).parents(".modal").siblings('.row-fluid'),
            btn = $parents.find('.full-set');

        btn.trigger('click');
    });

});
