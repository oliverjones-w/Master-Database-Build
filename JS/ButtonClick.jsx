document.getElementById('fetch-data-btn').addEventListener('click', function() {
    fetchData();
});

function fetchData() {
    fetch('/data')  // The endpoint where your Flask app serves the data
        .then(response => response.json())
        .then(data => {
            displayData(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function displayData(data) {
    const container = document.getElementById('data-container');
    container.innerHTML = '';  // Clear previous data

    // Assuming 'data' is an array of objects
    data.forEach(item => {
        const div = document.createElement('div');
        div.textContent = JSON.stringify(item);  // Format and display your data as needed
        container.appendChild(div);
    });
}
