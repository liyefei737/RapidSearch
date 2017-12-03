<!DOCTYPE html>
<html lang='en'>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
		<meta http-equiv="Pragma" content="no-cache"/>
		<meta http-equiv="Expires" content="0"/>
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
		<style>
			body { 
    			padding-top: 65px; 
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
		<title>Search Results</title>
	</head>
	<body>
<!-- 		 <nav class="navbar navbar-default navbar-fixed-top navbar-inverse bg-inverse" data-spy="affix" style="background-color: #1d353f;">
 			<div class="container">
 				<div class="navbar-header">
	 				<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
	 					<span class="icon-bar"></span>
	 				</button>
	  				<a class="navbar-brand" style="color:white" href="/"><img src="/static/logo.png" width="20" height="20" class="d-inline-block align-top" alt=""></a>
	  				<form action="/" method="get">
						<input type="text" name="keywords" size="60" id="autocomplete"/>
						<div class="input-group-btn">
        					<button type="submit" class="animated fadeIn btn btn-primary">Crawl!</button>
      					</div>
					</form>
	  			</div>
  			</div>
		</nav> -->
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
			      	<form class="form-inline my-2 my-lg-0">
				     	<input type="text" class="form-control" id="autocomplete" size="50" placeholder="Start Typing to Search" name="keywords" required/>
				     	<button type="submit" class="btn btn-primary">Crawl!</button>
				    </form>
   				</div>
  			</div>
		</nav>
<!-- 		<div class="searchFunction">
	 			<form action="/" method="get">
					<input type="text" name="keywords"/>
					<input type="submit" value="Crawl"/>
					<input type="submit" value="home"/>
				</form>
	 	</div> -->
	 	%if result:
	 	<ul>
	 		%for url,title in zip(URLs, titles):
	 		<li><a href="{{url}}">{{title}}</a></li>
	 		%end
	 	</ul>
	 	<nav class="pagination">
	 		%if page > 1:
	 		<a href="/&keywords={{keywords}}&page_no={{page-1}}">Previous</a>
	 		%end
	 		%if page+1 < length:
	 		<a href="/&keywords={{keywords}}&page_no={{page+1}}">Next</a>
	 		%end
	 	</nav>
	 	%else:
	 	<h1>We Couldn't find anything :(</h1>
	 	%end
	 <script>
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
		</script>
 	</body>
</html>