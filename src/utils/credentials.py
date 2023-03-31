from decouple import config

token = config("jira_token")

url = config("base_url")

user_email = config("user_email")


if __name__ == "__main__":
    print(url)
    print(token)