
	function add_feedback(url)
	{		
			
			var event_id=$('#event_id').val();
			$.post(url, {
				atmosphere : $('input:radio[name=rate_atmosphere]:checked').val(),
				organisation: $('input:radio[name=rate_organisation]:checked').val(),
				event_id : event_id,
				}, function(data) {
		  			$('#atmosphere_avg').html("<p style='font-size: 0.85em; color: #7B7B7B;'>Aktualna średnia to:</p>");
		  			$('#atmosphere_number').html(data.atmosphere_number);
		  			$('#organisation_avg').html("<p style='font-size: 0.85em; color: #7B7B7B;'>Aktualna średnia to:</p>");
		  			$('#organisation_number').html(data.organisation_number);
		  			$('#add_feedback').html("<p id='feedback_error'>Dziękujemy za ocenę wydarzenia</p>");
			});

	}	
	

