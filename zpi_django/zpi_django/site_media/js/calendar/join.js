	function join(url)
	{		
			var event_id=$('#event_id').val();
			$.post(url, {
				event_id : event_id,
				}, function(data) {
		  			$("#join").html("<p id='joined'>Zostałeś zapisany do wydarzenia</p>");
			});

	}	
	

