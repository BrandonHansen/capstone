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

	// Send song to the program
	// Prints to input.txt file, and the program will read from this file
	//<?php
	$inputfile=fopen("./../../input.txt","w");
	fwrite($inputfile,"play,");
	fwrite($inputfile,songName);
	fclose($inputfile);
	//?>

	// Show results on the screen
	var $table=document.getElementById('song-table');
	var myInterval = setInterval(myTimer,10);
	function myTimer() {
		var tableLen=$table.rows.length;
		var noteNum=$table.rows[$table.rows.length-1].cells[0].childNodes[0].value;
		//<?php
		$outputfile=fopen("./../../output.txt","r");
		var pieces="";
		if ($outputfile) {
			fseek($outputfile, -1, SEEK_END); 
			var $pos = ftell($outputfile);
			var $LastLine = "";
			var $C="";
			while((($C = fgetc($outputfile)) != "\n") && ($pos > 0)) {
				$LastLine = $C.$LastLine;
				fseek($outputfile, $pos--);
			}
			fclose($outputfile);
			pieces=$LastLine.split(",");
		}
		//?>
		if ((pieces != "") && (pieces[0] == "f")) {
			clearInterval(myInterval);
		}
		if ((pieces != "") && (pieces[0] == "1") && (noteNum != "1")) {
			$table.deleteRow(-1);
		}
		if ((pieces != "") && (noteNum != pieces[0])) {
			var row=$table.insertRow(-1);
			var cell1=row.insertCell(0);
			cell1.innerHTML=pieces[0];
			var cell2=row.insertCell(1);
			cell2.innerHTML=pieces[1];
			var cell3=row.insertCell(2);
			cell3.innerHTML=pieces[2];
			var cell4=row.insertCell(3);
			cell4.innerHTML=pieces[3];
			var cell5=row.insertCell(4);
			cell5.innerHTML=pieces[4];
			var cell6=row.insertCell(5);
			cell6.innerHTML=pieces[5];
		}
	}
}

