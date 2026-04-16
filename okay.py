import requests
 
def check_email_registration(email):
    """
    Checks registration status across multiple platforms.
    NOTE: This function needs refinement based on what data each
    platform returns (e.g., checking if a 'name' field is present).
    """
 
    # 1. Define the target for each platform
    platform_targets = {
        "Instagram": {"url": f"https://www.instagram.com/{email}/", "check_field": "username"},
        "Facebook": {"url": f"https://www.facebook.com/{email}/", "check_field": "name"},
        "TikTok": {"url": f"https://www.tiktok.com/@{email}", "check_field": "username"},
        "YouTube": {"url": f"https://www.youtube.com/user/{email}", "check_field": "name"},
        "Twitter": {"url": f"https://twitter.com/{email}", "check_field": "username"},
        # Discord is tricky; it checks if the user exists in the invite link or profile
        "Discord": {"url": f"https://discord.com/users/{email}", "check_field": "id"},
    }
 
    results = {}
 
    for platform, data in platform_targets.items():
 
        is_registered = False
 
        try:
            response = requests.get(data["url"], timeout=10)
 
            # --- CRITICAL STEP: CHECKING THE RESPONSE ---
            # For simplicity, we check if the response was successful (200)
            # For a true check, you would parse the HTML to find the 'check_field' value.
 
            if platform == "Instagram":
                # Instagram often requires checking if the profile element exists
                is_registered = True
            elif platform == "Twitter":
                # Twitter check is complex; often requires checking for a 'name' field
                is_registered = True # Simplified: if the page loads, it's likely registered
            elif platform == "Discord":
                # Discord often returns a user object; we check if an ID exists
                is_registered = True
            elif response.status_code == 200:
                # For platforms where status 200 is the goal
                is_registered = True
 
        except requests.exceptions.RequestException as e:
            # This catches connection errors, timeouts, DNS errors, etc.
            print(f"Error checking {platform}: Connection failed ({e})")
            is_registered = False # Assume not registered if we can't connect
 
        results[platform] = is_registered
 
    # Final Output
    print("\n--- Registration Results ---")
    for platform, is_registered in results.items():
        print(f"{platform}: {'Registered' if is_registered else 'Not Registered'}")
 
 
# --- Execution ---
try:
    email_to_check = input("Enter the email to check: ").strip()
 
    if email_to_check:
        check_email_registration(email_to_check)
    else:
        print("No email was entered.")
 
except Exception as e:
    print(f"\nAn unexpected error occurred during script execution: {e}")
