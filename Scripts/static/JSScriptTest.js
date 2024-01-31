document.getElementById('send-query-btn').addEventListener('click', function() {
    sendGPTQuery();
});

// Function to send the GPT query to the Python backend
function sendGPTQuery() {
    const gptQuery = document.getElementById('gpt-query').value;
    if (gptQuery.trim() === '') {
        alert('Please enter a GPT query.');
        return;
    }

    // Make an API request to GPT-3 with the user's query
    fetch('/generate-sql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: gptQuery }),
    })
    .then(response => response.json())
    .then(data => {
        // Display the received SQL query on the web page
        const sqlQueryResult = document.getElementById('sql-query-result');
        sqlQueryResult.textContent = data.sql_query;
        
        // Call the function to create the HTML table from response data
        createTableFromJSON(data.response_data);
    })
    .catch(error => {
        console.error('Error sending GPT query:', error);
    });
}

// Function to create an HTML table from JSON response data
function createTableFromJSON(data) {
    // Parse the JSON data into an array of objects
    const dataArray = data;

    if (dataArray.length === 0) {
        return; // No data to display
    }

    // Determine the headers based on the keys of the first object
    const headers = Object.keys(dataArray[0]);

    // Create the table element
    const table = document.createElement('table');

    // Create the table header row
    const headerRow = document.createElement('tr');
    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.textContent = headerText;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    // Create table rows and populate with data
    dataArray.forEach(dataObject => {
        const row = document.createElement('tr');
        headers.forEach(header => {
            const cell = document.createElement('td');
            cell.textContent = dataObject[header];
            row.appendChild(cell);
        });
        table.appendChild(row);
    });

    // Append the table to a container in your HTML (e.g., a div)
    const tableContainer = document.getElementById('table-container');
    tableContainer.innerHTML = ''; // Clear any previous table
    tableContainer.appendChild(table);
}










