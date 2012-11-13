/* LOGOWANIE AJAXOWE */
$(document).ready(function(){
	$("form.form_in_tabs").submit(function(event) {
		event.preventDefault(); 
		var $form = $( this ), url = $form.attr( 'action' );
		$.ajax({
	    	url : url,
	        type : 'POST',
	        data : $form.serialize(),
	        dataType : 'json',
	        success : function(data) { 
	        	$form.find('div.error').text(data.response);
			}
		});
	});
})