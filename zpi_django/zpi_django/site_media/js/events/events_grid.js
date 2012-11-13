$(function(){
  $('.grid_right').masonry({
    // options
    itemSelector : '.item',
    columnWidth : 0,
    isAnimated: true
  });
});

$(function(){
	$('.grid_right .item img').mouseover(function(){
	// po najechaniu na obrazek
	}).mouseout(function(){
	// po zjechaniu z obrazka
	});
});

