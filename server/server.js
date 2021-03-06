/*
 * Copyright (C) 2012 Massimiliano Marcon

 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software
 * and associated documentation files (the "Software"), to deal in the Software without restriction,
 * including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:

 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.

 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 * PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
 * FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
 * OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

var express = require('express'),
    app = express.createServer(),
    path = require('path'),
    WS = require('ws').Server,
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz',
    sockets = {};

var generateId = function(){
    return 'ws-' + Math.random().toFixed(3).replace(/\./, '') + '-' + Math.sqrt(Date.now()).toString().replace(/^\d+\./, '');
},
getAllExcept = function(object, key){
    var result = [], k;
    for (k in object) {
        if (object.hasOwnProperty(k) && key !== k) {
            result.push(object[k]);
        }
    }
    return result;
};

app.use(express.bodyParser());
app.listen(8000);
app.use(express.static(path.normalize(__dirname + '/app/')));

var wss = new WS({server: app});
wss.on('connection', function(ws) {
    console.log('WS Connected');
    var id = generateId();
    ws._id = id;
    sockets[id] = ws;
    ws.on('message', function(message) {
        var others = getAllExcept(sockets, this._id);

        others.forEach(function(v){
            try {
                v.send(message);
            } catch(e) {
                console.log('Failed to send message to socket: ' + v._id);
            }
        });
    });
    ws.on('close', function() {
        delete sockets[ws._id];
    });
});