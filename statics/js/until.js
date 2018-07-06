/*--------------------------------
 * Author: luozh@snail.com
 * Date: 2015-08-03
 * Usage:
 *--------------------------------
 */

// 弹窗内部动画
var ani_start = function () {
    $(".step-show1 span").addClass("zoomIn").addClass("animated");

    function animate1() {
        var dtd = $.Deferred();

        $("#dowebok").delay(800).animate({
            "opacity": 1
        }, 500, function() {
            dtd.resolve();
        });
        return dtd;
    }

    function animate2() {
        var dtd = $.Deferred();

        $(".left-text").animate({
            "opacity": 1
        }, 500, function() {
            dtd.resolve();
        });
        return dtd;
    }

    function animate3() {
        var dtd = $.Deferred();
        $("#move_box").animate({
            "opacity": 1
        }, 500, function() {
            dtd.resolve();
        });
        return dtd;
    }

    var anim = animate1();

    anim.then(function() {
        return animate2();
    }).then(function() {
        return animate3();
    });
};

// 按钮样式 
function icheck(obj) {
    obj.iCheck({
        checkboxClass: 'icheckbox_minimal-grey',
        radioClass: 'iradio_minimal-grey',
        increaseArea: '20%' // optional
    });
}

// 激活标签
function active_menu(that) {
    $('#menu_ul li').removeClass('active');
    var li_id = $(that).parent().attr('id');
    $('#menu_' + li_id).addClass('active');
}

// 显示收缩按钮
function show_tab_arrow() {
    var tab_length = $("#myTab li").length;
    var tab_width = 0;
    var ul_width = $("#myTab").width();

    for (var j = 0; j < tab_length; j++) {
        tab_width += $("#myTab li").eq(j).width();
    }
    if (tab_width > ul_width) {
        $(".tab-arrow").removeClass("hide");
    } else {
        $(".tab-arrow").addClass("hide");
        $("#myTab").css("height", "47px");
        $(".tab-arrow").find("i").removeClass("icon-arrow-up").addClass("icon-arrow-down");
    }
}

// 关闭标签
function close_tab(that) {
    var li = $(that).parent();
    var tab_name = $(that).next().attr("aria-controls");
    var li_active = $('#myTab li.active');
    var li_id = li_active.attr('id');

    li.remove();
    $('#' + tab_name).remove();

    if (li_id == 'li_' + tab_name) {
        $('#menu_ul li').removeClass('active');
        var li_last = $('#myTab a:first');
        if (li_last) {
            li_last.tab('show');
            var last_id = li_last.parent().attr('id');
            $('#menu_' + last_id).addClass('active');
        }
    }

    show_tab_arrow();
}

// 添加执行账户
function ajax_add_account(obj) {
    var modal = $(obj).parents(".modal");

    $.ajax({
        type: 'POST',
        url: '/account/ajax_add_account/',
        data: $("#ajaxaccountform").serialize(),
        dataType: 'json',
        success: function (msg) {
            modal.empty();
            modal.html(msg.html);
            if (msg.result == 1) {
                jSuccess('保存账户成功！');
                modal.modal("hide");
            } else {
                jError("保存账户失败");
            }
        },
        error: function () {
            jError('保存账户错误！');
        }
    });
    return true;
}

// codeMirror
function codeMirror(code_name, textarea, select, textarea2, textarea3, code_style, type1, type2, type4) {

    //选择主题
    select.change(function () {
        var theme = select.val();
        code_name.setOption("theme", theme);
    });

    select.trigger("change");

    //选择代码风格
    var txt1 = textarea.val();
    var txt2 = textarea3.val();
    var txt3 = textarea2.val();
    var type_style1 = type1;
    var type_style2 = type2;
    var type_style4 = type4;

    code_style.on("ifChecked", function () {
        var txt = code_name.getValue();
        var lang = $(this).prop("id");

        if (lang == type_style1) {
            code_name.setOption("mode", "shell");
            code_name.setValue(txt1);
        } else if (lang == type_style2) {
            code_name.setOption("mode", "perl");
            code_name.setValue(txt2);
        } else if (lang == type_style4) {
            code_name.setOption("mode", "python");
            code_name.setValue('');
        } else {
            code_name.setOption("mode", "python");
            code_name.setValue(txt3);
        }

    });
}

// codeMirror2
function codeMirror2(code_name, textarea, select) {
    var code_name = CodeMirror.fromTextArea(textarea[0], {
        lineNumbers: true,
        mode: "shell",
        lineWrapping: true,
    });

    // 选择主题
    select.change(function () {
        var theme = select.val();

        code_name.setOption("theme", theme);
    });

    select.trigger("change");
}

// 文件上传
function flie_upload2(obj_upload, textfield) {
    obj_upload.trigger('click');
    textfield.val(obj_upload.val());

    obj_upload.change(function () {
        textfield.val(obj_upload.val());
    });
}

// 导入文件
function load_file($parents, docfield, upfield, hash, upload_btn, ip_show, records, file_form, file_url, size) {
    var file = docfield.val();

    if (!file) {
        jNotify('请选择上传文件!');
        return false;
    }
    if (!check_size(upfield, size)) {
        return false;
    }

    var upfile = upfield.get(0).files[0];
    var md5sum = hash.val();

    $.ajax({
        url: '/files/file_exists/',
        type: 'POST',
        dataType: "json",
        data: {
            md5sum: md5sum,
            size: upfile.size,
            file_name: upfile.name,
        },
        success: function (data) {
            if (data.status == 200) {
                if (data.result.existed === true) {
                    upload_btn.button('complete').html("<i class='icon-arrow-up'></i>导入");
                    ip_show.parent().removeClass("hide");
                    ip_show.append('<li>本地文件：<i style="font-style:normal" title=' + file + '>' + file + '</i><i class="file-id" style="display:none;">' + data.result.record_id + '</i><span class="delete1">删除</span></li>');
                    
                    docfield.val("");
                    upfield.val("");
                    records.val(records.val() + $parents.find(".file-id").last().text() + ' ');
                    jSuccess('文件上传成功！');
                } else {
                    var formData = new FormData(file_form[0]);

                    upload_btn.button('loading');
                    $.ajax({
                        url: file_url,
                        type: 'POST',
                        dataType: "json",
                        data: formData,
                        success: function (data) {
                            upload_btn.button('complete').html("<i class='icon-arrow-up'></i>导入");

                            if (data.status == 200) {
                                ip_show.parent().removeClass("hide");
                                ip_show.append('<li>本地文件：<i style="font-style:normal" title=' + file + '>' + file + '</i><i class="file-id" style="display:none;">' + data.result.record_id + '</i><span class="delete1">删除</span></li>');
                                docfield.val("");
                                upfield.val("");
                                records.val(records.val() + $parents.find(".file-id").last().text() + ' ');
                                jSuccess('文件上传成功！');
                            } else {
                                jNotify(data.result.msg);
                            }

                        },
                        error: function () {
                            upload_btn.button('complete').html("<i class='icon-arrow-up'></i>导入");
                            jError('文件上传出错，请重试！');
                        },
                        cache: false,
                        contentType: false,
                        processData: false
                    });
                }
            } else {
                jNotify(data.result.msg);
            }
        },
        error: function () {
            jError('文件检查出错');
        },
        cache: false,
    });
}

// 检测文件大小
function check_size(upField, size) {
    var file = upField.get(0).files[0];

    if (file) {
        var fileSize = 0;
        if (file.size > 1024 * 1024 * size) {
            jError("文件大小不能大于100M");
            return false;
        } else if (file.size < 0) {
            jError("文件大小不能为0");
            return false;
        }
    } else {
        jError("请选择上传文件");
        return false;
    }
    return true;
}

// hash检测
function hash_get(find, upload, hash, upField) {
    if (!check_size(upField)) {
        return false;
    }

    find.button('loading');
    upload.addClass("disabled");

    var fileReader = new FileReader(),
        box = hash;

    blobSlice = File.prototype.mozSlice || File.prototype.webkitSlice || File.prototype.slice, file = upField.get(0).files[0], chunkSize = 2097152,

    chunks = Math.ceil(file.size / chunkSize),currentChunk = 0,spark = new SparkMD5();

    fileReader.onload = function (e) {
        /*console.log("read chunk nr", currentChunk + 1, "of", chunks);*/
        spark.appendBinary(e.target.result);

        currentChunk++;

        if (currentChunk < chunks) {
            loadNext();
        } else {
            /*console.log("finished loading");*/
            var md5 = spark.end();

            box.val(md5);
            /*console.info("computed hash", md5);*/
            find.button('complete').html("<i class='icon-folder-open'></i>浏览...");
            upload.removeClass("disabled");
        }
    };

    function loadNext() {
        var start = currentChunk * chunkSize,
            end = start + chunkSize >= file.size ? file.size : start + chunkSize;

        fileReader.readAsBinaryString(blobSlice.call(file, start, end));
    }

    loadNext();
}

// 判断是否存在同名文件
function isRepeat(arr) {
   var hash = {};
   
   for (var i in arr) {
       if (hash[arr[i]]) {
           return true;
       }

       // 不存在该元素，则赋值为true，可以赋任意值，相应的修改if判断条件即可
       hash[arr[i]] = true;
    }
   return false;
}

// 添加带分发url文件
function add_fileurls(hidelists, filelists, sendfile_btn, file_show, server_account) {
    var hidetxt = hidelists.val().trim();
    var file_road = filelists.val().trim().split('\n');
    var file_road_length = file_road.length;

    if (!filelists.val().trim()) {
        jNotify('请填写分发路径！');
        filelists.focus();
        return false;
    }

    file_show.parent().removeClass("hide");
    hidelists.val('');

    file_show.find(".list3").remove();

    var file_road_new = [];
    var file_json = [];

    // 判断隐藏域是否为空
    if (hidelists.val() === '') {
        var file_hide_json = {
            "remote": []
        };
    } else {
        var file_hide_json = $.parseJSON(hidelists.val());
    }

    // 删除空行
    for (var i = 0; i < file_road_length; i++) {
        file_road[i] === '' ? file_road.splice($.inArray(file_road[i], file_road), 1) : file_road_new.push(file_road[i]);
    }

    // 是否重名
    var fileArr = [];

    file_road_new.forEach(function(e, i) {
        var pathArr = e.replace('\\', '/').split('/');

        fileArr.push(pathArr[pathArr.length - 1]);
    });

    if (isRepeat(fileArr)) {
        jNotify('存在重名文件，请检查！');

        return false;
    }

    // 循环插入字典
    for (var j = 0; j < file_road_new.length; j++) {
        file_show.append('<li class="clearfix list3">url文件：<i class="file-road" title=' + file_road_new[j] + '>' + file_road_new[j] + '</i><i class="server-account">' + server_account.text() + '</i><span class="delete3">删除</span></li>');
        
        var obj = {
            'name': file_road_new[j],
            'account_id': server_account.val()
        };

        file_hide_json.remote.push(obj);
    }

    // 插入到隐藏域
    var res = JSON.stringify(file_hide_json);

    hidelists.val(res);
    jSuccess('添加成功！');
}

