document.getElementById('fetch-data-btn').addEventListener('click', function() {
    fetchData();
});

function fetchData() {
    fetch('/data')  // The endpoint where your Flask app serves the data
        .then(response => response.json())  // Parse the JSON response
        .then(data => {
            displayData(data);  // Handle the data
        })
        .catch(error => console.error('Error fetching data:', error));  // Handle any errors
}

function displayData(data) {
    const container = document.getElementById('data-container');
    container.innerHTML = '';  // Clear previous content

    // Assuming 'data' is an array of objects
    data.forEach(item => {
        // Create a new div for each item and add it to the container
        const div = document.createElement('div');
        div.textContent = JSON.stringify(item);  // Convert the item to a JSON string for display
        container.appendChild(div);
    });
}
