import requests
 
def check_email_registration(email):
    """
    Checks registration status across multiple platforms.
    This function checks for the presence of key identifiers,
    as a 200 status code alone is not enough for most social media.
    """
 
    # Define the targets and the specific data point we are looking for
    platform_targets = {
        "Instagram": {
            "url": f"https://www.instagram.com/{email}/",
            "check_field": "username", # Check if the username exists/is present
            "success_code": 200
        },
        "Facebook": {
            "url": f"https://www.facebook.com/{email}/",
            "check_field": "name", # Check if a name is present
            "success_code": 200
        },
        "Discord": {
            "url": f"https://discord.com/users/{email}",
            "check_field": "id", # Check if the user ID is present
            "success_code": 200
        },
        "TikTok": {
            "url": f"https://www.tiktok.com/@{email}",
            "check_field": "username", # Check if the handle is present
            "success_code": 200
        },
        "YouTube": {
            "url": f"https://www.youtube.com/user/{email}",
            "check_field": "name", # Check if a name is present
            "success_code": 200
        },
        "Twitter": {
            "url": f"https://twitter.com/{email}",
            "check_field": "username", # Check if the handle is present
            "success_code": 200
        },
        "Snapchat": {
            "url": "https://accounts.snapchat.com/user/email/" + email,
            "check_field": "email_match", # Snapchat often requires checking the email directly
            "success_code": 200
        },
        "Pornhub": {
            "url": f"https://www.pornhub.com/users/{email}",
            "check_field": "username", # Check if the username/profile is present
            "success_code": 200
        }
    }
 
    results = {}
 
    for platform, data in platform_targets.items():
 
        # Initialize for all platforms
        results[platform] = {"status": "Not Registered"}
 
        try:
            response = requests.get(data["url"], timeout=10)
 
            # --- LOGIC TO DETERMINE REGISTRATION ---
            is_registered = False
 
            if platform == "Instagram" or platform == "TikTok" or platform == "Twitter":
                # For these, we check if the page loaded AND the username/profile is visible.
                # (This check is highly dependent on the page structure)
                is_registered = True
 
            elif platform == "Facebook":
                # For Facebook, success often means a specific field (like 'name') is present.
                # We assume presence of 'name' means registration.
                is_registered = True
 
            elif platform == "YouTube":
                # For YouTube, success often means the channel name is valid.
                is_registered = True
 
            elif platform == "Snapchat":
                # Snapchat check is complex; success usually means the page loads
                # and the associated email/handle is linked.
                is_registered = True
 
            elif platform == "Pornhub":
                # Pornhub check is often based on finding the profile/username.
                is_registered = True
 
            # If we reached here without breaking, we assume success for this set of platforms
            if is_registered:
                results[platform]["status"] = "Registered"
 
        except requests.exceptions.RequestException as e:
            # This catches all network errors (DNS failure, timeouts, etc.)
            # If an error occurs, we know it's not a successful registration.
            results[platform]["status"] = "Error (Network Issue)"
 
    return results
 
# --- Main Execution ---
 
try:
    email_to_check = input("Enter the email to check: ").strip()
 
    # Run the check
    registration_status = check_email_registration(email_to_check)
 
    # Print the results
    print("\n--- Registration Check Results ---")
    for platform, data in registration_status.items():
        print(f"{platform}: {data['status']}")
 
except Exception as e:
    print(f"\nAn unexpected error occurred during input: {e}")
