function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function inputNumberComma(obj) {
    obj.value = comma(uncomma(obj.value));
}

function comma(str) {
    str = String(str);
    parts = str.split('.');
    part0 = parts[0].replace(/(\d)(?=(?:\d{3})+(?!\d))/g, '$1,');
    result = part0;
    if (parts[1])
        result += '.' + parts[1];
    return result;
}

function uncomma(str) {
    str = String(str);
    return str.replace(/[^\d]+/g, '');
}


function DataTable_MakeTHead(table_infos) {
    for (var table_info of table_infos) {
        var table = document.getElementById(table_info['id']);
        var elements = table.getElementsByTagName('thead');
        if (elements.length != 1) {
            alert('<thead> not exist.');
            return;
        }
        var thead = elements[0];
        var tr = document.createElement('tr');
        for (var head_info of table_info['head']) {
            var th = document.createElement('th');
            if ('name' in head_info) {
                var text = document.createTextNode(head_info['name']);
                th.append(text);
            }
            if ('width' in head_info) {
                th.setAttribute('width', head_info['width'])
            }
            tr.append(th);
        }
        thead.append(tr);
    }
}

function DataTable_SetData(table_infos, json_data) {
    for (var table_info of table_infos) {
        var table = document.getElementById(table_info['id']);
        var elements = table.getElementsByTagName('tbody');
        if (elements.length != 1) {
            alert('<tbody> not exist.');
            return;
        }
        var tbody = elements[0];
        tbody.textContent = "";

        var data_list = json_data[table_info['data_id']];
        for (item of data_list) {
            var tr = document.createElement("tr");
            for (var col_info of table_info['data']) {
                var td = document.createElement("td");
                var class_val = '';
                var is_minus = false;
    
                if ('name' in col_info) {
                    var val = item[col_info['name']];
                    if ('format_number' in col_info) {
                        if (val < 0)
                            is_minus = true
                        options = col_info['format_number']
                        val = new Intl.NumberFormat('ko-KR', options).format(val);
                    }
                    var text = document.createTextNode(val);
                    td.append(text);
                }
                if ('align' in col_info) {
                    if (col_info['align'] == 'left')
                        class_val = class_val + " text-start";
                    else if (col_info['align'] == 'center')
                        class_val = class_val + " text-center";
                    else if (col_info['align'] == 'right')
                        class_val = class_val + " text-end";
                }
                if ('minus' in col_info && is_minus) {
                    class_val = class_val + " text-" + col_info['minus'];
                }
    
                if (0 < class_val.length)
                    td.setAttribute("class", class_val)
                tr.append(td);
            }
            tbody.append(tr);
        }
    }
}

function DataTable_GetJsonData(url, send_data, success_func) {
    $.ajax({
        type: "POST",
        url: url,
        data: send_data,
        dataType: "json",
        success: function (response) {
            if (response.result == "Success") {
                success_func(response);
            }
            else { alert(response.result); }
        },
        error: function (request, status, error) { alert(error); },
    });
}
