
 	 function count_to_start(year, month, day, hour, minutes)
 	{	
 		hour=parseFloat(hour)+1;
 		month=parseFloat(month)-1;
 		var Now = new Date();
 		var Event_date= new Date(year,month,day,hour,minutes,0,0);
 		
 		var Pozostaly_czas= Event_date-Now;
 		
 		if(Pozostaly_czas>0){
 		
         	var s = Pozostaly_czas / 1000;   // sekundy
	        var min = s / 60;               // minuty
	        var h = min / 60;               // godziny
	        var d =h /24					//dni
	 
	        var sLeft = Math.floor(s  % 60);    // pozosta這 sekund    
	        var minLeft = Math.floor(min % 60); // pozosta這 minut
	        var hLeft = Math.floor(h % 24);          // pozosta這 godzin
	        var dLeft = Math.floor(d);          // pozosta這 godzin
	        
	         
 		
 			if(dLeft>0){
				$('#time_to_start_count').html(dLeft+" dni "+ hLeft+" h "+minLeft+" min "+sLeft+" s");
			}else{
				$('#time_to_start_count').html(hLeft+" h "+minLeft+" min "+sLeft+" s");
			}
		} else{$('#time_to_start').hide();
			}
	};
