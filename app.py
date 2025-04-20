from flask import Flask, render_template, request, redirect, url_for, send_file, session
import os
import time
from datetime import datetime
from io import StringIO
from jobsearch import JobSearch

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For session management
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    job_role = request.form.get('job_role')
    location = request.form.get('location')
    num_results = request.form.get('num_results', '10')
    
    try:
        num_results = int(num_results)
    except ValueError:
        num_results = 10
    
    job_search = JobSearch()
    success = job_search.search_jobs(job_role, location, num_results)
    
    if success:
        # Store results in session for potential download
        session['job_results'] = job_search.results
        return render_template('results.html', 
                              job_role=job_role, 
                              location=location,
                              results=job_search.results,
                              count=len(job_search.results))
    else:
        return render_template('index.html', 
                              error="No jobs found or API error. Please try again.",
                              job_role=job_role,
                              location=location)

@app.route('/download')
def download():
    results = session.get('job_results', [])
    
    if not results:
        return redirect(url_for('index'))
    
    # Create a new JobSearch instance and set the results
    job_search = JobSearch()
    job_search.results = results
    
    # Generate CSV filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"job_search_{timestamp}.csv"
    filepath = os.path.join(os.getcwd(), filename)
    
    # Export to CSV
    job_search.export_to_csv(filepath)
    
    # Send file to user
    return send_file(filepath, 
                    mimetype='text/csv',
                    attachment_filename=filename,
                    as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)