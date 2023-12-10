

// Get the select element
var selectElement = document.getElementById('mediaDropdown');

// Event listener for select change
function handleSelectChange() {
	var headingElement = document.getElementById('media-heading');
    var subheadingElement = document.getElementById('media-subheading');
	headingElement.innerHTML = ""; // Display heading
    subheadingElement.innerHTML = ""; // Display subheading

	var selectedOption = selectElement.options[selectElement.selectedIndex];

    // Get the text of the selected option
    var selectedText = selectedOption.text;

	// Get the selected value
	console.log(selectedText)
    var selectedValue = selectElement.textContent;

    // Split the selected value by ':'
    var splitValues = selectedText.split(':');
    // Display the heading and subheading
    headingElement.innerHTML = splitValues[0]; // Display heading
    subheadingElement.innerHTML = splitValues[1]; // Display subheading
}

selectElement.addEventListener('change', handleSelectChange);

// Trigger change event manually to display the initial default value
selectElement.dispatchEvent(new Event('change'));


async function callback_media() {
	let column = document.getElementById('mediaDropdown').value;
    console.log(column);
	response = await fetch("/media/generateMediaGraph?column=" + column);
	if (response.ok) {
		let graphJson = await response.json();
		Plotly.newPlot('graph-m', graphJson, {});
	} 
	else {
		alert("HTTP-Error: " + response.status + "on getCharts");
	}
}