import requests

def check_email_registration(email: str) -> dict:
    """
    Checks registration status across various platforms using a single email input.
    This function is designed to handle false positives by checking for
    presence rather than exact string matching.

    Args:
        email: The email address to check across all platforms. This is the
               primary input driving all checks.

    Returns:
        A dictionary containing the registration status and reasons for
        any false positives found.
    """

    # --- 1. Define Platform Targets ---
    # Each platform has a unique way it displays an email/username.
    platform_targets = {
        "Instagram": {
            "check_type": "username_or_email",
            "success_keywords": ["@"+email, email],
            "false_positive_reason": "Username/Email mismatch"
        },
        "Facebook": {
            "check_type": "name_presence",
            "success_keywords": [email],
            "false_positive_reason": "Email appears in contact details"
        },
        "Snapchat": {
            "check_type": "direct_match",
            "success_keywords": [email],
            "false_positive_reason": "System defaults to registration"
        },
        "Discord": {
            "check_type": "username_presence",
            "success_keywords": [email],
            "false_positive_reason": "Username/Email mismatch"
        },
        "YouTube": {
            "check_type": "handle_match",
            "success_keywords": [email],
            "false_positive_reason": "Email listed in channel details"
        },
        "TikTok": {
            "check_type": "bio_or_username",
            "success_keywords": [email],
            "false_positive_reason": "Bio/Username confusion"
        },
        "Pornhub": {
            "check_type": "username_or_email",
            "success_keywords": [email],
            "false_positive_reason": "Username/Email mismatch"
        }
    }

    final_results = {}

    # --- 2. Execute Checks ---
    for platform, data in platform_targets.items():
        is_registered = False
        response_text = ""

        try:
            # The actual request setup varies slightly for each platform
            if platform == "Instagram":
                # Check if the email appears in the handle or name fields
                target_url = f"https://www.instagram.com/{email}"
            elif platform == "Facebook":
                # Check if the email appears anywhere on the profile page
                target_url = f"https://www.facebook.com/{email}"
            elif platform == "Snapchat":
                # Snapchat often requires checking the URL path for the email
                target_url = f"https://accounts.snapchat.com/user/email/{email}"
            elif platform == "Discord":
                # Discord checks if the displayed username matches the input email
                target_url = f"https://discord.com/users/{email}"
            elif platform == "YouTube":
                # YouTube check often targets the channel handle
                # We strip any '@' from the email for clean handle matching
                youtube_handle = email.replace('@', '')
                target_url = f"https://www.youtube.com/@{youtube_handle}"
            elif platform == "TikTok":
                # TikTok checks the bio field or username
                tiktok_handle = email.replace('@', '')
                target_url = f"https://www.tiktok.com/@{tiktok_handle}"
            elif platform == "Pornhub":
                # Pornhub checks for the email in the user details
                target_url = f"https://www.pornhub.com/users/{email}"

            # --- Simulated Check Logic (This is where the actual API call would happen) ---

            # In a real scenario, we would make an HTTP request here and parse the response.
            # For this example, we simulate the logic based on the platform's needs.

            # --- SIMULATED SUCCESS LOGIC ---
            # If the input email matches the criteria for the platform:
            if data["check_type"] == "username_or_email":
                # This is the most common check; if *any* keyword is found, it's a hit.
                is_registered = True
                response_text = f"Success: Found keyword matching '{email}'."

            elif data["check_type"] == "direct_match":
                # Exact match is required for some platforms (e.g., Snapchat)
                is_registered = (email in "user_data") # Simulated check
                if is_registered:
                    response_text = f"Success: Exact match found for '{email}'."

            elif data["check_type"] == "name_presence":
                # Check if the email is present in a general name field (Facebook)
                is_registered = (email in "name_or_details") # Simulated check
                if is_registered:
                    response_text = f"Success: Email found in name/details for '{email}'."

            # --- End Simulated Logic ---

            if is_registered:
                final_results[platform] = {
                    "status": "Registered",
                    "reason": data["false_positive_reason"]
                }
            else:
                 final_results[platform] = {
                    "status": "Not Found",
                    "reason": f"Failed check against {data['false_positive_reason']}"
                }


        except requests.exceptions.RequestException as e:
            # Catches network errors (e.g., DNS failure, timeout)
            final_results[platform] = {
                "status": "Error",
                "reason": f"Network error occurred: {str(e)}"
            }

    return final_results

# Example usage demonstrating the input:
# result = check_email_registration("test@example.com")
