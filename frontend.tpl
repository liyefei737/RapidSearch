<!DOCTYPE html>
<html lang='en'>
	<head>
		<meta charset="utf-8">
		<link rel="stylesheet" href="/static/stylesheet.css">
		<title>Search Engine Frontend</title>
	</head>
 	<body>
 		<img id="logo" src="/static/logo.png" width="40%" height="45%" style= "position: absolute; top: 15px; left: 480px;">
		<div class="searchFunction">
			
			<form action="/" method="get">
				<input type="text" name="keywords"/><br>
				<input type="submit" value="Crawl"/><br>
			</form>
			%if loggedin :
				<form action="/logout" method="get">
				<input type="submit" value="Logout"/><br>
			</form>
			%else: 
			<form action="/login" method="get">
				<input type="submit" value="Login With Google"/><br>
			</form>
			%end
		</div>
		%if loggedin and name:
			<div>
				<h1 style="color:white;"> Welcome {{name}}!</h1>
				<p style="color:white;">{{email}}</p>
			</div>
		%elif loggedin:
			<div>
				<h1 style="color:white;"> Welcome!</h1>
				<p style="color:white;">{{email}}</p>
			</div>
		%end
	</body>

</html>