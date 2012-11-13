$(function() { $(".datepicker").datepicker({ dateFormat: 'yy-mm-dd' }); });

$(function() {
	$('label').each(function(){
		$(this).html( $(this).html().replace('*','<span class="star">*</span>') )
	});

})