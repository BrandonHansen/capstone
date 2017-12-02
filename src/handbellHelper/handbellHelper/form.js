"use strict";

function useForm () {
	// Assumes input of HTML form:
	// <form id="input-form" >
	// <label for="song-name">Song Name</label>
	// <input type="text" id="song-name" placeholder="Song Name" required>
	// </form>
	// <button id="submit-input" onclick="useForm()">Submit</button>
	// <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

	// Read data from the form
	$inputForm = $('#input-form');
	$songName = $('#song-name');
	$submitButton = $('#submit-input');
	var songName = $songName.val();

	// Hide the form
	$inputForm.hide();
	$songName.val("").blur();
	$submitButton.hide();

	// Run the program
	// Prints to console, and the program running in the program will get this input in order to begin
	console.log("play " + songName);

	// Show results on the screen
	
}
