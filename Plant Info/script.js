// Fetch data from JSON file
fetch('crop.json')
  .then(response => response.json())
  .then(data => {
    // Store JSON data in a variable
    var crops = data.Crops;

    // Function to search for crop information
    function searchCrop() {
      var cropInput = document.getElementById("cropInput").value.toLowerCase();
      var cropInfo = document.getElementById("cropInfo");
      var found = false;

      for (var crop in crops) {
        if (crop.toLowerCase() === cropInput) {
          cropInfo.innerHTML = "<h2>" + crop + "</h2>" +
                               "<p><strong>Temperature Range:</strong> " + crops[crop].TemperatureRange + "</p>" +
                               "<p><strong>Rainfall Requirement:</strong> " + crops[crop].RainfallRequirement + "</p>" +
                               "<p><strong>Weather Conditions:</strong> " + crops[crop].WeatherConditions + "</p>" +
                               "<p><strong>Care Instructions:</strong> " + crops[crop].CareInstructions + "</p>";
          found = true;
          break;
        }
      }

      if (!found) {
        cropInfo.innerHTML = "<p>Crop not found. Please enter a valid crop name.</p>";
      }
    }

    // Event listener for the "Search" button
    document.getElementById("searchBtn").addEventListener("click", searchCrop);

    // Event listener for Enter key press
    document.getElementById("cropInput").addEventListener("keypress", function(event) {
      if (event.key === "Enter") {
        searchCrop();
      }
    });
  })
  .catch(error => console.error('Error fetching data:', error));