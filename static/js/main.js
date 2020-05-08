var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    mode: {name: "python",
           version: 3,
           singleLineStringErrors: false},
    lineNumbers: true,
    indentUnit: 0,
    extraKeys: {"Ctrl-Space": "autocomplete"},
    matchBrackets: true
});

CodeMirror.commands.autocomplete = function(cm) {
     CodeMirror.simpleHint(cm, CodeMirror.pythonHint);
}

$("#submit").click(function() {
	var code = editor.getValue() + "\n";
	$.ajax({
		url: "/run",
		type: "post",
		dataType: "json",
		data: {"code": code},
		success: function(result) {
			alert(result.done);
		}
	});
});
