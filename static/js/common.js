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


function DataTable_MakeTHead(table_id, head_infos) {
    var table = document.getElementById(table_id);
    var elements = table.getElementsByTagName('thead');
    if (elements.length != 1) {
        alert('<thead> not exist.');
        return;
    }
    var thead = elements[0];
    var tr = document.createElement('tr');
    for (var head_info of head_infos) {
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

function DataTable_SetData(table_id, col_infos, data_list) {
    var table = document.getElementById(table_id);
    var elements = table.getElementsByTagName('tbody');
    if (elements.length != 1) {
        alert('<tbody> not exist.');
        return;
    }
    var tbody = elements[0];
    tbody.textContent = "";
    for (item of data_list) {
        var tr = document.createElement("tr");
        for (var col_info of col_infos) {
            var td = document.createElement("td");
            if ('name' in col_info) {
                var val = item[col_info['name']];
                if ('format_number' in col_info) {
                    options = col_info['format_number']
                    val = new Intl.NumberFormat('ko-KR', options).format(val);
                }
                var text = document.createTextNode(val);
                td.append(text);
            }
            if ('align' in col_info) {
                if (col_info['align'] == 'left')
                    td.setAttribute("class", "text-start")
                else if (col_info['align'] == 'center')
                    td.setAttribute("class", "text-center")
                else if (col_info['align'] == 'right')
                    td.setAttribute("class", "text-end")
            }
            tr.append(td);
        }
        tbody.append(tr);
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
                success_func(response.data);
            }
            else { alert(response.result); }
        },
        error: function (request, status, error) { alert(error); },
    });
}
