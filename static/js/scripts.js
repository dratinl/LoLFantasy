$(function(){
	$('button').click(function(){
		var user_name = $('#txtUser').val();
		//var user_team = $('#txtTeam').val();
		$.ajax({
			url: '/drafttool',
			data: $('form').serialize(),
			type: 'POST',

			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});