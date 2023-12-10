
// Get the select element
var selectElement = document.getElementById('occasionDropdown');

// Event listener for select change
function handleSelectChange() {
	var headingElement = document.getElementById('occasion-heading');
    var subheadingElement = document.getElementById('occasion-subheading');
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


async function callback_occasion() {
	let column = document.getElementById('occasionDropdown').value;
	response = await fetch("/occasion/generateOccasionGraph?column=" + column);
	if (response.ok) {
		let graphJson = await response.json();
		Plotly.newPlot('graph-o', graphJson, {});
	} 
	else {
		alert("HTTP-Error: " + response.status + "on getCharts");
	}
}