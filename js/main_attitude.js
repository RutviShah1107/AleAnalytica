
// Get the select element
var selectElement = document.getElementById('attitudesDropdown');

// Event listener for select change
function handleSelectChange() {
	var headingElement = document.getElementById('attitudes-heading');
    var subheadingElement = document.getElementById('attitudes-subheading');
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


async function callback_attitude_heatmaps() {
	let column = document.getElementById('attitudesDropdown').value;
    console.log(column);
	response = await fetch("/attitudes-heatmaps/generateAttitudeGraph?column=" + column);
	if (response.ok) {
		let graphJson = await response.json();
		Plotly.newPlot('graph-att', graphJson, {});
	} 
	else {
		alert("HTTP-Error: " + response.status + "on getCharts");
	}
}


async function callback_attitude_likert() {
	let column = document.getElementById('attitudesLikertDropdown').value;
    console.log(column);
	response = await fetch("/attitudes-likert/generateAttitudeGraph?column=" + column);
	if (response.ok) {
		let graphJson = await response.json();
        for (let i = 1; i < 9; i++) {
            Plotly.newPlot('graph-'+ i, graphJson[i], {});
        }
		
	} 
	else {
		alert("HTTP-Error: " + response.status + ". This column does not have a likert scale");
	}
}