// 添加待分发文件
function add_filelists(ipserver, hidelists, filelists, sendfile_btn, file_show, server_account) {
    var iptxt = ipserver.val().trim().replace(new RegExp('\t', 'g'), ' ');
    var hidetxt = hidelists.val().trim();
    var file_road = filelists.val().trim().split('\n');
    var file_road_length = file_road.length;

    if (!iptxt) {
        jNotify('请填写ip信息！');
        ipserver.focus();
        return false;
    }

    if (!filelists.val().trim()) {
        jNotify('请填写分发路径！');
        filelists.focus();
        return false;
    }

    var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    
    if (!reg.test(iptxt)) {
        jNotify("ip输入框格式错误");
        return false;
    }

    sendfile_btn.button('loading');

    $.ajax({
        type: 'POST',
        url: '/ajax_agent_valid/',
        data: {
            'iptxt': iptxt
        },
        dataType: 'json',
        error: function (XMLHttpRequest) {
            jError(XMLHttpRequest.responseText);
            return false;
        },
        success: function (data) {
            sendfile_btn.button('complete').html("<i class='icon-plus'></i>添加待分发文件");
            file_show.parent().removeClass("hide");
            hidelists.val('');

            var res = $.parseJSON(data.ip_dict);

            for (var key in res) {
                if (key != 'total' && key != 'num') {
                    var obj = res[key];
                    var status = obj[0];

                    if (status == 1) {
                        file_show.find(".list2").remove();

                        var file_road_new = [];
                        var file_json = [];

                        // 判断隐藏域是否为空
                        if (hidelists.val() === '') {
                            var file_hide_json = {
                                "remote": []
                            };
                        } else {
                            var file_hide_json = $.parseJSON(hidelists.val());
                        }

                        // 删除空行
                        for (var i = 0; i < file_road_length; i++) {
                            file_road[i] === '' ? file_road.splice($.inArray(file_road[i], file_road), 1) : file_road_new.push(file_road[i]);
                        }

                        // 是否重名
                        var fileArr = [];

                        file_road_new.forEach(function(e, i) {
                            var pathArr = e.replace('\\', '/').split('/');

                            fileArr.push(pathArr[pathArr.length - 1]);
                        });

                        if (isRepeat(fileArr)) {
                            jNotify('存在重名文件，请检查！');

                            return false;
                        }

                        // 循环插入字典
                        for (var j = 0; j < file_road_new.length; j++) {
                            file_show.append('<li class="clearfix list2">远程文件：<i class="file-road" title=' + file_road_new[j] + '>' + file_road_new[j] + '</i><i class="ipconfig">' + key + '</i><i class="server-account">' + server_account.text() + '</i><span class="delete2">删除</span></li>');
                            
                            var obj = {
                                'name': file_road_new[j],
                                'ip': key,
                                'account_id': server_account.val()
                            };

                            file_hide_json.remote.push(obj);
                        }

                        // 插入到隐藏域
                        var res = JSON.stringify(file_hide_json);

                        hidelists.val(res);
                        jSuccess('添加成功！');
                    } else if (status === 0) {
                        jNotify('输入的密码有误！');
                        return false;
                    } else if (status == -1) {
                        jNotify('agent状态异常！');
                        return false;
                    } else if (status == -2) {
                        jNotify('IP输入框格式错误！');
                        return false;
                    } else if (status == -99) {
                        jNotify('agent不存在！');
                        return false;
                    } else {
                        jNotify('添加文件出错，请重试！');
                        return false;
                    }
                }
            }
        }
    });
    return true;
}

// 删除待分发文件远程隐藏域
function del_filelists(e, send_file_hide) {
    var ip_index = e.parent().index(".list2");
    var res = $.parseJSON(send_file_hide.val());

    res.remote.splice(ip_index, 1);

    var res_str = JSON.stringify(res);
    
    send_file_hide.val(res_str);
    e.parent().remove();
}

// 删除待分发文件url隐藏域
function del_fileurls(e, send_file_hide) {
    var ip_index = e.parent().index(".list3");
    var res = $.parseJSON(send_file_hide.val());

    res.remote.splice(ip_index, 1);

    var res_str = JSON.stringify(res);

    send_file_hide.val(res_str);
    e.parent().remove();
}

// 删除待分发文件本地隐藏域
function del_filelists2(e, record) {
    var id_num = e.siblings(".file-id").text();
    var record_ids = record.val().split(' ');

    record_ids.splice($.inArray(id_num, record_ids), 1);

    var id_txt = record_ids.join(' ');

    record.val(id_txt);
    e.parent().remove();
}

// 全选 全不选
function check_all(checked_all, checked_it, power_btn) {
    $(document).on("click", checked_all, function () {
        if($(this).prop("checked")) {
            $(checked_it).prop("checked", true).parents("tr").addClass('checknow');
        }else {
            $(checked_it).prop("checked", false).parents("tr").removeClass('checknow');
        }

        var checked_box = $(checked_it).filter(":checked");

        if(power_btn){
            check_power(checked_box,power_btn); 
        }
    });

    $(document).on("click", checked_it, function () {
        if($(this).prop("checked") === true) {
            $(this).parents("tr").addClass('checknow');
        }
        if ($(this).prop("checked") === false) {
            $(checked_all).prop("checked", false);
            $(this).parents("tr").removeClass('checknow');
        }
        if ($(checked_it).filter(":checked").length >= $(checked_it).length) {
            $(checked_all).prop("checked", true);
        }

        var checked_box = $(checked_it).filter(":checked");

        if(power_btn){
            check_power(checked_box,power_btn); 
        }
    });
}

// 开启授权
function check_power(checked_box,poewr_btn){
    if(checked_box.length != 0) {
        poewr_btn.prop("disabled",false);
    }
    else {
        poewr_btn.prop("disabled",true);
    }
}

// 时间比较
function time_compare(from, to) {
    var start_time = from.split('-');
    var end_time = to.split('-');
    var start = new Date(start_time[0], start_time[1] - 1, start_time[2]);
    var end = new Date(end_time[0], end_time[1] - 1, end_time[2]);

    if (start > end) {
        jNotify("开始时间不能大于结束时间！");
        return false;
    }
    return true;
}

// tab跳转
function tab_href(tabArr, valueArr, dataArr) {
    if ($('#li_' + tabArr).length && $('#li_' + tabArr).length > 0) {
        $('#li_' + tabArr).find("label").html(valueArr);
        $('#' + tabArr).html(dataArr);
        $('#myTab a[aria-controls="' + tabArr + '"]').tab('show');
    } else {
        $('#myTab').prepend('<li id="li_' + tabArr + '" role="presentation" style="  position: relative;" ><i onclick="close_tab(this)" class="icon-remove mytab-close"></i><a href="#' + tabArr + '" aria-controls="' + tabArr + '" role="tab" data-toggle="tab" style="padding-right: 24px;"><label class="tab-ellipsis">' + valueArr + '</label></a></li>');
        $('#tabs>.tab-content').prepend('<div role="tabpanel" class="tab-pane" id="' + tabArr + '"></div>');
        $('#' + tabArr).html(dataArr);
        $('#myTab a:first').tab('show');
    }

    show_tab_arrow();
}

// tab跳转2
function tab_href2(tabArr, valueArr, dataArr) {
    if ($('#li_' + tabArr).length && $('#li_' + tabArr).length > 0) {
        $('#li_' + tabArr).find("label").html(valueArr);
        $('#myTab a[aria-controls="' + tabArr + '"]').tab('show');
    } else {
        $('#myTab').prepend('<li id="li_' + tabArr + '" role="presentation" style="  position: relative;" ><i onclick="close_tab(this)" class="icon-remove mytab-close"></i><a href="#' + tabArr + '" aria-controls="' + tabArr + '" role="tab" data-toggle="tab" style="padding-right: 24px;"><label class="tab-ellipsis">' + valueArr + '</label></a></li>');
        $('#tabs>.tab-content').prepend('<div role="tabpanel" class="tab-pane show-already" id="' + tabArr + '"></div>');
        $('#' + tabArr).html(dataArr);
        $('#myTab a:first').tab('show');
    }

    show_tab_arrow();
    $('#' + tabArr).removeClass("show-already");
}

// 检测作业名
function check_job_name(id1, id2) {
    var name = id1.val();
    var remarks = id2.val();
    var len1 = 0,
        len2 = 0;
    var len_result1 = getByteLen(name, len1);
    var len_result2 = getByteLen(remarks, len2);

    if (len_result1 > 255) {
        jNotify("作业名称不能超过255个字符");
        return false;
    }

    if (len_result2 > 255) {
        jNotify("备注不能超过255个字符");
        return false;
    }
}

// 检测中英文字符
function getByteLen(val, len) {
    for (var i = 0; i < val.length; i++) {
        var a = val.charAt(i);

        if (a.match(/[^\x00-\xff]/ig) !== null) {
            len += 2;
        } else {
            len += 1;
        }
    }
    return len;
}

// 模板过滤
function template_filter() {
    var template_name = $("#template_name").val();
    var template_creator = $("#template_creator").val();
    var template_type = $("#template_type").val();
    var template_step = $("#template_step").val();
    var template_stime = $("#template_stime").val();
    var template_etime = $("#template_etime").val();
    var id_search_type = $("#id_search_type").val();
    var id_search_value = $("#id_search_value").val();

    template_table.fnReloadAjax('/md_manage/list/?p=0&template_name=' + template_name + '&template_creator=' + template_creator + '&template_type=' + template_type + '&template_step=' + template_step + '&template_stime=' + template_stime + '&template_etime=' + template_etime + '&id_search_type=' + id_search_type + '&id_search_value=' + id_search_value);
    $(".mdcontent_checked_all").prop("checked",false);
}

// 定时任务过滤
function schedule_filter() {
    var search_schedule_name = $("#search_schedule_name").val();
    var search_schedule_creator = $("#search_schedule_creator").val();
    var search_schedule_executor = $("#search_schedule_executor").val();
    var search_schedule_note = $("#search_schedule_note").val();
    var search_schedule_stime = $("#search_schedule_stime").val();
    var search_schedule_etime = $("#search_schedule_etime").val();
    var search_schedule_status = $("#search_schedule_status").val();

    if (schedule_table !== undefined) {
        schedule_table.fnReloadAjax('/timing_manage/list/?p=0&name=' + search_schedule_name + '&creator=' + search_schedule_creator + '&executor=' + search_schedule_executor + '&note=' + search_schedule_note + '&stime=' + search_schedule_stime + '&etime=' + search_schedule_etime + '&status=' + search_schedule_status);
    }
}

// 模板查看
function template_view(template_id) {
    $.ajax({
        type: 'GET',
        url: '/md_manage/show/' + template_id + '/',
        data: {},
        dataType: 'json',
        success: function (data) {
            var tabArr = 'template_view_info_' + template_id;
            var valueArr = '模板【' + data.template_name + '】主页';
            var dataArr = data.html;
            tab_href(tabArr, valueArr, dataArr);
        },
        error: function () {
            jError('出错了');
        }
    });
}

// 重复ip提示
function compare_ip(iparr) {
    var ip_all_list = [];
    for (i = 0; i < iparr.length; i++) {
        var new_list = iparr[i].split(' ');

        if (new_list.length == 1 && new_list !='' && new_list !=' ') {
            jNotify("格式输入错误，请检查！");
            return false;
        }

        var ip = new_list[0];

        if (!ip) {
            continue;
        }

        if ($.inArray(ip, ip_all_list) == -1) {
            ip_all_list.push(ip);
        } else {
            jNotify("存在重复ip：" + ip + "，请检查！");
            return false;
        }
    }
}

// 重复ip提示（无需密码）
function compare_ipfree(iparr) {
    var ip_all_list = [];

    for (i = 0; i < iparr.length; i++) {
        var ip = iparr[i].trim();

        if (!ip) {
            continue;
        }
        if ($.inArray(ip, ip_all_list) == -1) {
            ip_all_list.push(ip);
        } else {
            jNotify("存在重复ip：" + ip + "，请检查！");
            return false;
        }
    }
}

