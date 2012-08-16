(function($, P){
    'use strict';
    var ws, onopen, onmessage, onclose, onerror, target = $('#livecode code'), h2 = $('h2'), setLanguage;

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
        var obj = JSON.parse(e.data), match;
        target.text($.trim(obj.code));
        match = obj.file.match(/.+\/(.+\.(.+))$/);
        h2.text(match[1]);
        setLanguage(match[2]);
        P.highlightAll();
    };

    setLanguage = function(ext){
        var lang = 'none';
        switch(ext){
            case 'js':
                lang = 'javascript';
                break;
            case 'css':
                lang = 'css';
                break;
            case 'java':
                lang = 'java';
                break;
            case 'html':
                lang = 'markup';
                break;
            default:
                lang = 'none';
        }
        target.removeClass();
        target.addClass('language-' + lang);
    };

    $(function(){
        ws = new WebSocket('ws://localhost:8000');
        ws.onopen = onopen;
        ws.onmessage = onmessage;
        ws.onclose = onclose;
        ws.onerror = onerror;
    });
})(jQuery, Prism);