from bs4 import BeautifulSoup

country = 'world'
source_file = f"data/{country}_areas.html";
output_file = f"data/{country}_areas.sql";

# Read the HTML file
with open(source_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Initialize an empty dictionary to store the result
data = {}

# Dictionary to track hrefs and the state they first appeared in
href_tracker = {}

# List to store state names with repeated hrefs
states_with_repeated_hrefs = []

# Find all <h4> elements
for h4 in soup.find_all('h4'):
    state_name = h4.text  # Get the text inside <h4> (state name)
    
    # Get the next <ul> element and its <li> children
    ul = h4.find_next('ul')
    if ul:
        links = []
        for li in ul.find_all('li'):
            a_tag = li.find('a')
            if a_tag:
                href = a_tag['href']
                text = a_tag.text
                
                # Check if href has been seen before
                if href in href_tracker:
                    # If href is repeated, add the state to the list
                    if state_name not in states_with_repeated_hrefs:
                        states_with_repeated_hrefs.append(state_name)
                else:
                    # Track the href and the state it first appeared in
                    href_tracker[href] = state_name
                
                # Add href and text to the list
                links.append([href, text])
        
        # Add to dictionary with state name as key
        data[state_name] = links

# Output the resulting dictionary and repeated href states
#print("Parsed Data:", data)
print("States with repeated hrefs:", states_with_repeated_hrefs)

# Start the SQL INSERT statement
sql_insert_statements = "INSERT INTO `areas` (`id`, `name`, `region`, `country`, `url`, `created_at`, `updated_at`) VALUES\n"

# List to hold all the value rows
values = []

# Loop through the dictionary and generate SQL values
for state_name, locations in data.items():
    for location in locations:
        href = location[0]
        text = location[1]
        
        # Exclude entries where href is 'https://miami.craigslist.org'
        if href == 'https://miami.craigslist.org':
            continue  # Skip this entry

        # Format the SQL value row
        values.append(f"(NULL, '{text}', '{state_name}', '{state_name}', '{href}', NOW(), NOW())")

# Join all values into a single string, separating each by a comma and newline
if values:
    sql_insert_statements += ",\n".join(values) + ";\n"
else:
    sql_insert_statements = ""  # In case no values are added, avoid invalid SQL

# Write the final SQL query to a text file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(sql_insert_statements)

# Print confirmation message
print(f"SQL statements have been written to {output_file}")