// 过滤错误ip及空行
function filter_ip(iparr, ip_show) {
    // 删除空行
    for (var i = 0; i < iparr.length; i++) {
        if (iparr[i] === "" || iparr[i] == " " || typeof(iparr[i]) == "undefined") {
            iparr.splice(i, 1);
            i = i - 1;
        }
    }

    for (var i = 0; i < iparr.length; i++) {
        if ($.inArray(' ', iparr[i]) == -1) {
            jNotify("存在错误的ip或输入格式，已过滤。");
            continue;
        }

        var ip = iparr[i].substr(0, iparr[i].indexOf(' '));

        // 验证ip格式
        var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
        
        if (!reg.test(ip)) {
            jNotify("存在错误的ip或输入格式，已过滤。");
            continue;
        }

        ip_show.append("<li class='clearfix'><i class='ipconfig'>" + ip + "</i><i class='status1'></i><i class='status2'></i><i class='loading'><img width='20px' src='/static/assets/img/loading.gif'></i></li>");
    }

}

// 过滤错误ip及空行(无需密码)
function filter_ipfree(iparr, ip_show, data_msg) {

    // 删除空行
    for (var i = 0; i < iparr.length; i++) {
        if (iparr[i] == "" || iparr[i] == " " || typeof(iparr[i]) == "undefined") {
            iparr.splice(i, 1);
            i = i - 1;
        }
    }

    if (data_msg == 'pwd') {
        for (var i = 0; i < iparr.length; i++) {
            var list = iparr[i].trim();

            if ($.inArray(' ', list) == -1) {
                jNotify("存在错误的ip或输入格式，已过滤。");
                continue;
            }

            var ip = list.substr(0, list.indexOf(' '));
            var pwd = list.substr(list.indexOf(' ') + 1, list.length);

            // 验证ip格式
            var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
            
            if (!reg.test(ip)) {
                jNotify("存在错误的ip或输入格式，已过滤。");
                continue;
            }

            ip_show.append("<li class='clearfix'><i class='ipconfig'>" + ip + "</i><i class='pwdconfig hide'>" + pwd + "</i><i class='status1'></i><i class='status2'></i><i class='loading'><img width='20px' src='/static/assets/img/loading.gif'></i></li>");
        }
    } else {
        for (var i = 0; i < iparr.length; i++) {
            var ip = iparr[i].trim();

            if ($.inArray(' ', ip) != -1) {
                jNotify("存在错误的ip或输入格式，已过滤。");
                continue;
            }

            // 验证ip格式
            var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
            
            if (!reg.test(ip)) {
                jNotify("存在错误的ip或输入格式，已过滤。");
                continue;
            }

            ip_show.append("<li class='clearfix'><i class='ipconfig'>" + ip + "</i><i class='status1'></i><i class='status2'></i><i class='loading'><img width='20px' src='/static/assets/img/loading.gif'></i></li>");
        }
    }

}

// ip验证插入
function vaild_ip(res, ip_show) {
    var html = '';

    for (var key in res.distinct_ip_dict) {
        var obj = res[key];
        var status = obj[0];
        var os = obj[2];
        var ip = obj[3];

        if (key != 'total' && key != 'num' && status != 1) {
            if (status == 0) {
                html += "<li class='clearfix'><i class='ipconfig'>" + ip + "</i><i class='os'>" + os + "</i><i class='status1'>密码错误</i><i class='status2'>不支持操作</i><span>删除</span></li>";
            } else if (status == -1) {
                html += "<li class='clearfix'><i class='ipconfig'>" + ip + "</i><i class='os'>" + os + "</i><i class='status1'>agent异常</i><i class='status2'>不支持操作</i><span>删除</span></li>";
            } else if (status == -2) {
                html += "<li class='clearfix'><i class='ipconfig'>" + ip + "</i><i class='os'>" + os + "</i><i class='status1'>格式错误</i><i class='status2'>不支持操作</i><span>删除</span></li>";
            } else if (status == -99) {
                html += "<li class='clearfix'><i class='ipconfig'>" + ip + "</i><i class='os'>" + os + "</i><i class='status1'>agent不存在</i><i class='status2'>不支持操作</i><span>删除</span></li>";
            }
        }
    }

    if (res) {
        for (var key in res.distinct_ip_dict) {
            var obj = res[key];
            var status = obj[0];
            var os = obj[2];
            var ip = obj[3];

            if (key != 'total' && key != 'num' && status == 1) {
                html += "<li class='clearfix'><i class='ipconfig'>" + ip + "</i><i class='os'>" + os + "</i><i class='status1'>agent正常</i><i class='status2'>支持操作</i><span>删除</span></li>";
            }
        }
    }

    ip_show.append(html);
}

// ip验证插入(无需密码)
/*function vaild_ipfree(res, ip_show) {
    var html = '';

    for (var key in res) {
        var obj = res[key];
        var status = obj[0];
        var os = obj[2];

        if (key != 'total' && key != 'num' && status != 1) {
            if (status == -1) {
                html += "<li class='clearfix'><i class='ipconfig'>" + key + "</i><i class='os'>" + os + "</i><i class='status1'>无权限操作</i><i class='status2 diswork'>不支持操作</i><span>删除</span></li>";
            } else if (status == -2) {
                html += "<li class='clearfix'><i class='ipconfig'>" + key + "</i><i class='os'>" + os + "</i><i class='status1'>agent异常</i><i class='status2 diswork'>不支持操作</i><span>删除</span></li>";
            } else if (status == -99) {
                html += "<li class='clearfix'><i class='ipconfig'>" + key + "</i><i class='os'>" + os + "</i><i class='status1'>agent未安装</i><i class='status2 diswork'>不支持操作</i><span>删除</span></li>";
            } else if (os == 'unknown') {
                html += "<li class='clearfix'><i class='ipconfig'>" + key + "</i><i class='os'>" + os + "</i><i class='status1'>系统类型未设定</i><i class='status2 diswork'>不支持操作</i><span>删除</span></li>";
            }
        }
    }

    if (res) {
        for (var key in res) {
            var obj = res[key];
            var status = obj[0];
            var os = obj[2];

            if (key != 'total' && key != 'num' && status == 1 && os != 'unknown') {
                html += "<li class='clearfix'><i class='ipconfig'>" + key + "</i><i class='os'>" + os + "</i><i class='status1'>agent正常</i><i class='status2'>支持操作</i><span>删除</span></li>";
            }
        }
    }

    ip_show.append(html);
}*/

// ip验证插入(无需密码，合并内外网ip)
function vaild_ipfree_v2(res, ip_show) {
    var html = '';

    for (var key in res) {
        var obj = res[key];
        var status = obj[0];
        var os = obj[2];
        var ip = obj[3];

        if (key != 'total' && key != 'num' && status != 1) {
            if (status == -1) {
                html += "<li class='clearfix'><i class='ipconfig' id=" + key + ">" + ip + "</i><i class='os'>" + os + "</i><i class='status1'>无权限操作</i><i class='status2 diswork'>不支持操作</i><span>删除</span></li>";
            } else if (status == -2) {
                html += "<li class='clearfix'><i class='ipconfig' id=" + key + ">" + ip + "</i><i class='os'>" + os + "</i><i class='status1'>agent异常</i><i class='status2 diswork'>不支持操作</i><span>删除</span></li>";
            } else if (status == -99) {
                html += "<li class='clearfix'><i class='ipconfig' id=" + key + ">" + ip + "</i><i class='os'>" + os + "</i><i class='status1'>agent未安装</i><i class='status2 diswork'>不支持操作</i><span>删除</span></li>";
            } else if (os == 'unknown') {
                html += "<li class='clearfix'><i class='ipconfig' id=" + key + ">" + ip + "</i><i class='os'>" + os + "</i><i class='status1'>系统类型未设定</i><i class='status2 diswork'>不支持操作</i><span>删除</span></li>";
            }
        }
    }

    if (res) {
        for (var key in res) {
            var obj = res[key];
            var status = obj[0];
            var os = obj[2];
            var ip = obj[3];

            if (key != 'total' && key != 'num' && status == 1 && os != 'unknown') {
                html += "<li class='clearfix'><i class='ipconfig' id=" + key + ">" + ip + "</i><i class='os'>" + os + "</i><i class='status1'>agent正常</i><i class='status2'>支持操作</i><span>删除</span></li>";
            }
        }
    }

    ip_show.append(html);
}

// 编辑分发文件ip验证插入
function vaild_ip2(res, ip_show) {
    var html = '';

    for (var key in res) {
        if (key != 'total' && key != 'num') {
            var obj = res[key];
            var status = obj[0];
            var os = obj[2];

            if (status == 1)
                html += "<li class='clearfix'><i class='ipconfig'>" + key + "</i><i class='os'>" + os + "</i><i class='status1'>agent正常</i><i class='status2'>支持操作</i><span>删除</span></li>";
            else if (status == 0)
                html += "<li class='clearfix'><i class='ipconfig'>" + key + "</i><i class='os'>" + os + "</i><i class='status1'>密码错误</i><i class='status2'>不支持操作</i><span>删除</span></li>";
            else if (status == -1)
                html += "<li class='clearfix'><i class='ipconfig'>" + key + "</i><i class='os'>" + os + "</i><i class='status1'>agent异常</i><i class='status2'>不支持操作</i><span>删除</span></li>";
            else if (status == -2)
                html += "<li class='clearfix'><i class='ipconfig'>" + key + "</i><i class='os'>" + os + "</i><i class='status1'>格式错误</i><i class='status2'>不支持操作</i><span>删除</span></li>";
            else if (status == -99)
                html += "<li class='clearfix'><i class='ipconfig'>" + key + "</i><i class='os'>" + os + "</i><i class='status1'>agent不存在</i><i class='status2'>不支持操作</i><span>删除</span></li>";
        }
    }

    ip_show.append(html);
}


// 删除列表ip及隐藏框ip
function delete_ip_hide(ip_hide, e, msg, ip_config) {
    var res = $.parseJSON(ip_hide.val());
    var total = res['total'];
    var num = res['num'];
    var dist = res[ip_config];

    total = total - 1;
    res['total'] = total;

    if (dist[0] == "1") {
        num = num - 1;
        res['num'] = num;
    }

    delete res[ip_config];
    
    var res_str = JSON.stringify(res);

    ip_hide.val(res_str);
    e.parent().remove();
    msg.html("涉及服务器[" + total + "]台，仅[<span>" + num + "</span>]台支持操作");
}

// 只可以输入数字 
function getEvent() {
    if (document.all) {
        return window.event; // for ie
    }

    func = getEvent.caller;

    while (func != null) {
        var arg0 = func.arguments[0];

        if (arg0) {
            if ((arg0.constructor == Event || arg0.constructor == MouseEvent) || (typeof(arg0) == "object" && arg0.preventDefault && arg0.stopPropagation)) {
                return arg0;
            }
        }

        func = func.caller;
    }
    return null;
}

function doit() {
    var ev = getEvent();

    if (ev.keyCode < 8) {
        return false;
    } else if (ev.keyCode > 8 && ev.keyCode < 48) {
        return false;
    } else if (ev.keyCode > 57 && ev.keyCode < 96) {
        return false;
    } else if (ev.keyCode > 105) {
        return false;
    } else {
        return true;
    }
}

// 复选框显示隐藏
function check_toggle(e, wrap, toggle_box) {
    e.on("ifChecked", function () {
        wrap.find(toggle_box).removeClass("hide");
    });
    e.on("ifUnchecked", function () {
        wrap.find(toggle_box).addClass("hide");
    });
}

