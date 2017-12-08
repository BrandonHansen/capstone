"use strict";

console.log("OUTSIDE");

function getParameterByName(name,url) {
	if (!url) url = window.location.href;
	name= name.replace(/[/[/]]/g,"\\$&");
	var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
		results = regex.exec(url);
	if (!results) return null;
	if (!results[2]) return '';
	return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function useForm() {
	console.log("INSIDE");
	// Read data from the form
	var songName=getParameterByName('mySong');
	var xhr_put = new XMLHttpRequest();
	xhr_put.open("PUT","http://127.0.0.1:8080/song", true);
	xhr_put.send(songName);
	xhr_put.onload=function(){
		console.log("success");
	}
	// SEND SONG NAME TO SERVER

	// Show results on the screen
	var $table=document.getElementById('song-table');
	var myInterval = setInterval(myTimer,200);
	var contentAdded = 0;
	var noteNumber=0;
	var done=0;
	function myTimer() {
		var tableLen=$table.rows.length;
		if (contentAdded == 0) {
			var noteNum=$table.rows[$table.rows.length-1].cells[0].childNodes[0].value;
		} else if (contentAdded == 1) {
			var noteNum=$table.rows[$table.rows.length-1].cells[0].innerHTML;
		}
		//console.log("_______________________");
		//console.log(noteNum);
		var pieces = "";
		var prevNoteNumber = 0;

		// SEND GET TO SERVER
		var xhr = new XMLHttpRequest();
		xhr.open("GET", "http://127.0.0.1:8080/", true);
		xhr.onload = function() {
			//console.log(xhr.responseText);
			pieces = $.csv.toArrays(xhr.responseText);
			//console.log(String(pieces[0][0]));
			if ((pieces[0] != "") && (String(pieces[0][1]) == "f")) {
				clearInterval(myInterval); // Stop myTimer()
				done=1;
			}
			if ((pieces[0] != "") && (String(pieces[0][0]) == "1") && (noteNum != "1")) {
				$table.deleteRow(-1); // Deletes loading bar
				contentAdded=1;
			}
			console.log(Number(pieces[0][0]));
			if ((pieces[0] != "") && (Number(pieces[0][0]) != Number(noteNum)) && (done==0)) {
				var row=$table.insertRow(-1);
				var cell1=row.insertCell(0);
				cell1.innerHTML=pieces[0][0];
				var cell2=row.insertCell(1);
				cell2.innerHTML=pieces[0][1];
				var cell3=row.insertCell(2);
				cell3.innerHTML=pieces[0][2];
				var cell4=row.insertCell(3);
				cell4.innerHTML=pieces[0][3];
				var cell5=row.insertCell(4);
				cell5.innerHTML=pieces[0][4];
				var cell6=row.insertCell(5);
				cell6.innerHTML=pieces[0][5];
				noteNumber=noteNumber+1;
				console.log(noteNumber);
				console.log(Number(pieces[0][0]));
			}
		};
		xhr.send();



	}
}

