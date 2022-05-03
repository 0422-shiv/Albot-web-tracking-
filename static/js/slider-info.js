var shadow = '0 20px 50px rgba(0,34,45,0.5)';

function styles(item_id, x, y, z , opacity, shadow){
	$(item_id).css({
		transform: 'translate3d('+ x +'px, ' + y + 'px, ' + z +'px) ',
		opacity: opacity,
		'box-shadow': shadow
	});
}

$('#one').click(function(){
	$('#one').addClass('focus');
	$('#two').removeClass('focus');
	$('#three').removeClass('focus');
	styles('#first', 0, 0, 0, 1, shadow);
	styles('#second', 70, -80, -50, 0.6, 'none');
	styles('#third', 110, 80, -60, 0.1, 'none');
}); 


$('#two').click(function(){
	$('#one').removeClass('focus');
	$('#two').addClass('focus');
	$('#three').removeClass('focus');
	styles('#first', 110, 80, -60, 0.1, 'none');
	styles('#second', 0, 0, 0, 1, shadow);
	styles('#third', 70, -80, -50, 0.6, 'none');
});
$('#three').click(function(){
	$('#one').removeClass('focus');
	$('#two').removeClass('focus');
	$('#three').addClass('focus');
	styles('#first', 70, -80, -50, 0.6, 'none');
	styles('#second', 110, 80, -60, 0.1, 'none');
	styles('#third', 0, 0, 0, 1, shadow);
});