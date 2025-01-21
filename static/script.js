// Global variables
let currentPage = 1;
let resultsPerPage = 10;
let totalRecords = 0;

// DOM Elements
const cveTableBody = document.getElementById('cveTableBody');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');
const totalRecordsElement = document.getElementById('totalRecords');
const prevPageButton = document.getElementById('prevPage');
const nextPageButton = document.getElementById('nextPage');
const pageInfoElement = document.getElementById('pageInfo');
const resultsPerPageSelect = document.getElementById('resultsPerPage');

// Fetch CVE data from the API
async function fetchCVEs() {
    try {
        loadingElement.style.display = 'block';
        errorElement.style.display = 'none';
        cveTableBody.innerHTML = '';

        const startIndex = (currentPage - 1) * resultsPerPage;
        
        // Fetch data from the local API
        const response = await fetch(`http://127.0.0.1:5000/api/cves?startIndex=${startIndex}&resultsPerPage=${resultsPerPage}`);

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        totalRecords = data.length || 0;
        updateUI(data);
    } catch (error) {
        showError('Failed to fetch CVE data. Please try again later.');
    } finally {
        loadingElement.style.display = 'none';
    }
}

// Update the UI with CVE data
function updateUI(cves) {
    // Update total records
    totalRecordsElement.textContent = totalRecords.toLocaleString();

    // Update table
    cveTableBody.innerHTML = cves.map(item => `
        <tr>
            <td>${item.id}</td>
            <td>${item.description?.substring(0, 100) || ''}...</td>
            <td>${formatDate(item.published)}</td>
            <td>${formatDate(item.last_modified)}</td>
            <td>${item.cvss_score || 'N/A'}</td>
        </tr>
    `).join('');

    // Update pagination
    updatePagination();
}

// Format date string
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString();
}

// Show error message
function showError(message) {
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

// Update pagination controls
function updatePagination() {
    const totalPages = Math.ceil(totalRecords / resultsPerPage);
    pageInfoElement.textContent = `Page ${currentPage} of ${totalPages}`;
    prevPageButton.disabled = currentPage === 1;
    nextPageButton.disabled = currentPage * resultsPerPage >= totalRecords;
}

// Event Listeners
prevPageButton.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        fetchCVEs();
    }
});

nextPageButton.addEventListener('click', () => {
    currentPage++;
    fetchCVEs();
});

resultsPerPageSelect.addEventListener('change', (e) => {
    resultsPerPage = parseInt(e.target.value);
    currentPage = 1;
    fetchCVEs();
});

// Function to show CVE details (you can implement this based on your requirements)
function showCVEDetails(cveId) {
    // For now, we'll just alert the CVE ID
    alert(`Clicked CVE: ${cveId}`);
    // You can implement a modal or navigate to a details page
}

// Initial load
fetchCVEs();