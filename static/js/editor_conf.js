// referencia a codemirror: https://codemirror.net/doc/manual.html
var entrada = CodeMirror.fromTextArea(document.getElementById("entrada"),{
    lineNumbers : true,
    theme:'material-palenight',
    autoRefresh: true,
    mode : 'julia',
   // matchBrackets: true
});
var salidas = CodeMirror.fromTextArea(document.getElementById("salida"),{
    lineNumbers : true,
    theme:'material-palenight',
    autoRefresh: true,
    mode : 'go',
    //matchBrackets: true,
});
var consola = CodeMirror.fromTextArea(document.getElementById("consola"),{
    lineNumbers : true,
    theme:'material-palenight',
    autoRefresh: true,
    mode : 'powershell',
    readonly: true
    //matchBrackets: true,
});
var opt = CodeMirror.fromTextArea(document.getElementById("opt"),{
    lineNumbers : true,
    theme:'material-palenight',
    autoRefresh: true,
    mode : 'go',
    //matchBrackets: true,
});

entrada.setSize(650,700);
salidas.setSize(650,700);