// 显示编辑作业模板页面
function template_edit(template_id) {
    $.ajax({
        type: 'GET',
        url: '/md_manage/edit/' + template_id + '/',
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                var tabArr = 'template_edit_' + template_id;
                var valueArr = '编辑模板【' + data.result.template_name + '】';
                var dataArr = data.result.html;

                tab_href(tabArr, valueArr, dataArr);

                var work_type = data.result.work_type;
                var e = $(".work_type_" + template_id);

                product_from(e, work_type);

            } else {
                jError("出错了");
            }
        },
    });
}

// 所属业务拉取
function product_from(e, work_type) {
    $.ajax({
        type: "POST",
        url: '/usual/ajax_get_cmdb_product_returns/',
        dataType: 'json',
        timeout: 3000,
        success: function (data) {
            if (data) {
                e.html("<option value=''>未分类</option>");

                var html = '';

                $.each(data, function (i, e) {
                    if (e['productname'] == work_type) {
                        html += "<option data-id="+ e['productid'] +" "+"value=" + e['productname'] + " selected>" + e['productname'] + "</option>";
                    } else {
                        html += "<option data-id="+ e['productid'] +" "+"value=" + e['productname'] + ">" + e['productname'] + "</option>";
                    }
                });

                e.append(html);
            } else {
                jError("获取所属业务失败！");
            }
        },
        error: function () {
            jError("获取所属业务失败！");
        }
    });
}

// 提交编辑模板
function template_step_edit(template_step_id, type) {
    var template_form = $("#edit_template_form_" + template_step_id);

    $.ajax({
        type: 'POST',
        url: '/md_manage/template_step/edit/' + template_step_id + "/",
        data: template_form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                var tabArr = 'template_step_edit_' + template_step_id;
                var valueArr = '编辑模板步骤【' + data.result.name + '】';
                var dataArr = data.result.html;

                type == 'script' ? tab_href2(tabArr, valueArr, dataArr) : tab_href(tabArr, valueArr, dataArr);
            } else {
                jError(data.result.msg);
            }

        },
    });
    return true;
}

// 提交编辑模板v2
function template_step_edit_v2(template_step_id, type) {
    var template_form = $("#edit_template_form_" + template_step_id);

    $.ajax({
        type: 'POST',
        url: '/md_manage/template_step/edit_v2/' + template_step_id + "/",
        data: template_form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                var tabArr = 'template_step_edit_' + template_step_id;
                var valueArr = '编辑模板步骤【' + data.result.name + '】';
                var dataArr = data.result.html;

                type == 'script' ? tab_href2(tabArr, valueArr, dataArr) : tab_href(tabArr, valueArr, dataArr);
            } else {
                jError(data.result.msg);
            }

        },
    });
    return true;
}

// 步骤排序
function sort_step(e) {
    var $parents = e.parents(".edit-md-wrap");

    $parents.find(".edit_md_table tbody tr").each(function () {
        var $index = $(this).index() + 1;

        // 简化版
        $(this).find('td').eq(1).html("第" + $index + "步");
    });
}

function sort_step2(e, template_id, step_id_list) {
    sort_step(e);

    $.ajax({
        type: 'POST',
        url: '/md_manage/sort/' + template_id + '/',
        data: {
            'step_id_list': step_id_list
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                jSuccess('操作成功');
            } else {
                jError('操作失败');
            }
        },
        error: function () {
            jError('操作失败');
        }
    });
}

// 检测ip是否支持操作
function check_ip_support(ip_hide) {
    if (!ip_hide) {
        jNotify('无有效的Agent状态的IP');
        return false;
    }
    // 判断是否全部支持操作
    var res = $.parseJSON(ip_hide);
    var total = res['total'];
    var num = res['num'];

    if (total != num) {
        jNotify("存在不支持操作的机器，请删除!");
        return false;
    }

    if (num == 0) {
        jNotify('支持操作的机器不能为空!');
        return false;
    }

    return true;
}

// 保存模板步骤,回到模板编辑页面
function handle_edit_template_step(step_id, template_id, save_form, obj, check) {

    // 检测是否全部支持操作
    var data = $(obj).attr("data-type");
    var data_msg = $(obj).attr("data-msg");

    // 编辑脚本页
    if (data == 'script') {
        var $parents = $(obj).parents(".edit-script-wrap");
        var script_name = $parents.find(".edit-script-name").val();
        var script_desc = $parents.find(".edit-script-desc").val();
        var script_option = $parents.find(".edit-script-option").val();
        var script_version = $parents.find(".edit-script-version").val();
        var ip_hide = $parents.find(".edit-script-ip-hide").val();
        var checkbox = $parents.find("#dst_use_own").prop("checked");

        if (!script_name || !script_desc || script_option == '' || script_version == '') {
            jNotify('有未填写的输入项，请检查！');
            return false;
        }

        if (checkbox == true) {
            var msg = check_ip_support(ip_hide);
            if (msg == false) {
                return false;
            }
        }

    }
    // 编辑拉取文件页
    if (data == 'pullfile') {
        var $parents = $(obj).parents(".edit-pullfile-wrap");
        var pullfile_name = $parents.find(".edit-pullfile-name").val();
        var pullfile_desc = $parents.find(".edit-pullfile-desc").val();
        var pillfile_list = $parents.find(".edit-pullfile-list li").length;
        var pillfile_ip = $parents.find(".edit-pullfile-ip").val();
        var pillfile_path = $parents.find(".edit-pullfile-path").val();
        var ip_hide = $parents.find(".edit-pullfile-ip-hide").val();
        var pullfile_hide = $parents.find(".edit-pullfile-file-hide");
        var pullfile_filename = $parents.find(".edit-pullfile-list li .file-road");
        var checkbox = $parents.find("#dst_use_own").prop("checked");

        if (!pullfile_name || !pullfile_desc || pillfile_list == 0 || !pillfile_ip || !pillfile_path) {
            jNotify('有未填写的输入项，请检查！');
            return false;
        }

        if (checkbox == true) {
            var msg = check_ip_support(ip_hide);

            if (msg == false) {
                return false;
            }
        }

        // 存储文件路径
        var file_arr = [];

        pullfile_filename.each(function() {
            file_arr.push($(this).text());
        });

        var file_new = [];

        for (var i = 0, flie_length = file_arr.length; i < flie_length; i++) {
            var items = file_arr[i];

            if ($.inArray(items, file_new) == -1) {
                file_new.push(items);
            } else {
                jNotify("存在重复文件，请删除！");
                return false;
            }
        }

        var file_str = file_new.join(',');

        pullfile_hide.val(file_str);
    }
    // 编辑文本步骤
    if (data == 'text') {
        var $parents = $(obj).parents(".edit-text-wrap");
        var text_name = $parents.find(".edit-text-name").val();
        var text_content = $parents.find(".edit-text-content").val();

        if (!text_name) {
            jNotify('步骤名称不能为空！');
            return false;
        }

        if (!text_content) {
            jNotify('文本描述不能为空！');
            return false;
        }
    }

    // 编辑分发文件
    if (data == 'sendfile') {
        var $parents = $(obj).parents(".edit-sendfile-wrap");
        var sendfile_name = $parents.find(".edit-sendfile-name").val();
        var sendfile_desc = $parents.find(".edit-sendfile-desc").val();
        var sendfile_list = $parents.find(".edit-sendfile-ip li").length;
        var sendfile_path = $parents.find(".edit-sendfile-path").val();
        var ip_hide = $parents.find(".edit-sendfile-ip-hide").val();
        var checkbox = $parents.find("#dst_use_own").prop("checked");

        if (!sendfile_name || !sendfile_desc || sendfile_list == 0 || !sendfile_path) {
            jNotify('有未填写的输入项，请检查！');
            return false;
        }

        if (checkbox == true) {
            var msg = check_ip_support(ip_hide);

            if (msg == false) {
                return false;
            }
        }
    }

    // 检测机器类型及路径
    if (check == true) {
        if (data == 'sendfile') {
            var $parents = $(obj).parents(".edit-sendfile-wrap");
            var system = $parents.find(".os");
            var path = $parents.find(".edit-sendfile-path");
            var msg = check_system(system, path);

            if (msg == false) {
                return false;
            }
        } else {
            var $parents = $(obj).parents(".edit-pullfile-wrap");
            var system = $parents.find(".os");
            var path = $parents.find(".edit-pullfile-path");
            var msg = check_system(system, path);

            if (msg == false) {
                return false;
            }
        }
    }

    // 判断模板or实例
    data_msg == 'job' ? save_job(save_form, step_id, template_id) : save_template(save_form, step_id, template_id);
    return false;
}

// 保存模板步骤,回到模板编辑页面v2
function handle_edit_template_step_v2(step_id, template_id, save_form, obj, check) {

    // 检测是否全部支持操作
    var data = $(obj).attr("data-type");
    var data_msg = $(obj).attr("data-msg");

    // 编辑脚本页
    if (data == 'script') {
        var $parents = $(obj).parents(".edit-script-wrap");
        var script_name = $parents.find(".edit-script-name").val();
        var script_desc = $parents.find(".edit-script-desc").val();
        var script_option = $parents.find(".edit-script-option").val();
        var script_version = $parents.find(".edit-script-version").val();
        var ip_hide = $parents.find(".edit-script-ip-hide").val();
        var checkbox = $parents.find("#dst_use_own").prop("checked");
        var ip_result = $parents.find(".edit-script-ip-result li").length;

        if (!script_name || !script_desc || script_option == '' || script_version == '') {
            jNotify('有未填写的输入项，请检查！');
            return false;
        }

        if (checkbox == true) {
            if(ip_result){
                var msg = check_ip_support(ip_hide);

                if (msg == false) {
                    return false;
                }
            }
        }

    }

    // 编辑拉取文件页
    if (data == 'pullfile') {
        var $parents = $(obj).parents(".edit-pullfile-wrap");
        var pullfile_name = $parents.find(".edit-pullfile-name").val();
        var pullfile_desc = $parents.find(".edit-pullfile-desc").val();
        var pillfile_list = $parents.find(".edit-pullfile-list li").length;
        var pillfile_ip = $parents.find(".edit-pullfile-ip").val();
        var pillfile_path = $parents.find(".edit-pullfile-path").val();
        var ip_hide = $parents.find(".edit-pullfile-ip-hide").val();
        var pullfile_hide = $parents.find(".edit-pullfile-file-hide");
        var pullfile_filename = $parents.find(".edit-pullfile-list li .file-road");
        var checkbox = $parents.find("#dst_use_own").prop("checked");

        if (!pullfile_name || !pullfile_desc || pillfile_list == 0 || !pillfile_ip || !pillfile_path) {
            jNotify('有未填写的输入项，请检查！');
            return false;
        }

        if (checkbox == true) {
            var msg = check_ip_support(ip_hide);

            if (msg == false) {
                return false;
            }
        }

        // 存储文件路径
        var file_arr = [];

        pullfile_filename.each(function() {
            file_arr.push($(this).text());
        });

        var file_new = [];

        for (var i = 0, flie_length = file_arr.length; i < flie_length; i++) {
            var items = file_arr[i];

            if ($.inArray(items, file_new) == -1) {
                file_new.push(items);
            } else {
                jNotify("存在重复文件，请删除！");
                return false;
            }
        }

        var file_str = file_new.join(',');

        pullfile_hide.val(file_str);
    }

    // 编辑文本步骤
    if (data == 'text') {
        var $parents = $(obj).parents(".edit-text-wrap");
        var text_name = $parents.find(".edit-text-name").val();
        var text_content = $parents.find(".edit-text-content").val();

        if (!text_name) {
            jNotify('步骤名称不能为空！');
            return false;
        }

        if (!text_content) {
            jNotify('文本描述不能为空！');
            return false;
        }
    }

    // 编辑分发文件
    if (data == 'sendfile') {
        var $parents = $(obj).parents(".edit-sendfile-wrap");
        var sendfile_name = $parents.find(".edit-sendfile-name").val();
        var sendfile_desc = $parents.find(".edit-sendfile-desc").val();
        var sendfile_list = $parents.find(".edit-sendfile-ip li").length;
        var sendfile_path = $parents.find(".edit-sendfile-path").val();
        var ip_hide = $parents.find(".edit-sendfile-ip-hide").val();
        var checkbox = $parents.find("#dst_use_own").prop("checked");

        if (!sendfile_name || !sendfile_desc || sendfile_list == 0 || !sendfile_path) {
            jNotify('有未填写的输入项，请检查！');
            return false;
        }

        if (checkbox == true) {
            var msg = check_ip_support(ip_hide);

            if (msg == false) {
                return false;
            }
        }
    }

    // 检测机器类型及路径
    if (check == true) {
        if (data == 'sendfile') {
            var $parents = $(obj).parents(".edit-sendfile-wrap");
            var system = $parents.find(".os");
            var path = $parents.find(".edit-sendfile-path");
            var msg = check_system(system, path);

            if (msg == false) {
                return false;
            }
        } else {
            var $parents = $(obj).parents(".edit-pullfile-wrap");
            var system = $parents.find(".os");
            var path = $parents.find(".edit-pullfile-path");
            var msg = check_system(system, path);

            if (msg == false) {
                return false;
            }
        }
    }

    // 判断模板or实例
    save_template_v2(save_form, step_id, template_id);
    return false;
}

