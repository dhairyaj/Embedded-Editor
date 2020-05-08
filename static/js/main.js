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
	var filename = $("#filename").val();

	if(!code || !filename) {
		Swal.fire({
		  icon: 'error',
		  title: 'Error',
		  text: 'Both inputs are required!'
		});
	} else {
		$.ajax({
			url: "/run",
			type: "post",
			dataType: "json",
			data: {"code": code, "filename": filename},
			success: function(result) {
				if(result.icon == 'success') {
					editor.setValue("");
					$("#filename").val("");
				}
				Swal.fire({
					icon: result.icon,
					title: result.title,
					html: "<pre style='text-align: left;'>" + result.text + "</pre>"
				})
			}
		});
	}
});
