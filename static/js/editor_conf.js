// referencia a codemirror: https://codemirror.net/doc/manual.html
CodeMirror.fromTextArea(document.getElementById("entrada"),{
    lineNumbers : true,
    theme:'material-palenight',
    mode : 'julia',
    matchBrackets: true
});
CodeMirror.fromTextArea(document.getElementById("salida"),{
    lineNumbers : true,
    theme:'material-palenight',
    mode : 'go',
    matchBrackets: true
});