// 保存步骤（模板）
function save_template(save_form, step_id, template_id) {
    if (save_form == true) {
        var step_form = $("#edit_template_step_form_" + step_id);

        $.ajax({
            type: 'POST',
            url: '/md_manage/template_step/save/' + step_id + "/",
            data: step_form.serialize(),
            dataType: 'json',
            success: function (data) {
                if (data.status == 200) {
                    template_edit(template_id);
                    template_step_edit(step_id);
                    jSuccess(data.result.msg);
                } else {
                    jError(data.result.msg);
                }

            },
            error: function () {
                jError("保存步骤失败");
            }
        });
    } else {
        $('#myTab li.active').find("i").trigger("click");
        template_edit(template_id);
    }
}

// 保存步骤（模板）v2
function save_template_v2(save_form, step_id, template_id) {
    if (save_form == true) {
        var step_form = $("#edit_template_step_form_" + step_id);

        $.ajax({
            type: 'POST',
            url: '/md_manage/template_step/save/' + step_id + "/",
            data: step_form.serialize(),
            dataType: 'json',
            success: function (data) {
                if (data.status == 200) {
                    $('#myTab li.active').find("i").trigger("click");
                    job_view_v2(template_id);
                    jSuccess(data.result.msg);
                } else {
                    jError(data.result.msg);
                }

            },
            error: function () {
                jError("保存步骤失败");
            }
        });
    } else {
        $('#myTab li.active').find("i").trigger("click");
        job_view_v2(template_id);
    }
}

// 保存步骤（实例）
function save_job(save_form, step_id, template_id) {
    if (save_form == true) {
        var step_form = $("#edit_job_step_form_" + step_id);

        $.ajax({
            type: 'POST',
            url: '/job/job_step/save/' + step_id + "/",
            data: step_form.serialize(),
            dataType: 'json',
            success: function (data) {
                if (data.status == 200) {
                    job_view(template_id);
                    jSuccess(data.result.msg);
                } else {
                    jError(data.result.msg);
                }
            },
            error: function () {
                jError("保存步骤失败");
            }
        });
    } else {
        $('#myTab li.active').find("i").trigger("click");
        job_view(template_id);
    }
}

// ip添加(需要输入密码)
function add_ip(ip_area, ip_hide, ip_show, ip_add, save_set, scroll_wrap, url) {
    var url = url || '/ajax_pwd_valid_v2/1/';
    var iptxt = ip_area.val().trim().replace(new RegExp('\t', 'g'), ' ');
    var iparr = iptxt.split('\n');
    var hidetxt = ip_hide.val();

    if (!iptxt) {
        jNotify('请填写目标机器信息！');
        ip_area.focus();
        return false;
    }

    // 重复ip提示
    var result = compare_ip(iparr);

    ip_show.parent().removeClass("hide");
    ip_show.empty();

    // 过滤错误ip及空行
    filter_ip(iparr, ip_show);
    ip_add.button('loading');
    save_set.addClass("disabled");

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'iptxt': iptxt,
            'hidetxt': hidetxt
        },
        dataType: 'json',
        error: function (XMLHttpRequest) {
            jError(XMLHttpRequest.responseText);
            return false;
        },
        success: function (data) {
            ip_add.button('complete').html("<i class='icon-plus'></i>ip添加");
            save_set.removeClass("disabled");
            ip_show.parent().removeClass("hide");
            ip_hide.val(data.ip_dict);

            var res = $.parseJSON(data.ip_dict);

            scroll_wrap.html("涉及服务器[" + res.total + "]台，仅[" + res.num + "]台支持操作");
            ip_show.empty();

            // ip验证插入
            vaild_ip(res, ip_show);
        }
    });
    return true;
}

// ip添加（无需输入密码）
function add_ipfree(ip_area, ip_hide, ip_show, ip_add, save_set, scroll_wrap, data_msg) {
    var iptxt = ip_area.val().trim().replace(new RegExp('\t', 'g'), ' ');
    var iparr = iptxt.split('\n');
    var hidetxt = ip_hide.val();
    var ip_dict = {};

    if (!iptxt) {
        jNotify('请填写目标机器信息！');
        ip_area.focus();
        return false;
    }

    // 重复ip提示
    if (data_msg == 'pwd') {
        var result = compare_ip(iparr);
    } else {
        compare_ipfree(iparr);
    }
    
    ip_show.parent().removeClass("hide");
    ip_show.empty();

    // 过滤错误ip及空行
    filter_ipfree(iparr, ip_show, data_msg);

    var ip_list = [];
    var ip_obj = ip_show.find(".ipconfig");

    for (var i = 0, len = ip_obj.length; i < len; i++) {
        ip_list.push(ip_obj.eq(i).text());
    }

    var pwd_list = [];

    if (data_msg == 'pwd') {
        var pwd_obj = ip_show.find(".pwdconfig");

        for (var i = 0, len = pwd_obj.length; i < len; i++) {
            pwd_list.push(pwd_obj.eq(i).text());
        }

        // 存成对象 {'127.0.0.1':'123','127.0.0.2':'321'}
        for(var i=0; i<ip_list.length; i++) {
            var ip = ip_list[i];
            var pwd = pwd_list[i];
            ip_dict[ip] = pwd;
        }
    }

    if (ip_list == '') {
        jNotify("存在错误ip或输入格式，请检查！");
        return false;
    }

    ip_add.button('loading');
    save_set.addClass("disabled");

    $.ajax({
        type: 'post',
        url: '/usual/ajax_get_cmdb_ipvalid_returns_v2/',
        data: {
            'iplist': ip_list
        },
        dataType: 'json',
        error: function (XMLHttpRequest) {
            jError(XMLHttpRequest.responseText);
            return false;
        },
        success: function (data) {
            ip_add.button('complete').html("<i class='icon-plus'></i>ip添加");
            save_set.removeClass("disabled");
            ip_show.parent().removeClass("hide");
            ip_show.empty();

            // ip验证插入
            vaild_ipfree_v2(data, ip_show);

            var total = ip_show.find("li").length;
            var diswork = ip_show.find(".diswork").length;
            var num = total - diswork;

            data.total = total;
            data.num = num;

            if (data_msg == 'pwd') {
                for(key in data) {
                    var obj = data[key];
                    var k = obj[3];

                    if(k in ip_dict) {
                        obj[1] = ip_dict[k];
                    }
                }
            }

            scroll_wrap.html("涉及服务器[" + total + "]台，仅[" + num + "]台支持操作");
            ip_hide.val(JSON.stringify(data));
        }
    });
    return true;
}

// 编辑分发文件 ip添加
function add_ip2(ip_area, ip_hide, ip_show, ip_add, save_set, scroll_wrap) {
    var iptxt = ip_area.val().trim().replace(new RegExp('\t', 'g'), ' ');
    var iparr = iptxt.split('\n');
    var hidetxt = ip_hide.val();

    if (!iptxt) {
        jNotify('请填写目标机器信息！');
        ip_area.focus();
        return false;
    }

    // 重复ip提示
    compare_ip(iparr);
    ip_show.parent().removeClass("hide");
    ip_show.empty();

    // 过滤错误ip及空行
    filter_ip(iparr, ip_show);
    ip_add.button('loading');
    save_set.addClass("disabled");

    $.ajax({
        type: 'POST',
        url: '/ajax_pwd_valid_v2/2/',
        data: {
            'iptxt': iptxt,
            'hidetxt': hidetxt
        },
        dataType: 'json',
        error: function (XMLHttpRequest) {
            jError(XMLHttpRequest.responseText);
            return false;
        },
        success: function (data) {
            ip_add.button('complete').html("<i class='icon-plus'></i>ip添加");
            save_set.removeClass("disabled");
            ip_show.parent().removeClass("hide");
            ip_hide.val(data.ip_dict);

            var res = $.parseJSON(data.ip_dict);

            scroll_wrap.html("涉及服务器[" + res.total + "]台，仅[" + res.num + "]台支持操作");
            ip_show.empty();

            // ip验证插入
            vaild_ipfree_v2(res, ip_show);
        }
    });
    return true;
}

// 检查机器类型及路径
function check_system(system, path) {

    // 判断机器类型是否一致
    for (var i = 1; i < system.length; i++) {
        if (system.eq(i).text().toLowerCase().substr(0, 2) != system.eq(0).text().toLowerCase().substr(0, 2)) {
            jNotify('目标机器操作系统不一致，保存失败！');
            return result = false;
        }
    }

    // 判断路径是否合法
    if (system.eq(0).text().toLowerCase().indexOf('win') == 0) {
        var winpath = /^[a-zA-Z]:\\(?:[-\\w\\.\\d]+\\)*(?:[-\\w\\.\\d]+)?/;

        if (!winpath.test(path.val())) {
            jNotify('非法的windows路径！');
            return false;
        }

        var pathcode = /^[^"'?><*|]*$/;

        if (!pathcode.test(path.val())) {
            jNotify('包含特殊字符！(\"\'?><*|)');
            return false;
        }
    }

    if (system.eq(0).text().toLowerCase() == "linux") {
        var lnxPath = /^(\/([0-9a-zA-Z]+))+/;

        if (!lnxPath.test(path.val())) {
            jNotify('非法的linux路径！');
            return false;
        }
    }

    if (path.val().indexOf('\\\\') != -1 || path.val().indexOf('\//') != -1) {
        jNotify("路径中不能有重复的' / '或者' \\ '");
        return false;
    }

    return true;
}

// 删除待分发文件
function del_file(obj) {
    $(obj).parent('.list2').remove();
}

// 查看实例
function job_view(job_id) {
    $.ajax({
        type: 'GET',
        url: '/job/job_view/',
        data: {
            'job_id': job_id
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError(data.msg);
            } else {
                var tabArr = 'job_view_' + data.job_id;
                var valueArr = '作业实例';
                var dataArr = data.html;

                tab_href(tabArr, valueArr, dataArr);
            }
        },
        error: function () {}
    });
}


