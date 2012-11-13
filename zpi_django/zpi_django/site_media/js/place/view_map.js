	var marker;
	var start_marker;
	
	function Menu($div){
	  var that = this, 
	      ts = null;
	  
	  this.$div = $div;
	  this.items = [];
	  
	  // create an item using a new closure 
	  this.create = function(item){
	    var $item = $('<div class="item '+item.cl+'">'+item.label+'</div>');
	    $item
	      // bind click on item
	      .click(function(){
	        if (typeof(item.fnc) === 'function'){
	          item.fnc.apply($(this), []);
	        }
	      })
	      // manage mouse over coloration
	      .hover(
	        function(){$(this).addClass('hover');},
	        function(){$(this).removeClass('hover');}
	      );
	    return $item;
	  };
	  this.clearTs = function(){
	    if (ts){
	      clearTimeout(ts);
	      ts = null;
	    }
	  };
	  this.initTs = function(t){
	    ts = setTimeout(function(){that.close()}, t);
	  };
	}
	
	// add item
	Menu.prototype.add = function(label, cl, fnc){
	  this.items.push({
	    label:label,
	    fnc:fnc,
	    cl:cl
	  });
	}
	
	// close previous and open a new menu 
	Menu.prototype.open = function(event){
	  this.close();
	  var k,
	      that = this,
	      offset = {
	        x:0, 
	        y:0
	      },
	      $menu = $('<div id="menu"></div>');
	      
	  // add items in menu
	  for(k in this.items){
	    $menu.append(this.create(this.items[k]));
	  }
	  
	  // manage auto-close menu on mouse hover / out
	  $menu.hover(
	    function(){that.clearTs();},
	    function(){that.initTs(3000);}
	  );
	  
	  // change the offset to get the menu visible (#menu width & height must be defined in CSS to use this simple code)
	  if ( event.pixel.y + $menu.height() > this.$div.height()){
	    offset.y = -$menu.height();
	  }
	  if ( event.pixel.x + $menu.width() > this.$div.width()){
	    offset.x = -$menu.width();
	  }
	  
	  // use menu as overlay
	  this.$div.gmap3({
	    action:'addOverlay',
	    latLng: event.latLng,
	    content: $menu,
	    offset: offset
	  });
	  
	  // start auto-close
	  this.initTs(5000);
	}
	
	// close the menu
	Menu.prototype.close = function(){
	  this.clearTs();
	  this.$div.gmap3({action:'clear', name:'overlay'})
	}	
	
	
	$(document).ready(function(){
			menu = new Menu($("#map")),
			$("#map").gmap3(
				{action:'init',
				 options:{
				 	zoom:14,
				 	center:[lng,lat]
				 },
				 events:{
				 	rightclick:function(map,event){
			//	 		console.log(event);
				 		update_marker(event);
	//			 		marker=event;
				 		menu.open(marker);
				 	},
				 	click:function(){
				 		menu.close();
				 	},
				 	dragstart:function(){
				 		menu.close();
				 	},
				 	zoom_changed:function(){
				 		menu.close;
				 	}
				 },
				 				
			},
			{
				action:'addMarker',
				latLng:[lng,lat],
				callback:function(results){
					start_marker=results;
				}
			},
			{ action:'addDirectionsRenderer',
            	preserveViewport: true,
           		markerOptions:{
              	visible: false
            }
          },
          // add a direction panel
          { action:'setDirectionsPanel',
            id : 'directions'
          }
          );
			$('#address').autocomplete({
			  source: function() {
			    $("#map").gmap3({
			      action:'getAddress',
			      address: $(this).val(),
			      callback:function(results){
			        if (!results) return;
			        $('#address').autocomplete(
			          'display', 
			          results,
			          false
			        );
			      }
			    });
			  },
			  cb:{
			    cast: function(item){
			      return item.formatted_address;
			    },
			    select: function(item) {
			    update_marker(item);
			    add_marker(true);
			    }
			  }
			});		
		
		menu.add('Droga samochodowa', 'itemB',
		function(){
			menu.close();
			add_marker(false);
			console.log(start_marker);
			
          $("#map").gmap3({
            action:'getRoute',
            options:{
              origin:start_marker.getPosition(),
              destination:marker.latLng.toString(),
              travelMode: google.maps.DirectionsTravelMode.DRIVING
            },
            callback: function(results){
              if (!results){
              	console.log("no results");
              	return;
              } 
               $("#map").gmap3({ action: 'setDirections', directions:results});
            }
          });			
			
		});
		 
		// MENU : ITEM 2
		menu.add('Droga tramwajowa', 'itemA separator',
		function(){
			menu.close();
			add_marker(false);
			var link='http://wroclaw.jakdojade.pl/index.html?fc='+lng +':'+lat +
			'&tc='+marker.latLng.lat()+':'+marker.latLng.lng()+'&as=true';
			window.open(link);
		})
		
		function update_marker(item){
			marker=item;
			
			
	//		console.log(marker);
			
		}
		
		function add_marker(isAutocomplete){
			if(marker!=null){
				var clear={action:'clear', name:"marker", tag: 'tag'}
				if(isAutocomplete){
					var latlng=marker.geometry.location;
					
				}
				else{
					var latlng=marker.latLng
				}
				var add={action:'addMarker',
			         	 latLng:latlng,		          
			         	 marker:{
			          		options:{draggable:true},
			          		tag:'tag',
			          		events:{
			          			dragend:function(item){
			          				update_marker(item);
			          			}
			          		},
			          		callback:function(item){
			          	//	update_marker(item);
			          		}},
			         	 map:{center:true},        
			        }
				 $("#map").gmap3(
				 	clear,	
				 	add
				 );
			}
		}		
		
						
		});		