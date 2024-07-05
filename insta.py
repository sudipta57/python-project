from instabot import Bot
import os
import logging
import time

def delete_session_file(username):
    session_file = f"config/session-{username}.json"
    if os.path.exists(session_file):
        os.remove(session_file)
        print(f"Deleted old session file: {session_file}")
    else:
        print(f"No session file found for user: {username}")

def clear_cookies_directory():
    cookies_dir = "config"
    if os.path.exists(cookies_dir):
        for file in os.listdir(cookies_dir):
            file_path = os.path.join(cookies_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted cookie file: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

def login_with_retry(bot, username, password, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            bot.login(username=username, password=password)
            if bot.api.is_logged_in:
                print("Login successful")
                return True
        except Exception as e:
            print(f"Login attempt {retries + 1} failed: {e}")
            wait_time = 60 * (2 ** retries)  # Exponential backoff
            print(f"Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            retries += 1
    print("Max retries reached. Login failed.")
    return False

def main():
    username = input("Enter your instagram ID: ")
    password = input("Enter your instagram Password: ")
    clear_cookies_directory()
    bot = Bot()

    try:
        # Enable verbose logging
        logging.basicConfig(level=logging.INFO)

        # Attempt login with retries
        if not login_with_retry(bot, username, password):
            raise Exception("Login failed after multiple attempts.")

        # Example: Unfollow users
        following = bot.following
        for user_id in following:
            try:
                bot.unfollow(user_id)
                print(f"Unfollowed user: {user_id}")
                time.sleep(10)  # Delay between unfollow actions to avoid rate limits
            except Exception as e:
                print(f"Failed to unfollow {user_id}: {e}")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
