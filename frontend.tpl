<!DOCTYPE html>
<html lang='en'>
	<head>
		<meta charset="utf-8">
		<link rel="stylesheet" href="/static/stylesheet.css">
		<title>Search Engine Frontend</title>
	</head>
 	<body>
		<img class="logo" id="logo" src="/static/logo.png" width="27%" height="40%">
		<div class="searchFunction">
			<br>
			<form action="/" method="get">
				<input type="text" name="keywords"/><br>
				<input type="submit" value="Crawl"/><br>
			</form>
			%if not loggedin: 
			<form action="/login" method="get">
				<input type="submit" value="Login With Google"/><br>
			</form>
			%end
		</div>
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
	</body>

</html>