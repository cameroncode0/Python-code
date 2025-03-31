from TikTokApi import TikTokApi
import time

def check_new_post(username, last_video_id=None):
    # Initialize TikTokApi
    api = TikTokApi()

    # Get the latest videos from the user
    user_videos = api.user(username=username).videos(count=1)

    # Get the ID of the latest video
    if user_videos:
        latest_video_id = user_videos[0].id

        # Check if the latest video is new
        if latest_video_id != last_video_id:
            print(f"New video posted by {username}: {latest_video_id}")
            return latest_video_id  # Return the new ID to update the last known video
    return last_video_id

def monitor_tiktok(username, check_interval=60):
    print(f"Monitoring TikTok for user: {username}")
    last_video_id = None  # Store the ID of the last known video

    while True:
        last_video_id = check_new_post(username, last_video_id)
        time.sleep(check_interval)  # Wait for the next check

# Replace 'username' with the TikTok username you want to monitor
monitor_tiktok('username', check_interval=300)  # Check every 5 minutes
