(function($){
    'use strict';
    var ws, onopen, onmessage, onclose, onerror, target = $('#livecode code');

    onopen = function(){
        console.log('Connection opened!');
    };

    onclose = function(){
        console.log('Connection closed!');
    };

    onerror = function(){
        console.log('Connection error!');
    };

    onmessage = function(e){
        target.text($.trim(e.data));  
    };

    $(function(){
        ws = new WebSocket('ws://localhost:8000');
        ws.onopen = onopen;
        ws.onmessage = onmessage;
        ws.onclose = onclose;
        ws.onerror = onerror;
    });
})(jQuery);