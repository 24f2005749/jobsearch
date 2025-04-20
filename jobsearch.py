import requests
import pandas as pd
import json
import os
from datetime import datetime

class JobSearch:
    def __init__(self):
        # Adzuna API credentials - you'll need to register at https://developer.adzuna.com/
        self.app_id = "apiid"  # Replace with your App ID
        self.app_key = "apikey"  # Replace with your API Key
        self.base_url = "https://api.adzuna.com/v1/api/jobs"
        self.results = []
        
    def search_jobs(self, what, where, results_per_page=10, page=1):
        """Search for jobs based on role and location"""
        country_code = self._get_country_code(where)
        
        url = f"{self.base_url}/{country_code}/search/{page}"
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": results_per_page,
            "what": what,
            "where": where,
            "content-type": "application/json"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            
            if "results" in data:
                self.results = data["results"]
                return True
            else:
                print(f"No results found or API error: {data.get('error', 'Unknown error')}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return False
            
    def _get_country_code(self, location):
        """Simple mapping of common countries/regions to their country codes"""
        location = location.lower()
        country_map = {
            "uk": "gb",
            "united kingdom": "gb",
            "britain": "gb",
            "england": "gb",
            "us": "us",
            "usa": "us",
            "united states": "us",
            "america": "us",
            "canada": "ca",
            "australia": "au",
            "germany": "de",
            "france": "fr",
            "india": "in"
        }
        
        # Look for country names in the location string
        for country, code in country_map.items():
            if country in location:
                return code
                
        # Default to US if no match found
        return "us"
        
    def display_results(self):
        """Display job results in a formatted way"""
        if not self.results:
            print("No results to display")
            return
            
        print(f"\n{'=' * 80}")
        print(f"Found {len(self.results)} jobs:")
        print(f"{'=' * 80}")
        
        for i, job in enumerate(self.results, 1):
            print(f"\n{i}. {job.get('title', 'No title')}")
            print(f"Company: {job.get('company', {}).get('display_name', 'N/A')}")
            print(f"Location: {job.get('location', {}).get('display_name', 'N/A')}")
            print(f"Salary: {job.get('salary_min', 'N/A')} - {job.get('salary_max', 'N/A')} {job.get('salary_currency', '')}")
            print(f"Description: {job.get('description', 'No description')[:150]}...")
            print(f"URL: {job.get('redirect_url', 'N/A')}")
            print(f"{'-' * 80}")
    
    def export_to_csv(self, filename=None):
        """Export job results to a CSV file"""
        if not self.results:
            print("No results to export")
            return False
            
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"job_search_{timestamp}.csv"
            
        try:
            # Extract relevant data from results
            jobs_data = []
            for job in self.results:
                job_data = {
                    "Title": job.get("title", ""),
                    "Company": job.get("company", {}).get("display_name", ""),
                    "Location": job.get("location", {}).get("display_name", ""),
                    "Salary Min": job.get("salary_min", ""),
                    "Salary Max": job.get("salary_max", ""),
                    "Currency": job.get("salary_currency", ""),
                    "Description": job.get("description", ""),
                    "URL": job.get("redirect_url", ""),
                    "Job ID": job.get("id", "")
                }
                jobs_data.append(job_data)
                
            # Create DataFrame and export to CSV
            df = pd.DataFrame(jobs_data)
            df.to_csv(filename, index=False, encoding="utf-8")
            
            print(f"Successfully exported {len(self.results)} jobs to {filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False


def main():
    job_search = JobSearch()
    
    print("\n🔍 Job Search Tool 🔍")
    print("-" * 30)
    
    while True:
        role = input("\nEnter job role/title (or 'exit' to quit): ")
        if role.lower() == "exit":
            break
            
        location = input("Enter location (city, state, or country): ")
        num_results = input("Number of results to retrieve (default: 10): ")
        
        try:
            num_results = int(num_results) if num_results else 10
        except ValueError:
            num_results = 10
            print("Invalid input. Using default value of 10.")
            
        print(f"\nSearching for {role} jobs in {location}...")
        
        if job_search.search_jobs(role, location, num_results):
            job_search.display_results()
            
            export = input("\nExport results to CSV? (y/n): ")
            if export.lower() == "y":
                job_search.export_to_csv()
        
        continue_search = input("\nSearch for another job? (y/n): ")
        if continue_search.lower() != "y":
            break
            
    print("\nThank you for using Job Search Tool!")


if __name__ == "__main__":
    main()