// 查看实例v2
function job_view_v2(template_id) {
    $.ajax({
        type: 'GET',
        url: '/job/job_view_v2/',
        data: {
            'template_id': template_id
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError(data.msg);
            } else {
                var tabArr = 'job_view_' + data.template_id;
                var valueArr = '作业实例【'+ data.template_name +'】';
                var dataArr = data.html;

                tab_href(tabArr, valueArr, dataArr);

                var work_type = data.work_type;
                var e = $(".work_type_" + data.template_id);

                product_from(e, work_type);
            }
        },
        error: function() {}
    });
}

// 编辑实例步骤
function job_step_edit(job_step_id, type) {
    $.ajax({
        type: 'POST',
        url: '/job/job_step/edit/' + job_step_id + "/",
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                var tabArr = 'job_step_edit_' + job_step_id;
                var valueArr = '编辑实例步骤【' + data.result.name + '】';
                var dataArr = data.result.html;

                type == 'script' ? tab_href2(tabArr, valueArr, dataArr) : tab_href(tabArr, valueArr, dataArr);
            } else {
                jError(data.result.msg);
            }

        },
    });
    return true;
}

// 查询脚本
function script_filter() {
    var name = $("#script_manage_name").val();
    var describe = $("#script_manage_describe").val();
    var create_user = $("#script_manage_create_user").val();
    var created_from = $("#script_manage_created_from").val();
    var created_to = $("#script_manage_created_to").val();

    if (created_from && created_to) {
        time_compare(created_from, created_to);
    }

    oTable_script_manage.fnReloadAjax('/script_manage/list/?p=0&name=' + name + '&create_user=' + create_user + '&describe=' + describe + '&created_from=' + created_from + '&created_to=' + created_to);
    $(".scriptcontent_checked_all").prop("checked",false);
    $("#script_btn_power").prop("disabled",true);
}

// 添加脚本
function show_script_add() {
    $.ajax({
        type: 'GET',
        url: '/script/script_add/',
        dataType: 'json',
        success: function (data) {
            var tabArr = 'script_add_info_' + data.check_id;
            var valueArr = '新建作业脚本';
            var dataArr = data.html;

            tab_href2(tabArr, valueArr, dataArr);
        },
        error: function () {
            jError('出错了');
        }
    });
}

// 删除脚本
function script_manage_delete(script_id) {
    if (confirm("是否真的要删除指定的内容？") == true) {
        $.ajax({
            type: 'POST',
            url: '/script/script_delete/',
            data: {
                'script_id': script_id
            },
            dataType: 'json',
            success: function (data) {
                if (data.result == 1) {
                    jSuccess('删除成功！');
                } else if (data.result == 0) {
                    jError(data.showMsg);
                }
                $('#script_manage').empty();
                $('#script_manage').html(data.html);
            },
            error: function (re, status) {}
        });
    }
}

// 查看脚本
function script_manage_view(script_id) {
    $.ajax({
        type: 'POST',
        url: '/script/script_view/',
        data: {
            'script_id': script_id
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError("获取脚本内容失败");
            } else {
                var tabArr = 'script_view_' + data.script_id;
                var valueArr = '查看脚本';
                var dataArr = data.html;

                tab_href(tabArr, valueArr, dataArr);
            }
        },
        error: function () {
            jError("获取脚本内容失败");
        }
    });
}

// 查看脚本2
function template_step_script_view(step_id) {
    var script_id = $("#edit_template_step_form_" + step_id).find("#step_script").val();

    if (script_id == "") {
        jNotify("请选择脚本后再查看");
    } else {
        script_manage_view(script_id);
    }
}

// 删除版本
function version_delete(version_id) {
    if (confirm("是否真的要删除指定的内容？") == true) {
        $.ajax({
            type: 'POST',
            url: '/script/version_delete/',
            data: {
                'version_id': version_id
            },
            dataType: 'json',
            success: function (data) {
                if (data.result == 1) {
                    jSuccess('删除成功！');
                } else if (data.result == 0) {
                    jError(data.showMsg);
                }

                $('#script_view_' + data.script_id).empty();
                $('#script_view_' + data.script_id).html(data.html);
            },
            error: function (re, status) {}
        });
    }
}

// 查看版本详细
function show_version_detail(version_id) {
    $.ajax({
        type: 'POST',
        url: '/script/show_version_detail/',
        data: {
            'version_id': version_id
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == 500) {
                jError('查看版本详细失败!');
            } else {
                var tabArr = 'version_detail_' + data.version_id;
                var valueArr = '脚本详细';
                var dataArr = data.html;

                tab_href2(tabArr, valueArr, dataArr);
            }
        },
        error: function(re, status) {}
    });
}

// 复制并新建版本
function version_copy(version_id) {
    $.ajax({
        type: 'GET',
        url: '/script/version_copy/',
        data: {
            'version_id': version_id
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError('复制并新建版本失败!');
            } else {
                var tabArr = 'version_copy_' + data.version_id;
                var valueArr = '复制并新建';
                var dataArr = data.html;

                tab_href2(tabArr, valueArr, dataArr);
            }
        },
        error: function (re, status) {}
    });
}

// 修改版本备注
function version_remarks_edit(version_id) {
    $.ajax({
        type: 'GET',
        url: '/script/version_remarks_edit/',
        data: {
            'version_id': version_id
        },
        dataType: 'json',
        success: function (data) {
            if (data.result == 0) {
                jError('修改版本备注失败!');
            } else {
                $('#edit_remarks').html(data.html);
                $('#edit_remarks').modal('show');
            }
        },
        error: function (re, status) {}
    });
}

// 保存版本备注
function version_remarks_save(version_id) {
    var version_remarks = $('#version_remarks_' + version_id).val();

    $('#edit_remarks').modal('hide');

    $.ajax({
        type: 'GET',
        url: '/script/version_remarks_save/',
        data: {
            'version_id': version_id,
            'version_remarks': version_remarks
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError('编辑版本备注失败!');
            } else {
                $('#script_view_' + data.script_id).empty();
                $('#script_view_' + data.script_id).html(data.html);
                jSuccess('编辑版本备注成功!');
            }
        },
        error: function (re, status) {}
    });
}

// 修改脚本
function script_manage_edit(script_id) {
    var script_name = $('#script_manage_view_name_' + script_id).val();
    var script_describe = $('#script_manage_view_describe_' + script_id).val();

    if (!script_name) {
        jNotify('请输入脚本名称');
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/script/script_edit/',
        dataType: 'json',
        data: {
            'script_id': script_id,
            'script_name': script_name,
            'script_describe': script_describe,
        },
        success: function (data) {
            if (data.status == 500) {
                jError(data.msg);
            } else {

                var tabArr = 'script_view_' + script_id;
                var valueArr = '查看脚本';
                var dataArr = data.html;

                tab_href(tabArr, valueArr, dataArr);
                jSuccess('保存脚本成功!');
            }
        },
        error: function () {
            jError('保存脚本失败!');
        }
    });
}

// 刷新账号列表
function refresh_accounts(obj) {
    var select_accounts = $(obj).parents(".row-fluid").find(".account-msg");

    $.ajax({
        type: 'GET',
        url: '/account/get_account_list/',
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                select_accounts.html('<option value="" selected>请选择执行账户</option>');
                $.each(data.result.accounts, function (n, item) {
                    select_accounts.append('<option value="' + item.a_id + '" >' + item.a_name + '</option>');
                });
                jSuccess("账户列表更新成功");
            } else {
                jError(data.result.msg);
            }
        },
        error: function () {
            jError('账户列表更新失败');
        }
    });
}

// 刷新授权账号列表
function refresh_accounts_v2 (obj) {
    var select_accounts = $(obj).parents(".row-fluid").find(".account-msg");

    $.ajax({
        type: 'GET',
        url: '/account/get_account_list_v2/',
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                select_accounts.html('<option value="" selected>请选择执行账户</option>');
                $.each(data.result.accounts, function (n, item) {
                    select_accounts.append('<option value="' + item.a_id + '" >' + item.a_name + '</option>');
                });
                jSuccess("账户列表更新成功");
            } else {
                jError(data.result.msg);
            }
        },
        error: function() {
            jError('账户列表更新失败');
        }
    });
}

// 刷新脚本列表
function template_step_refresh_script_list(step_id) {
    $.ajax({
        type: 'GET',
        url: '/md_manage/get_script_list/',
        dataType: 'json',
        success: function (data) {
            var select_script = $("#edit_template_step_form_" + step_id).find("#step_script");
            var select_version = $("#edit_template_step_form_" + step_id).find("#step_version");

            if (data.status == 200) {
                select_script.html('<option value="" selected>请选择步骤脚本</option>');
                select_version.html('<option value="" selected>请选择版本</option>');

                $.each(data.result.scripts, function (n, item) {
                    select_script.append('<option value="' + item.s_id + '" >' + item.s_name + '</option>');
                });
                jSuccess("脚本列表更新成功")
            } else {
                jError(data.result.msg);
            }
        },
        error: function () {
            jError('脚本列表更新失败');
        }
    });
}

// 删除模板
function template_del(template_id) {
    if (confirm("是否真的要删除该模板？") == true) {
        $.ajax({
            url: '/md_manage/delete/' + template_id + '/',
            dataType: 'json',
            success: function (data) {
                if (data.status == 200) {
                    $('#myTab li.active').find("i").trigger("click");
                    template_filter();
                    jSuccess('删除成功！');
                } else if (data.status == 500) {
                    jError(data.result.msg);
                }
            },
            error: function (re, status) {
                jError("出错了");
            }
        });
    }
}

// 添加实例
function example_manage_add(template_id) {
    $.ajax({
        type: 'GET',
        url: '/job/job_add/',
        data: {
            'template_id': template_id
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError('添加实例失败!');
            } else {
                var tabArr = 'job_view_' + data.job_id;
                var valueArr = '作业实例';
                var dataArr = data.html;

                tab_href(tabArr, valueArr, dataArr);
            }
        },
        error: function (re, status) {}
    });
}

function submit_create_new_template(template_id) {
    var check = check_job_name($("#id_name"), $("#id_remarks"));

    if (check == false) {
        return false;
    }

    var template_form = $("#new_template_form_" + template_id);

    $.ajax({
        type: 'POST',
        url: '/md_manage/add/',
        data: template_form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                $('#myTab li.active').find("i").trigger("click");
                template_view(data.result.template_id);
                template_filter();
                jSuccess('新作业模板创建成功！');
            } else {
                $("#template_add_info").html(data.result.html);
                jError('作业模板创建失败！');
            }

        },
    });
    return true;
}


// 删除实例
function job_delete(job_id, template_id) {
    if (confirm("是否真的要删除指定的内容？") == true) {
        $.ajax({
            type: 'POST',
            url: '/job/job_delete/',
            data: {
                'job_id': job_id
            },
            dataType: 'json',
            success: function (data) {
                if (data.result == 1) {
                    jSuccess('删除成功！');
                } else if (data.result == 0) {
                    jError('删除失败！');
                }
                $('#refresh_job_list_' + template_id).click();
            },
            error: function (re, status) {}
        });
    }
}

// 删除实例v2
function job_delete_v2(template_id) {
    if (confirm("是否真的要删除指定的内容？") == true) {
        $.ajax({
            type: 'POST',
            url: '/job/job_delete_v2/',
            data: {
                'template_id': template_id
            },
            dataType: 'json',
            success: function (data) {
                if (data.result == 1) {
                    jSuccess('删除成功！');
                    job_manage_filter_v2();
                } else if (data.result == 0) {
                    jError('删除失败！');
                }
            },
            error: function (re, status) {}
        });

    }
}

