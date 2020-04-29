var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    mode: {name: "python",
           version: 3,
           singleLineStringErrors: false},
    lineNumbers: true,
    indentUnit: 4,
    extraKeys: {"Ctrl-Space": "autocomplete"},
    matchBrackets: true
});
CodeMirror.commands.autocomplete = function(cm) {
     CodeMirror.simpleHint(cm, CodeMirror.pythonHint);
 }