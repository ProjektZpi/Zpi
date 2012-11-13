	$(document).ready(function(){
		$('#login-trigger').click(function(){
			$(this).next('#login-content').slideToggle(400);
			$(this).toggleClass('active');					
			
			if ($(this).hasClass('active')) $(this).find('span').html('&#x25B2;')
			else $(this).find('span').html('&#x25BC;')
		})
		
		/* LOGOWANIE AJAXOWE */
		$("#login_form").submit(function(event) {
		    event.preventDefault(); 
		    var $form = $( this ), url = $form.attr( 'action' );
		
           $.ajax({
                url : url,
                type : 'POST',
                data : $form.serialize(),
                dataType : 'json',
                success : function(data) { 
                	// Je¿eli zalogowano
                	if(data.response == ""){
                		$(window.location).attr('href', '/');
                	} else {
                		$(".error").empty().append(data.response);
                	}
				}
		  });
		});
	})