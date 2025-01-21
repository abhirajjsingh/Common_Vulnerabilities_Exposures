# CVE API Documentation

This repository provides an API to retrieve and filter CVE (Common Vulnerabilities and Exposures) data from the National Vulnerability Database (NVD). The data is stored in an SQLite database and can be accessed and filtered through various endpoints.

Here's the video demo for whole: https://drive.google.com/file/d/1Q_W_p2vIvf9n32AiUj_irtVaqyJdgVmN/view?usp=sharing

## **API Endpoints**

### **1. Rendering the Homepage (/)**
- **Route**: `GET /`
- **Description**: Renders the homepage with a table displaying the CVE data.
- **Response**: An HTML page showing CVE data in a table.

### **2. Fetching CVEs in JSON Format (/api/cves)**
- **Route**: `GET /api/cves`
- **Description**: Retrieves all CVE entries from the database in JSON format.
- **Response**: A JSON array of CVEs.
  ```json
  [
    {
      "id": "CVE-2021-34527",
      "description": "Windows Print Spooler Remote Code Execution Vulnerability",
      "published": "2021-07-06",
      "last_modified": "2021-07-06",
      "cvss_score": 8.8
    },
    ...
  ]
  ```

### **3. Rendering CVE Data in HTML Format (/cves)**
- **Route**: `GET /cves`
- **Description**: Renders a list of CVEs in an HTML table format.
- **Response**: An HTML page displaying the CVE data.

### **4. Syncing CVE Data from the NVD API (/api/cves/sync)**
- **Route**: `GET /api/cves/sync`
- **Description**: Fetches CVE data from the NVD API and stores it in the database.
- **Response**:
  - **200 OK**: 
    ```json
    { "message": "CVE data synchronized successfully" }
    ```
  - **500 Internal Server Error**: 
    ```json
    { "message": "Error: <error_message>" }
    ```

### **5. Fetching a Specific CVE by ID (/api/cves/<cve_id>)**
- **Route**: `GET /api/cves/<string:cve_id>`
- **Description**: Retrieves detailed information for a specific CVE by its ID.
- **Response**:
  - **200 OK**:
    ```json
    {
      "id": "CVE-2021-34527",
      "description": "Windows Print Spooler Remote Code Execution Vulnerability",
      "published": "2021-07-06",
      "last_modified": "2021-07-06",
      "cvss_score": 8.8
    }
    ```
  - **404 Not Found**:
    ```json
    { "message": "CVE not found" }
    ```

### **6. Filtering CVEs by Published Date or CVSS Score (/api/cves/filter)**
- **Route**: `GET /api/cves/filter`
- **Description**: Filters CVEs by their published date or CVSS score.
- **Query Parameters**:
  - `published` (string): The published date of the CVE (e.g., "2021-07-06").
  - `min_cvss` (float): Minimum CVSS score (e.g., 5.0).
  - `max_cvss` (float): Maximum CVSS score (e.g., 9.0).
- **Example Request**:
  ```
  GET /api/cves/filter?published=2021-07-06&min_cvss=7.0
  ```
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": "CVE-2021-34527",
        "description": "Windows Print Spooler Remote Code Execution Vulnerability",
        "published": "2021-07-06",
        "last_modified": "2021-07-06",
        "cvss_score": 8.8
      },
      ...
    ]
    ```

### **7. A Test Route for Ensuring the API is Running (/test)**
- **Route**: `GET /test`
- **Description**: A simple test route to verify that the API is running.
- **Response**:
  - **200 OK**:
    ```json
    { "message": "CVE API is running!" }
    ```

---

## **Test Cases**

Here are some test cases to verify the correctness of your filtering functionality:

### **1. test_get_cves_no_filter**
- **Description**: Verifies that the `/api/cves/filter` route works without any filters and returns a list of CVEs.
- **Expected Result**: A list of CVEs is returned without any filters.

### **2. test_filter_by_cvss_score**
- **Description**: Tests the filtering functionality by CVSS score, using both a minimum and maximum value.
- **Example Request**: 
  ```
  GET /api/cves/filter?min_cvss=7.0&max_cvss=9.0
  ```
- **Expected Result**: Only CVEs with CVSS scores between 7.0 and 9.0 are returned.

### **3. test_filter_by_published_date**
- **Description**: Tests filtering by the `published` date.
- **Example Request**: 
  ```
  GET /api/cves/filter?published=2021-07-06
  ```
- **Expected Result**: Only CVEs published on "2021-07-06" are returned.

### **4. test_filter_by_both**
- **Description**: Tests filtering by both the `published` date and the `cvss_score`.
- **Example Request**:
  ```
  GET /api/cves/filter?published=2021-07-06&min_cvss=7.0
  ```
- **Expected Result**: Only CVEs that match both the published date and the minimum CVSS score of 7.0 are returned.

### **5. test_filter_no_match**
- **Description**: Tests a scenario where no CVEs match the filter criteria (e.g., an invalid date or CVSS range).
- **Example Request**:
  ```
  GET /api/cves/filter?published=2021-01-01&min_cvss=10.0
  ```
- **Expected Result**: No CVEs are returned since no CVEs match the given filter criteria.

---

## **How to Use**

1. **Clone the Repository**: Clone the repository to your local machine.
2. **Install Dependencies**: Install the necessary dependencies using:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the App**: Start the Flask app by running:
   ```bash
   python app.py
   ```
4. **Access the API**: The API will be available at `http://localhost:5000`. You can test the endpoints using tools like Postman or by directly entering the URLs in your browser.

---

## **Additional Notes**

- Ensure the CVE data is synchronized before querying for CVEs using `/api/cves` or `/api/cves/{cve_id}`.
- The filtering functionality allows you to filter by the published date and CVSS score range.
- This API provides a simple, robust method for accessing and filtering CVE data for security and vulnerability management purposes.

---
