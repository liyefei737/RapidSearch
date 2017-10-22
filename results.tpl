<!DOCTYPE html>
<html lang='en'>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
		<meta http-equiv="Pragma" content="no-cache"/>
		 <meta http-equiv="Expires" content="0"/>
		<title>Results Page</title>
	</head>
 	<body>
 		%if logged_in and name:
 		<h1> {{name}}, here are your search results </h1>
 		%else:
 		<h1> Here are your search results </h1>
 		%end
 		<p> Search for "{{inputString}}" </p>
 		<table border='1' style='width: 200px' id='search_string_occurence'>
 			<caption> Words and Their Occurences in the Search String </caption> 
 			<thead>
 				<tr>
 					<th>Word</th>
 					<th>Count</th>
 				</tr>
 			</thead>
 			%for word in splitInput:
 			<tr>
 				<td align='center'>{{word}} </td> 
 				<td align='center'>{{occurence_dict[word]}}</td> 
 			</tr>
 			%end
 			</table><br>
 			<div></div>
 			%if logged_in:
 			<table border='1' style='width: 200px'id='top_twenty'>
 				<caption> History Top 20 Search Words </caption>
 				<thead>
 					<tr>
 						<th>Word</th>
 						<th>Count</th>
 					</tr>
 				</thead>
 				%for count, w in reversed_copy_heap:
 				<tr>
 					<td align='center'>{{w}}</td> 
 					<td align='center'>{{count}}</td> 
 				</tr>
 				%end
 			</table><br>
 			<div></div>
 			<table border='1' style='width: 200px'id='top_twenty'>
 				<caption> Top 10 Most Recent Searches </caption>
 				<thead>
 					<tr>
 						<th>Rank</th>
 						<th>Search</th>
 					</tr>
 				</thead>
 				%for i in range(1,len(queue)+1):
 				<tr>
 					<td align='center'>{{i}}</td>
 					<td align='center'>{{queue[-i]}}</td> 
 				</tr>
 				%end
 			</table><br>
 			<div>
 				<form action="/logout" method="get">
				<input type="submit" value="Logout"/><br>
 			</div>
 			%end
	</body>

</html>