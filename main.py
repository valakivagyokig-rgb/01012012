import requests

def check_email_registration(email):
    platforms = {
        "Instagram": f"https://www.instagram.com/{email}/",
        "Facebook": f"https://www.facebook.com/{email}/",
        "Discord": f"https://discord.com/users/{email}",
        "Pornhub": f"https://www.pornhub.com/users/{email}",
        "Snapchat": f"https://accounts.snapchat.com/accounts/login",
        "TikTok": f"https://www.tiktok.com/@{email}",
        "YouTube": f"https://www.youtube.com/user/{email}",
        "Twitter": f"https://twitter.com/{email}"
    }

    results = {}
    for platform, url in platforms.items():
        response = requests.get(url)
        results[platform] = response.status_code == 200

    return results

email_to_check = input("Enter the email to check: ")
registration_status = check_email_registration(email_to_check)

for platform, is_registered in registration_status.items():
    print(f"{platform}: {'Registered' if is_registered else 'Not Registered'}")