// 复制并新建实例
function job_copy(job_id) {
    $("#loading-panel").show().css({
        "z-index": 1000
    }).animate({
        opacity: "1"
    }, 100);
    $.ajax({
        type: 'GET',
        url: '/job/job_copy/',
        data: {
            'job_id': job_id
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError('复制并新建实例失败!');
            } else {
                var tabArr = 'job_view_' + data.job_id;
                var valueArr = '作业实例';
                var dataArr = data.html;

                tab_href(tabArr, valueArr, dataArr);
            }

            $("#loading-panel").animate({
                opacity: "0"
            }, 200).hide().css({
                "z-index": -999
            });
        },
        error: function (re, status) {
            $("#loading-panel").animate({
                opacity: "0"
            }, 200).hide().css({
                "z-index": -999
            });
        }
    });
}

// 复制并新建实例v2
function job_copy_v2(template_id) {
    $("#loading-panel").show().css({
        "z-index": 1000
    }).animate({
        opacity: "1"
    }, 100);
    $.ajax({
        type: 'GET',
        url: '/job/job_copy_v2/',
        data: {
            'template_id': template_id
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError('复制并新建实例失败!');
            } else {
                var tabArr = 'job_view_' + data.template_id;
                var valueArr = '作业实例';
                var dataArr = data.html;

                tab_href(tabArr, valueArr, dataArr);

                var work_type = data.work_type;
                var e = $(".work_type_" + data.template_id);

                product_from(e, work_type);
            }

            $("#loading-panel").animate({
                opacity: "0"
            }, 200).hide().css({
                "z-index": -999
            });
        },
        error: function (re, status) {
            $("#loading-panel").animate({
                opacity: "0"
            }, 200).hide().css({
                "z-index": -999
            });
        }
    });
}

function show_result(history_id) {
    // 显示执行详情页面.
    $.ajax({
        type: 'POST',
        url: '/history/show_result/' + history_id + '/',
        dataType: 'json',
        async: true,
        data: {},
        success: function (data) {
            var result = data.result;
            var tabArr = 'exec_result_' + history_id;
            var valueArr = result.job_name + '-执行';
            var dataArr = data.result.html;

            tab_href(tabArr, valueArr, dataArr);
        },
        error: function () {
            jError('出错了');
        }
    });
}

// 查询结果(改密)
function showPswResults(jid_list, ip_list, total) {
    var timeout = 0;
    var timer = setInterval(function() {
        timeout += 5;
        if (timeout > 60) {
            clearInterval(timer);
        }

        $("#psw_result").empty(); // 清空原来的数据

        $.ajax({
            type: 'POST',
            url: '/usual/ajax_get_psw_returns/',
            data: {
                'jid_list': jid_list,
                'ip_list': ip_list
            },
            dataType: "json",
            success: function (data) {
                $("#psw_result").empty();

                if (data.res.length == total) {
                    clearInterval(timer);
                }

                for (var i = 0; i < data.res.length; i++) {
                    $("#psw_result").append("<li><i class='ipconfig'>" + data.res[i].minion_ip + "</i><i class='loading'>" + data.res[i].result_str + "</i></li>");
                }
            }
        })
    }, 5000); // 隔5秒就查询一次数据
};

// 查询结果（重启）
function showRebootResults(jid, ip_list, total) {
    var timeout = 0;
    var timer = setInterval(function() {
        timeout += 5;
        if (timeout > 60) {
            clearInterval(timer);
        }

        $("#reboot_result").empty(); // 清空原来的数据

        $.ajax({
            type: 'POST',
            url: '/usual/ajax_get_reboot_returns/',
            data: {
                'jid': jid,
                'ip_list': ip_list
            },
            dataType: "json",
            success: function(data) {
                $("#reboot_result").empty();

                if (data.res.length == total) {
                    clearInterval(timer);
                }

                for (var i = 0; i < data.res.length; i++) {
                    $("#reboot_result").append("<li><i class='ipconfig'>" + data.res[i].minion_ip + "</i><i class='loading'>" + data.res[i].result_str + "</i></li>");
                }
            }
        })
    }, 5000); // 隔5秒就查询一次数据
};

// 检测规则框必填项
function rule_model(obj) {
    var $parents = $(obj).parents(".modify-timing-modal");
    var rule = $parents.find(".expression"),
        note = $parents.find(".note"),
        executor = $parents.find(".executor");

    if (!rule.val() || !note.val() || !executor.val()) {
        jNotify("有未填写的输入项，请检查！");
        return false;
    }
}


function show_history_info(history_id) {

    // 显示历史作业详情页面.
    $.ajax({
        type: 'POST',
        url: '/history/' + history_id + '/',
        dataType: 'json',
        async: true,
        data: {},
        success: function (data) {
            var result = data.result;
            var tabArr = 'exec_job_info_' + history_id;
            var valueArr = result.job_name;
            var dataArr = data.result.html;

            tab_href(tabArr, valueArr, dataArr);
        },
        error: function () {
            jError('出错了');
        }
    });
    return false;
}

// 账户添加验证格式及长度
function sum_add_account() {
    var is_name = /^\w+$/;
    var is_another_name = /^[\u4e00-\u9fa5A-Za-z0-9-_]*$/;
    var name_txt = $("#id_name").val();
    var another_name_txt = $("#id_name_abbr").val();
    // var password_txt = $("#id_password").val();

    if (!is_name.test(name_txt)) {
        jNotify("账户名称只能由数字、英文字母或者下划线组成！");
        return false;
    }
    if (!is_another_name.test(another_name_txt)) {
        jNotify("账户别名只能由中英文、数字、下划线或者减号组成！");
        return false;
    }
    if (name_txt.length > 20) {
        jNotify("账户名称不能超过20个字符");
        return false;
    }
    if (another_name_txt.length > 100) {
        jNotify("账户名称不能超过100个字符");
        return false;
    }
    // if (password_txt.length > 20) {
    //     jNotify("账户密码不能超过20个字符");
    //     return false;
    // }

    $.ajax({
        type: 'POST',
        url: '/account/add/',
        data: $("#addaccountform").serialize(),
        dataType: 'json',
        success: function (msg) {
            $('#account_add').empty();
            $('#account_add').html(msg.html);

            if (msg.result == 1) {
                jSuccess('保存账户成功！');
            }
        },
    });
    return true;
}

// 修改账户
function account_edit(account_id, name) {
    $.ajax({
        type: 'GET',
        url: '/account/edit/' + account_id + '/',
        dataType: 'json',
        success: function (data) {
            var tabArr = 'account_edit_' + account_id;
            var valueArr = '账户[' + name + ']';
            var dataArr = data.html;

            tab_href(tabArr, valueArr, dataArr);
        },
        error: function (re, status) {}
    });
}

// 删除账户
function account_del(form, delete_url, type) {
    if (confirm("是否真的要删除指定的内容？") == true) {
        $.ajax({
            type: type,
            url: delete_url,
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                if (data.result == 1) {
                    jSuccess('删除成功！');
                } else if (data.result == 0) {
                    jError('删除失败！');
                }
                $('#account').empty();
                $('#account').html(data.html);
            },
            error: function (re, status) {}
        });
    }
}


// 查询账户
function account_filter() {
    var name = $("#account_name").val();
    var name_abbr = $("#account_name_abbr").val();
    var update_user = $("#account_update_user").val();
    var created_from = $("#account_created_from").val();
    var created_to = $("#account_created_to").val();
    var updated_from = $("#account_updated_from").val();
    var updated_to = $("#account_updated_to").val();

    if (created_from && created_to) {
        result = time_compare(created_from, created_to);
        if (!result) {
            return false;
        }
    }

    if (updated_from && updated_to) {
        result = time_compare(updated_from, updated_to);
        if (!result) {
            return false;
        }
    }

    oTable_account.fnReloadAjax('/account/list/?p=0&name=' + name + '&name_abbr=' + name_abbr + '&update_user=' + update_user + '&created_from=' + created_from + '&created_to=' + created_to + '&updated_from=' + updated_from + '&updated_to=' + updated_to);
}

// 作业实例查询
function job_manage_filter() {
    var name = $("#job_manage_name").val();
    var create_user = $("#job_manage_create_user").val();
    var created_from = $("#job_manage_created_from").val();
    var created_to = $("#job_manage_created_to").val();
    var update_user = $("#job_manage_update_user").val();
    var updated_from = $("#job_manage_updated_from").val();
    var updated_to = $("#job_manage_updated_to").val();

    if (created_from && created_to) {
        result = time_compare(created_from, created_to);
        if (!result) {
            return false;
        }
    }

    if (updated_from && updated_to) {
        result = time_compare(updated_from, updated_to);
        if (!result) {
            return false;
        }
    }

    oTable_job_manage.fnReloadAjax('/example_manage/list/?p=0&name=' + name + '&create_user=' + create_user + '&update_user=' + update_user + '&created_from=' + created_from + '&created_to=' + created_to + '&updated_from=' + updated_from + '&updated_to=' + updated_to);
    $(".jobcontent_checked_all").prop("checked",false);
}

// 作业实例查询v2
function job_manage_filter_v2() {
    var name = $("#job_manage_name").val();
    var create_user = $("#job_manage_create_user").val();
    var created_from = $("#job_manage_created_from").val();
    var created_to = $("#job_manage_created_to").val();
    var update_user = $("#job_manage_update_user").val();
    var updated_from = $("#job_manage_updated_from").val();
    var updated_to = $("#job_manage_updated_to").val();
    var product = $("#job_manage_product").val();

    if (created_from && created_to) {
        result = time_compare(created_from, created_to);
        if (!result) {
            return false;
        }
    }

    if (updated_from && updated_to) {
        result = time_compare(updated_from, updated_to);
        if (!result) {
            return false;
        }
    }

    oTable_job_manage.fnReloadAjax('/job_manage/list/?p=0&name=' + name + '&create_user=' + create_user + '&update_user=' + update_user + '&created_from=' + created_from + '&created_to=' + created_to + '&updated_from=' + updated_from + '&updated_to=' + updated_to + '&product=' + product);
    $(".jobcontent_checked_all").prop("checked",false);
    $("#job_btn_power").prop("disabled",true);
}

// 保存实例
function job_edit(job_id) {
    var check_list = [];

    $('#example_view_form_' + job_id).find("input:checked").each(function() {
        check_list.push($(this).val()); 
    });

    var job_name = $('#example_view_name_' + job_id).val();
    var job_remarks = $('#example_view_remarks_' + job_id).val();

    if (!job_name) {
        jError('实例名称不能为空!');
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/job/job_view/',
        data: {
            'job_id': job_id,
            'job_name': job_name,
            'job_remarks': job_remarks,
            'check_list': check_list
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError(data.msg);
            } else {
                jSuccess('保存实例成功!');
            }
        },
        error: function (re, status) {}
    });
}

// 保存实例全程设定
function job_full_setting_save(job_id) {
    var job_form = $("#edit_job_form_settings_" + job_id);

    $.ajax({
        type: 'POST',
        url: '/job/save_full_setting/' + job_id + "/",
        data: job_form.serialize(),
        dataType: 'json',
        success: function(data) {
            if (data.status == 200) {
                jSuccess('操作成功！');
            } else {
                jError(data.result.msg);
            }
        },
    });
    return true;
}

