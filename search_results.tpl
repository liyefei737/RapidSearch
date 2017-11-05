<!DOCTYPE html>
<html lang='en'>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
		<meta http-equiv="Pragma" content="no-cache"/>
		 <meta http-equiv="Expires" content="0"/>
		<title>Search Results</title>
	</head>
	<div class="searchFunction">
 			<form action="/" method="get">
				<input type="text" name="keywords"/>
				<input type="submit" value="Crawl"/>
				<input type="submit" value="home"/>
			</form>
 	</div>
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
</html>