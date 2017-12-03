<!DOCTYPE html>
<html lang='en'>
	<head>
		<meta charset="utf-8">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
		<script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
		<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
		<script src="//code.jquery.com/jquery-1.12.4.js"></script>
  		<script src="//code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  		<link rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.min.css"
  integrity="sha384-OHBBOqpYHNsIqQy8hL1U+8OXf9hH6QRxi0+EODezv82DfnZoV7qoHAZDwMwEJvSw"
  crossorigin="anonymous">
  		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animsition/4.0.2/css/animsition.css" integrity="sha256-eacfEFFt07So0i0jcf0GCoJfYEnTpTelDK3/9zN+P0g=" crossorigin="anonymous" />
  		<script src="https://cdnjs.cloudflare.com/ajax/libs/animsition/4.0.2/js/animsition.min.js" integrity="sha256-8y2mv4ETTGZLMlggdrgmCzthTVCNXGUdCQe1gd8qkyM=" crossorigin="anonymous"></script>
		<!-- <link rel="stylesheet" href="/static/stylesheet.css"> -->
		<style>
			.jumbotron {
				height: 1000px;
    			background-color: #1d353f;
    			color: #fff;
    			padding: 250px 25px;
			}
			.navbar{
				margin-bottom: 0;
				z-index: 9999;
      			border: 0;
      			font-size: 12px !important;
      			line-height: 1.42857143 !important;
      			letter-spacing: 1px;
      			border-radius: 0;
				position: fixed !important;
			}
			 .navbar-nav li a:hover, .navbar-nav li.active a {
      			color: #1d353f !important;
      			background-color: #fff !important;
  			}
		</style>
		<title>Search Engine Frontend</title>
	</head>
 	<body>
 		<nav class="navbar navbar-default navbar-fixed-top navbar-inverse bg-inverse" data-spy="affix" style="background-color: #1d353f;">
 			<div class="container">
 				<div class="navbar-header">
	 				<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
	 					<span class="icon-bar"></span>
	 					<span class="icon-bar"></span>
	 				</button>
	  				<a class="navbar-brand" style="color:white" href="/"><img src="/static/logo.png" width="20" height="20" class="d-inline-block align-top" alt=""></a>
	  			</div>
	  			<div class="collapse navbar-collapse" id="myNavbar">
      				<ul class="nav navbar-nav navbar-right">
      					<li><a href="#news">NEWS</a></li>
				        <li><a href="#howto">HOW TO</a></li>
				        <li><a href="#about">ABOUT</a></li>
				        <li><a href="#login">LOGIN</a></li>
			      	</ul>
   				</div>
  			</div>
		</nav>

		<div class="jumbotron text-center">
			<h1 class="animated bounceInDown">RapidCrawl</h1><br>
			<form  action="/" method="get" class="form-inline" id="myForm" onsubmit="loadIt()">
				<div class="input-group">
					<input type="text" class="animated fadeIn form-control" id="autocomplete" size="100" placeholder="Start Typing to Search" name="keywords" required/>
					<div class="input-group-btn">
        				<button type="submit" class="animated fadeIn btn btn-primary">Crawl!</button>
      				</div>
      			</div>
      		</form>

			%if loggedin and name:
				<div style="left: 100%">
					<h1 style="color:white;"> Welcome {{name}}!</h1>
					<p style="color:white;">{{email}}</p>
					<form action="/logout" method="get">
						<input type="submit" value="Logout"/><br>
					</form>
				</div>
			%elif loggedin:
				<div style="top: 10%">
					<h1 style="color:white;"> Welcome!</h1>
					<p style="color:white;">{{email}}</p>
					<form action="/logout" method="get">
						<input type="submit" value="Logout"/><br>
					</form>
				</div>
			%end
		</div>
		<div id="searchResult"></div>

		<script>

			/*start typing without having to focus on the search bar*/
			var $search = $("#autocomplete");

			$(document).on("keydown", function(e) {
			  if (!$search.is(":focus"))
			    if (e.which != 9 && e.which != 13)
			      $search.focus();
			});

			/*search word suggestion*/
			var tags = null;
			$.getJSON("/lexicon.json", function(data) {
				tags = data;
    			console.log(data);//output your data to console
			});
			$( "#autocomplete" ).autocomplete({
  				source: function( request, response ) {
          			var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( request.term ), "i" );
          			response( $.grep( tags, function( item ){
              			return matcher.test( item );
          			}));
      			}
			});

			/*inject search results*/
			// function loadIt() {
			// 	var inVal = $('#autocomplete').val()
	  //           $.ajax({
	  //               url: '/&keywords=' + inVal + '&page_no=1',
	  //               cache: false,
	  //               success: function (data) {
	  //                   $("#searchResult").empty();
	  //                   $("#searchResult").html(data).slideDown();
	  //               },
	  //               error: function () {
	  //                   alert("something went wrong");
	  //               }
	  //           });
	  //       }

			$( "#autocomplete" ).submit(function( event ) {
				var inVal = $(this).val
				$('#myForm').attr('action', '/&keywords=' + inVal + '&page_no=1')
			});
			// $("#autocomplete").submit( function() {
   //  			$('html, body').animate({
   //       			scrollTop: $("#searchResult").offset().top
   //  			}, 2000);
   //  			return false;
			// });

		</script>
	</body>

</html>