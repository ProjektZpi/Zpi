

function comment(url)
{
		var comment=$('#textarea_comment').val();
		var event_id=$('#event_id').val();

		$.post(url, {
			comment : comment,
			event_id : event_id,
		}, function(data) {
		$("#comments").fadeOut(0,function(){
		$(this).html(data.content).fadeIn(1500);
		}); 
		
		
		});

}
	

