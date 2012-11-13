	 $(document).ready(function() {
		if( $('#id_photo').val().length == 0 ) {
			$('#id_photo2').hide();
			$('#id_description_photo2').hide();
			$('label[for=photo2]').hide();
			$('label[for=description_photo2]').hide();
		}	
		
		if( $('#id_photo2').val().length == 0 ) {
			$('#id_photo3').hide();
			$('#id_description_photo3').hide();
			$('label[for=photo3]').hide();
			$('label[for=description_photo3]').hide();
		}	
		
		if( $('#id_photo3').val().length == 0 ) {
			$('#id_photo4').hide();
			$('#id_description_photo4').hide();
			$('label[for=photo4]').hide();
			$('label[for=description_photo4]').hide();
		}	
		
		$("#id_photo").change(function() {	
			if( $('#id_photo').val().length == 0 ) {
				$('#id_photo2').hide();
				$('#id_description_photo2').hide();
				$('label[for=photo2]').hide();
				$('label[for=description_photo2]').hide();
			}
			
			if( $('#id_photo').val().length > 0 ) {
				$('#id_photo2').show();
				$('#id_description_photo2').show();
				$('label[for=photo2]').show();
				$('label[for=description_photo2]').show();
			}
		 });
		 
		 $("#id_photo2").change(function() {	
			if( $('#id_photo2').val().length == 0 ) {
				$('#id_photo3').hide();
				$('#id_description_photo3').hide();
				$('label[for=photo3]').hide();
				$('label[for=description_photo3]').hide();
			}
			
			if( $('#id_photo2').val().length > 0 ) {
				$('#id_photo3').show();
				$('#id_description_photo3').show();
				$('label[for=photo3]').show();
				$('label[for=description_photo3]').show();
			}
		 });
		 
		 		 
		 $("#id_photo3").change(function() {	
			if( $('#id_photo3').val().length == 0 ) {
				$('#id_photo4').hide();
				$('#id_description_photo4').hide();
				$('label[for=photo4]').hide();
				$('label[for=description_photo4]').hide();
			}
			
			if( $('#id_photo3').val().length > 0 ) {
				$('#id_photo4').show();
				$('#id_description_photo4').show();
				$('label[for=photo4]').show();
				$('label[for=description_photo4]').show();
			}
		 });				
	   });	
	   
