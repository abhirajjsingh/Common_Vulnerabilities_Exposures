from flask import Flask, jsonify, render_template, request
import requests
import sqlite3
import os
import time

app = Flask(__name__)

# Define the database path (update as needed)
DATABASE = os.path.join(os.path.dirname(__file__), 'cve_database.db')

# Function to connect to the SQLite database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Function to create or alter the database schema
def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Create the table if it does not exist
    c.execute('''CREATE TABLE IF NOT EXISTS cves (
                    id TEXT PRIMARY KEY,
                    description TEXT,
                    published TEXT,
                    last_modified TEXT,
                    cvss_score REAL)''')
    
    # Check if 'published' column exists, and if not, add it
    c.execute("PRAGMA table_info(cves);")
    columns = c.fetchall()
    column_names = [column[1] for column in columns]
    
    if 'published' not in column_names:
        c.execute("ALTER TABLE cves ADD COLUMN published TEXT;")
    
    conn.commit()
    conn.close()

# Fetch CVEs from NVD API and insert into the database
def fetch_and_store_cves(start_index=0, results_per_page=10):
    url = f'https://services.nvd.nist.gov/rest/json/cves/2.0?startIndex={start_index}&resultsPerPage={results_per_page}'
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch CVEs from NVD API: {e}")

    data = response.json()
    cves = data.get('vulnerabilities', [])
    print(f"Fetched {len(cves)} CVEs.")  # Print number of CVEs fetched

    conn = get_db()
    c = conn.cursor()

    for item in cves:
        cve_id = item.get('cve', {}).get('id', '')
        description = item.get('cve', {}).get('descriptions', [{}])[0].get('value', 'No Description')
        published = item.get('cve', {}).get('published', '')
        last_modified = item.get('cve', {}).get('lastModified', '')
        cvss_score = item.get('cve', {}).get('metrics', {}).get('cvssMetricV3', [{}])[0].get('cvssData', {}).get('baseScore', None)

        c.execute('''INSERT OR REPLACE INTO cves (id, description, published, last_modified, cvss_score) 
                     VALUES (?, ?, ?, ?, ?)''',
                  (cve_id, description, published, last_modified, cvss_score))

    conn.commit()
    conn.close()
    print("CVEs stored successfully.")  # Log when storage is complete

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')  # Serve the home page with a table

# Route to render CVE data in a JSON format
@app.route('/api/cves', methods=['GET'])
def show_cves():
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute('SELECT id, description, published, last_modified, cvss_score FROM cves')
        rows = c.fetchall()
    finally:
        conn.close()

    cves_list = []
    for row in rows:
        cves_list.append({
            'id': row['id'],
            'description': row['description'],
            'published': row['published'],
            'last_modified': row['last_modified'],
            'cvss_score': row['cvss_score']
        })
    
    return jsonify(cves_list)

# Route to render CVE data in HTML format
@app.route('/cves', methods=['GET'])
def render_cves():
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute('SELECT id, description, published, last_modified, cvss_score FROM cves')
        rows = c.fetchall()
    finally:
        conn.close()

    return render_template('cve_list.html', cves=rows)  # Pass the data to HTML template

# API to sync CVE data from NVD
@app.route('/api/cves/sync', methods=['GET'])
def sync_cves():
    try:
        fetch_and_store_cves()
        return jsonify({'message': 'CVE data synchronized successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# API to get details of a specific CVE by ID
@app.route('/api/cves/<string:cve_id>', methods=['GET'])
def get_cve_by_id(cve_id):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute('SELECT id, description, published, last_modified, cvss_score FROM cves WHERE id = ?', (cve_id,))
        row = c.fetchone()
    finally:
        conn.close()

    if row:
        cve = {
            'id': row['id'],
            'description': row['description'],
            'published': row['published'],
            'last_modified': row['last_modified'],
            'cvss_score': row['cvss_score']
        }
        return jsonify(cve)
    else:
        return jsonify({'message': 'CVE not found'}), 404

# API to filter CVEs by published date or CVSS score
@app.route('/api/cves/filter', methods=['GET'])
def filter_cves():
    # Get query parameters from the request
    published = request.args.get('published', None)
    min_cvss = request.args.get('min_cvss', None)
    max_cvss = request.args.get('max_cvss', None)

    # Initialize query and parameters
    query = 'SELECT id, description, published, last_modified, cvss_score FROM cves WHERE 1=1'
    params = []

    # Add filtering for 'published' date
    if published:
        query += ' AND published = ?'
        params.append(published)

    # Add filtering for 'min_cvss' score (greater than or equal to)
    if min_cvss:
        try:
            min_cvss = float(min_cvss)
            query += ' AND cvss_score >= ?'
            params.append(min_cvss)
        except ValueError:
            return jsonify({'message': 'Invalid min_cvss value. It must be a number.'}), 400

    # Add filtering for 'max_cvss' score (less than or equal to)
    if max_cvss:
        try:
            max_cvss = float(max_cvss)
            query += ' AND cvss_score <= ?'
            params.append(max_cvss)
        except ValueError:
            return jsonify({'message': 'Invalid max_cvss value. It must be a number.'}), 400

    # Execute the query with the specified filters
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute(query, tuple(params))
        rows = c.fetchall()
    finally:
        conn.close()

    # Prepare the list of CVEs to return
    cves_list = []
    for row in rows:
        cves_list.append({
            'id': row['id'],
            'description': row['description'],
            'published': row['published'],
            'last_modified': row['last_modified'],
            'cvss_score': row['cvss_score']
        })

    return jsonify(cves_list)

# Root route for testing
@app.route('/test')
def test():
    return jsonify({'message': 'CVE API is running!'})

if __name__ == '__main__':
    init_db()  # Initialize the database with the required schema
    app.run(debug=True, host='0.0.0.0', port=5000)