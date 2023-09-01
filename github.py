import requests
import re
import pandas as pd

# GitHub API endpoint for issues
GITHUB_ISSUES_URL = "https://api.github.com/repos/connext/community-sybil-reports/issues"

# Define a function to extract addresses and file links from issue body
def extract_info_from_issue(issue_body):
    if not isinstance(issue_body, str):
        return set(), []

    # Extract Ethereum addresses
    addresses = set(re.findall(r'0x[a-fA-F0-9]{40}', issue_body))

    # Extract file links (for simplicity, we are considering only .txt and .csv files)
    file_links_pattern = r'https?://[\w\-\.]+/\S+\.(txt|csv)'
    file_links = [match.group() for match in re.finditer(file_links_pattern, issue_body)]

    return addresses, file_links

# Function to download and extract addresses from file links
def extract_addresses_from_files(file_links):
    extracted_addresses = set()
    for link in file_links:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                content = response.text
                addresses = set(re.findall(r'0x[a-fA-F0-9]{40}', content))
                extracted_addresses.update(addresses)
        except Exception as e:
            print(f"Error downloading or processing {link}: {e}")
    return extracted_addresses

def main():
    # Make a request to get issues
    response = requests.get(GITHUB_ISSUES_URL, params={"per_page": 100, "state": "all"})  # Adjust 'per_page' if needed
    issues = response.json()

    # Loop through issues, extract addresses and file links
    all_addresses = set()
    for issue in issues:
        if issue['number'] < 500:
            addresses, file_links = extract_info_from_issue(issue['body'])
            all_addresses.update(addresses)

            # Extract addresses from linked files
            addresses_from_files = extract_addresses_from_files(file_links)
            all_addresses.update(addresses_from_files)

    # Save all extracted addresses to CSV
    df = pd.DataFrame(list(all_addresses), columns=["Address"])
    df.to_csv("all_addresses_500.csv", index=False)

# Run the script
main()
