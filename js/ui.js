var ui = {};

ui.getValues = function () {
    var url = $('#url').val().trim(), code = $('#code').val().trim();

    if (code === '' || url === '') {
        alert("some field empty");
        return null;
    }

    return {'url': url, 'code': code};
};

ui.sendCode = function () {
    $('#send-result,#test-result').html('');
    ui.doRequest(ui.sendCodeReq, ui.putResponseIn('send-result'),
            ui.errorCb('error sending code'));
};

ui.sendCodeReq = function(values, okCb, errorCb) {
    ws.POST("/", values, okCb, errorCb, "html");
};

ui.testCode = function () {
    $('#send-result,#test-result').html('');
    ui.doRequest(ui.testCodeReq, ui.putResponseIn('test-result'),
            ui.errorCb('error sending code'));
};

ui.testCodeReq = function(values, okCb, errorCb) {
    ws.POST("/test", values, okCb, errorCb, "html");
};

ui.doRequest = function (action, okCb, errorCb) {
    var values = ui.getValues();

    if (values !== null) {
        action(values, okCb, errorCb);
    }
};

ui.putResponseIn = function (id) {
    return function (response) {
        console.log(response);
        $('#' + id).html(response);
    };
};

ui.error = function (msg) {
    alert(msg);
};

ui.errorCb = function (msg) {
    return function() {
        ui.error(msg);
    }
};
