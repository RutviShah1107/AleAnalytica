
async function callback() {
	response = await fetch("/display/generateDendogram?p=" + 8);
	if (response.ok) {
		let dendogramJson = await response.json();
		Plotly.newPlot('dendogram-chart', dendogramJson, {});
	} 
	else {
		alert("HTTP-Error: " + response.status + "on getCharts");
	}
}


async function callback_demographic() {
	response = await fetch("/demographic/generateDemographicGraph");
	if (response.ok) {
		let graphJson = await response.json();
		Plotly.newPlot('graph-age', graphJson['Age'], {});
		Plotly.newPlot('graph-gender', graphJson['Gender'], {});
		Plotly.newPlot('graph-ethinicity', graphJson['Ethinicity'], {});
		Plotly.newPlot('graph-marital-status', graphJson['MaritalStatus'], {});
		Plotly.newPlot('graph-employment-status', graphJson['EmploymentStatus'], {});
		Plotly.newPlot('graph-education', graphJson['Education'], {});
		Plotly.newPlot('graph-living-area', graphJson['LivingArea'], {});
		Plotly.newPlot('graph-hhi', graphJson['HHI'], {});

	} 
	else {
		alert("HTTP-Error: " + response.status + "on generateDemographicGraph");
	}
}

