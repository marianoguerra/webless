var ws = {};
ws.base = location.protocol + "//" + location.host + "/";

ws.PUT = function (url, data, okCb, errorCb, type) {
    ws.requestData("PUT", url, data, okCb, errorCb, type);
};

ws.POST = function (url, data, okCb, errorCb, type) {
    ws.requestData("POST", url, data, okCb, errorCb, type);
};

ws.GET = function (url, okCb, errorCb, type) {
    ws.request("GET", url, okCb, errorCb, type);
};

ws.DELETE = function (url, okCb, errorCb, type) {
    ws.request("DELETE", url, okCb, errorCb, type);
};

ws.request = function(type, url, success, error, datatype) {
    if (url.substr(0, 1) !== "/") {
        url = ws.base + url;
    }

    $.ajax({
        "type": type,
        "url": url,
        "dataType": datatype || "json",
        "success": success,
        "error": error
    });
};

ws.requestData = function(type, url, data, success, error, datatype) {
    data = JSON.stringify(data);
    if (url.substr(0, 1) !== "/") {
        url = ws.base + url;
    }

    $.ajax({
        "type": type,
        "contentType": "application/json",
        "url": url,
        "data": data,
        "dataType": datatype || "json",
        "success": success,
        "error": error
    });
};
