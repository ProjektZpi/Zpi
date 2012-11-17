		$(function() {
			$('.month').each(function(){
			    $(this).html( $(this).html().replace('January','Styczeń') );
			    $(this).html( $(this).html().replace('February','Luty') );
			    $(this).html( $(this).html().replace('March','Marzec') );
			    $(this).html( $(this).html().replace('April','Kwiecień') );
			    $(this).html( $(this).html().replace('May','Maj') );
			    $(this).html( $(this).html().replace('June','Czerwiec') );
			    $(this).html( $(this).html().replace('July','Lipiec') );
			    $(this).html( $(this).html().replace('August','Sierpień') );
			    $(this).html( $(this).html().replace('September','Wrzesień') );
				$(this).html( $(this).html().replace('October','Październik') );
				$(this).html( $(this).html().replace('November','Listopad') );
				$(this).html( $(this).html().replace('December','Grudzień') );
				
			});

			$('.mon').each(function(){
			    $(this).html( $(this).html().replace('Mon','Pon'));		
			});
			
			$('.tue').each(function(){
			    $(this).html( $(this).html().replace('Tue','Wt'));		
			});
			
			$('.wed').each(function(){
			    $(this).html( $(this).html().replace('Wed','Śr'));		
			});
			
			$('.thu').each(function(){
			    $(this).html( $(this).html().replace('Thu','Czw'));		
			});
			
			$('.fri').each(function(){
			    $(this).html( $(this).html().replace('Fri','Pt'));		
			});
			
			$('.sat').each(function(){
			    $(this).html( $(this).html().replace('Sat','Sob'));		
			});
			
			$('.sun').each(function(){
			    $(this).html( $(this).html().replace('Sun','Nd'));		
			});


				
		});
		
		

	
