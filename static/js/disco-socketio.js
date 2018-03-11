var socket;

$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
// rick roll
  socket.on('update', function(data) {
  	if (data.msg == "on") {
  		console.log(data.msg)
  	$('#rickroll').append("<h1>LET'S GET READY TO RUMBLE!!!</h1>");
  	$('#rickroll').append("<iframe width='100%' height='400' src='https://www.youtube.com/embed/DLzxrzFCyOs?rel=0&amp;controls=0&amp;showinfo=0&autoplay=1' frameborder='0' allow='autoplay; encrypted-media' allowfullscreen></iframe>");
  	} else {
  		console.log(data.msg);
  		$('#rickroll')[0].innerHTML="";
  	}
  });
});

