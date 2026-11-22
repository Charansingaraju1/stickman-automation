import os, json, sys
import urllib.request, urllib.parse
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secret.json")

BOT_TOKEN = "9209650931:AAHnXeSzG4JURWeZCryqRMLSdpV6Mp-Z3lU"
CHAT_ID = "6236827164"

def send_telegram_alert(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("Telegram alert sent successfully.")
    except Exception as e:
        print(f"Telegram alert error: {e}")

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        from google.auth.transport.requests import Request
        creds.refresh(Request())
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    elif not creds or not creds.valid:
        if os.path.exists(CLIENT_SECRETS_FILE):
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
        else:
            raise RuntimeError("No valid credentials or client_secret.json found!")
    return build("youtube", "v3", credentials=creds)

def upload_video(file_path, title, description, tags=None, privacy="public"):
    youtube = get_authenticated_service()
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": "28"  # Science & Technology
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False
        }
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    print(f"Video uploaded successfully! Video ID: {response['id']}")
    return response

VIRAL_QUEUE = [
    {
        "id": "hangnail",
        "filenames": ["stickman_hangnail_paronychia.mp4"],
        "title": "Why You Should NEVER Pull a Hangnail 😱 #shorts",
        "description": "What actually happens when you rip a hangnail? Here is why pulling it downwards can trigger severe Paronychia infection! #shorts #animation #facts #stickman",
        "tags": ["shorts", "animation", "science", "medical facts", "stickman", "paronychia"]
    },
    {
        "id": "holding_pee",
        "filenames": ["stickman_holding_pee_viral.mp4"],
        "title": "What Happens If You Hold Your Pee?! 🚽💀 #shorts",
        "description": "Can holding your pee actually rupture your bladder? Here is what happens inside your urinary tract! #shorts #animation #facts #stickman",
        "tags": ["shorts", "animation", "science", "medical facts", "stickman", "health"]
    },
    {
        "id": "swallowing_gum",
        "filenames": ["stickman_swallowing_gum_viral.mp4"],
        "title": "What Actually Happens If You Swallow Gum?! 🍬 #shorts",
        "description": "Does swallowed gum stay in your stomach for 7 years? Let's bust the medical myth with stickman science! #shorts #animation #mythbusters #facts",
        "tags": ["shorts", "animation", "science", "mythbusters", "stickman", "health"]
    }
]

def find_video_file(candidate_names):
    search_dirs = [
        os.path.join(BASE_DIR, "videos"),
        os.path.join(BASE_DIR, "out"),
        BASE_DIR,
        r"C:\Users\chara\.gemini\antigravity\scratch\stickman-daily\out"
    ]
    for d in search_dirs:
        if not os.path.exists(d):
            continue
        for name in candidate_names:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
    return None

def upload_next_in_queue():
    queue_file = os.path.join(BASE_DIR, "uploaded_history.json")
    uploaded = []
    if os.path.exists(queue_file):
        try:
            with open(queue_file, "r") as f:
                uploaded = json.load(f)
        except:
            uploaded = []
            
    for item in VIRAL_QUEUE:
        if item["id"] not in uploaded:
            target_file = find_video_file(item["filenames"])
            if target_file:
                print(f"Uploading next in queue: {item['title']} from {target_file}")
                res = upload_video(target_file, item["title"], item["description"], item["tags"])
                vid_id = res.get("id")
                uploaded.append(item["id"])
                with open(queue_file, "w") as f:
                    json.dump(uploaded, f, indent=2)
                alert = (
                    f"🎉 Boss, Short is LIVE on YouTube!\n\n"
                    f"🎬 Title: {item['title']}\n"
                    f"🔗 Link: https://youtube.com/shorts/{vid_id}\n\n"
                    f"Published via 100% Free Cloud Automation (0% Laptop Load)! 💪"
                )
                send_telegram_alert(alert)
                return res
            else:
                print(f"Warning: Video file for {item['id']} not found in search paths.")
    print("All queued videos have been uploaded!")
    return None

if __name__ == "__main__":
    upload_next_in_queue()