// 作业立即执行
function job_start_now(job_id) {
    $.ajax({
        type: 'POST',
        url: '/job/job_start_now/' + job_id + "/",
        dataType: 'json',
        success: function(data) {
            if (data.status == 200) {
                show_result(data.result.history_id);
                jSuccess('操作成功！');
            } else {
                jError(data.result.msg);
            }
        },
    });
    return true;
}

// 作业立即执行v2
function job_start_now_v2(template_id,obj) {
    var $modal = $(obj).parents('.comfirm_fullset');

	$(obj).button('loading');

    $.ajax({
        type: 'POST',
        url: '/job/job_start_now_v2/' + template_id + "/",
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                show_result(data.result.history_id);
                jSuccess('操作成功！');
                $(obj).button('complete').html("<i class='icon-play icon-white'></i>立即启动");
                $modal.modal('hide');
            } else {
                jError(data.result.msg);
                $(obj).button('complete').html("<i class='icon-play icon-white'></i>立即启动");
            }
        },
    });
    return true;
}

// 显示新建定时任务页面
function show_schedule_new(job_id) {
    var modify_modal = $('#set_timing_' + job_id);

    $.ajax({
        type: 'get',
        url: '/timing_manage/add/' + job_id + '/',
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError(data.result.msg);
            } else {
                modify_modal.html(data.result.html);
                modify_modal.modal('show');
            }
        },
        error: function (re, status) {
            jError("页面显示失败");
        }
    });
    return false;
}

// 显示新建定时任务页面v2
function show_schedule_new_v2(template_id) {
    var modify_modal = $('#set_timing_' + template_id);

    $.ajax({
        type: 'get',
        url: '/timing_manage/add_v2/' + template_id + '/',
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError(data.result.msg);
            } else {
                modify_modal.html(data.result.html);
                modify_modal.modal('show');
            }
        },
        error: function (re, status) {
            jError("页面显示失败");
        }
    });
    return false;
}

// 新建定时规则
function schedule_save(check_id, job_id, obj) {
    var schedule_form = $("#schedule_add_" + check_id);
    var check = rule_model(obj);

    if (check == false) {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/timing_manage/add/' + job_id + "/",
        data: schedule_form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                jSuccess('定时任务创建成功！');
                $('#set_timing_' + job_id).modal("hide");
            } else {
                jError(data.result.msg);
            }
        },
        error: function () {
            jError("定时任务创建失败");
        }
    });
    return true;
}

// 历史查询
function history_filter() {
    var job_name = $("#history_job_name").val();
    var history_user = $("#history_user").val();
    var start_from = $("#history_start_from").val();
    var start_to = $("#history_start_to").val();
    var history_status = $("#history_status").val();
    var template_type = $("#history_template_type").val();
    var template_step = $("#history_template_step").val();
    var end_from = $("#history_end_from").val();
    var end_to = $("#history_end_to").val();
    var template_result = $("#history_template_result").val();

    if (start_from && start_to) {
        result = time_compare(start_from, start_to);
        if (!result) {
            return false;
        }
    }

    if (end_from && end_to) {
        result = time_compare(end_from, end_to);
        if (!result) {
            return false;
        }
    }

    oTable_history.fnReloadAjax('/history/list/?p=0&job_name=' + job_name + '&history_user=' + history_user + '&start_from=' + start_from + '&start_to=' + start_to + '&history_status=' + history_status + '&template_type=' + template_type + '&template_step=' + template_step + '&end_from=' + end_from + '&end_to=' + end_to + '&template_result=' + template_result);
}

// 显示步骤详细信息.
function show_history_step_info(history_step_id, history_id) {
    $.ajax({
        type: 'GET',
        url: '/history/ajax_show_history_step_info/' + history_step_id + '/',
        dataType: 'json',
        async: true,
        success: function (data) {
            var result = data.result;

            if (data.status == 200) {
                $("#history_step_info_" + history_id).html(result.html);
            } else {
                jError(result.msg)
            }
        },
        error: function () {
            jError('出错了');
        }
    });
}

// 新建作业模板
function show_template_add() {
    $.ajax({
        type: 'GET',
        url: '/md_manage/add/',
        data: {},
        success: function (data) {
            var tabArr = 'template_add_info';
            var valueArr = '新建作业模板';
            var dataArr = data;

            tab_href(tabArr, valueArr, dataArr);
        },
        error: function () {
            jError('出错了');
        }
    });
}

// 新建作业v2
function show_job_add() {
    $.ajax({
        type: 'GET',
        url: '/job/job_add_v2/',
        data: {},
        success: function (data) {
            var data = $.parseJSON(data);

            if (data.status == 500) {
                jError(data.msg);
            } else {
                var tabArr = 'job_view_' + data.template_id;
                var valueArr = '作业实例【'+ data.template_name +'】';
                var dataArr = data.html;

                tab_href(tabArr, valueArr, dataArr);

                var e = $(".work_type_" + data.template_id);

                product_from(e, '');
            }
        },
        error: function () {
            jError('出错了');
        }
    });
}

// 提交编辑模板
function submit_edit_template(template_id) {
    var check = check_job_name($("#id_name"), $("#id_remarks"));

    if (check == false) {
        return false;
    }

    var template_form = $("#edit_template_form_" + template_id);

    $.ajax({
        type: 'POST',
        url: '/md_manage/edit/' + template_id + "/",
        data: template_form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                $('#myTab li.active').find("i").trigger("click");
                template_view(data.result.template_id);
                template_filter();
                jSuccess('操作成功！');
            } else {
                var tabArr = 'template_edit_' + template_id;
                var valueArr = '编辑作业【' + data.result.template_name + '】';
                var dataArr = data.result.html;

                tab_href(tabArr, valueArr, dataArr);
                jError('操作失败！');
            }

        },
    });
    return true;
}

// 提交编辑模板v2
function submit_edit_template_v2(template_id) {
    var check_list = [];

    $('#edit_template_form_' + template_id).find("input:checked").each(function() {
        check_list.push($(this).val());
    });
    
    var check = check_job_name($("#id_name"), $("#id_remarks"));

    if (check == false) {
        return false;
    }

    var template_form = $("#edit_template_form_" + template_id);
    var form_serialize = template_form.serialize();

    form_serialize = form_serialize + "&check_list[]=" +check_list;

    $.ajax({
        type: 'POST',
        url: '/job/job_view_v2/',
        data: form_serialize,
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError(data.msg);
            } else {
                jSuccess('保存实例成功!');
            }

            var tabArr = 'job_view_' + data.template_id;
            var valueArr = '作业实例【'+ data.template_name +'】';
            var dataArr = data.html;

            tab_href(tabArr, valueArr, dataArr);

            var work_type = data.work_type;
            var e = $(".work_type_" + data.template_id);

            product_from(e, work_type);
        },
        error: function (re, status) {}
    });
    
}

// 保存模板全程设定
function template_full_setting_save(template_id) {
    var template_form = $("#edit_template_form_settings_" + template_id);
    var ip_hide =  template_form.find("#full_settings_ips_hide").val();
    var ip_result =  template_form.find(".edit-fullset-ip-result li").length;

    if (ip_result) {
        var msg = check_ip_support(ip_hide);

        if (msg == false) {
            return false;
        }
    }

    $.ajax({
        type: 'POST',
        url: '/md_manage/save_full_setting/' + template_id + "/",
        data: template_form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                $('#myTab li.active').find("i").trigger("click");
                job_view_v2(template_id);
                jSuccess('操作成功！');
            } else {
                jError(data.result.msg);
            }

        }
    });
    return true;
}

// 清空模板步骤中目标机器配置
function clear_settings(template_id) {
    if (confirm("操作将重置全程设定及所有步骤中的目标机器、执行账户、执行模式和脚本步骤中超时及参数配置，确认执行？") == true) {
        $.ajax({
            type: 'POST',
            url: '/md_manage/clear_settings/' + template_id + "/",
            dataType: 'json',
            success: function (data) {
                if (data.status == 200) {
                    $('#myTab li.active').find("i").trigger("click");
                    job_view_v2(template_id);
                    jSuccess('操作成功！');
                } else {
                    jError(data.result.msg);
                }

            }
        });
    }
    return true;
}

// 启动结束后清空配置
function clear_settings_after_run (template_id){
    $.ajax({
        type: 'POST',
        url: '/md_manage/clear_settings/' + template_id + "/",
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                jSuccess('操作成功！');
            } else {
                jError(data.result.msg);
            }

        }
    });
}

// 显示脚本详情页面.
function script_once_detail(version_id, history_step_id, script_name) {
    $.ajax({
        type: 'POST',
        url: '/script/script_detail/' + version_id + '/' + history_step_id + '/',
        dataType: 'json',
        async: true,
        data: {},
        success: function (data) {
            var result = data.result;
            var tabArr = 'script_detail_' + version_id;
            var valueArr = script_name + '-执行详细';
            var dataArr = result.html;

            tab_href(tabArr, valueArr, dataArr);
        },
        error: function () {}
    });
}

// 显示脚本作业实例
function show_script_instance(history_id) {
    $.ajax({
        type: 'POST',
        url: '/history/' + history_id + '/',
        dataType: 'json',
        async: true,
        data: {},
        success: function (data) {
            var result = data.result;
            var tabArr = 'exec_job_info_' + result.job_name;
            var valueArr = result.job_name;
            var dataArr = data.result.html;

            tab_href(tabArr, valueArr, dataArr);
        },
        error: function () {
            jError('出错了');
        }
    });
}

// 同步版本
function version_sync(version_id) {
    $.ajax({
        type: 'GET',
        url: '/script/version_template_sync/',
        data: {
            'version_id': version_id
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError('同步版本失败!');
            } else {
                var tabArr = 'version_sync_' + version_id;
                var valueArr = '同步版本';
                var dataArr = data.html;

                tab_href(tabArr, valueArr, dataArr);
            }
        },
        error: function(re, status) {}
    });
}

// 同步版本v2
function version_sync_v2(version_id) {
    $.ajax({
        type: 'GET',
        url: '/script/version_template_sync_v2/',
        data: {
            'version_id': version_id
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError('同步版本失败!');
            } else {
                var tabArr = 'version_sync_' + version_id;
                var valueArr = '同步版本';
                var dataArr = data.html;

                tab_href(tabArr, valueArr, dataArr);
            }
        },
        error: function (re, status) {}
    });
}

// 替换实例步骤版本
function version_job_sync(version_id, template_id) {
    $.ajax({
        type: 'get',
        url: '/script/version_job_sync/',
        data: {
            'version_id': version_id,
            'template_id': template_id
        },
        dataType: 'json',
        success: function (data) {
            if (data.status == 500) {
                jError('替换实例步骤版本失败!');
            } else {
                $('#select_example_step_' + version_id).html(data.html);
                $('#select_example_step_' + version_id).modal('show');
            }
        },
        error: function (re, status) {}
    });
    return false;
}

// 替换实例步骤版本
function version_job_sync_save(version_id) {
    if ($(".update_step_checked_it_" + version_id).filter(":checked").length == 0) {
        jNotify("指定实例步骤列表为空，替换脚本版本失败！");
        return false;
    } else {
        var check_list = [];

        $('#select_example_step_' + version_id).find("input:checked").each(function() {
            check_list.push($(this).val()); 
        });

        $.ajax({
            type: 'post',
            url: '/script/version_job_sync/',
            data: {
                'version_id': version_id,
                'check_list': check_list
            },
            dataType: 'json',
            success: function (data) {
                if (data.status == 500) {
                    jError('替换实例步骤版本失败!');
                } else {
                    jSuccess('替换实例步骤版本成功!');
                    $('#select_example_step_' + version_id).modal('hide');
                }
            },
            error: function (re, status) {}
        });
        return false;
    }
}
