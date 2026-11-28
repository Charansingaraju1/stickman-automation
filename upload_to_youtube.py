import os, json, sys
import urllib.request, urllib.parse

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
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists(TOKEN_FILE):
        # Load scopes embedded in token.json so adding broader scopes doesn't break existing refresh tokens
        creds = Credentials.from_authorized_user_file(TOKEN_FILE)
    if creds and creds.expired and creds.refresh_token:
        from google.auth.transport.requests import Request
        creds.refresh(Request())
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    elif not creds or not creds.valid:
        if os.path.exists(CLIENT_SECRETS_FILE):
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"],
            )
            creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
        else:
            raise RuntimeError("No valid credentials or client_secret.json found!")
    return build("youtube", "v3", credentials=creds)

def upload_video(file_path, title, description, tags=None, privacy="public", thumbnail_path=None, comment_text=None, contains_synthetic_media=False):
    from googleapiclient.http import MediaFileUpload

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
            "selfDeclaredMadeForKids": False,
            # YPP disclosure for photorealistic altered/synthetic scenes when applicable
            "containsSyntheticMedia": bool(contains_synthetic_media),
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

    if thumbnail_path and os.path.exists(thumbnail_path):
        try:
            youtube.thumbnails().set(
                videoId=response['id'],
                media_body=MediaFileUpload(thumbnail_path, mimetype='image/jpeg')
            ).execute()
            print(f"Thumbnail uploaded successfully for video {response['id']}!")
        except Exception as e:
            print(f"Warning: Failed to set custom thumbnail: {e}")

    comment_posted = False
    comment_note = ""
    if comment_text:
        try:
            c_res = youtube.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": response['id'],
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": comment_text
                            }
                        }
                    }
                }
            ).execute()
            comment_posted = True
            print(f"Automated top-level comment posted! ID: {c_res['id']}")
        except Exception as e:
            comment_note = f"Auto-comment skipped (needs youtube.force-ssl OAuth scope): {e}"
            print(comment_note)

    response["_comment_posted"] = comment_posted
    response["_comment_note"] = comment_note
    return response

VIRAL_QUEUE = [
    {
        "id": "hangnail",
        "filenames": ["stickman_hangnail_paronychia.mp4"],
        "title": "Why You Should NEVER Pull a Hangnail 😱🩸 #shorts",
        "description": "What actually happens when you rip a hangnail? Pulling it downwards can trigger severe paronychia bacterial infection! Never pull it with your teeth or fingers! #shorts #animation #science #medicalfacts #facts #stickman",
        "tags": ["shorts", "animation", "science", "medical facts", "stickman", "paronychia", "zack d films", "health", "satisfying"]
    },
    {
        "id": "holding_pee",
        "filenames": ["stickman_holding_pee_viral.mp4"],
        "title": "What Happens If You Hold Your Pee?! 🚽💀 #shorts",
        "description": "Can holding your pee actually explode your bladder? Here is the scientific truth of what happens inside your urinary tract! #shorts #animation #facts #stickman #science #health",
        "tags": ["shorts", "animation", "science", "medical facts", "stickman", "health", "zack d films", "curiosity"]
    },
    {
        "id": "swallowing_gum",
        "filenames": ["stickman_swallowing_gum_viral.mp4"],
        "title": "Does Swallowed Gum REALLY Stay For 7 Years?! 🍬😱 #shorts",
        "description": "What actually happens if you swallow chewing gum? Let's bust the 7-year stomach myth with stickman science! #shorts #animation #mythbusters #facts #science #health",
        "tags": ["shorts", "animation", "science", "mythbusters", "stickman", "health", "facts", "zack d films"]
    },
    {
        "id": "holding_sneeze",
        "filenames": ["stickman_holding_sneeze_viral.mp4", "stickman_holding_sneeze_perfect.mp4"],
        "title": "What Actually Happens If You Hold in a Sneeze?! 🤧💀 #shorts",
        "description": "Can holding in a sneeze actually tear your throat or burst an eardrum? Here is what happens when 100 MPH air gets trapped! #shorts #animation #facts #stickman #science #health",
        "tags": ["shorts", "animation", "science", "medical facts", "stickman", "sneeze", "health", "zack d films", "curiosity"]
    },
    {
        "id": "pimple_danger_triangle",
        "contains_synthetic_media": True,
        "filenames": ["stickman_pimple_danger_viral.mp4"],
        "thumbnail": "stickman_pimple_danger_thumbnail.jpg",
        "pinned_comment": "Be honest: have you EVER popped a pimple in the Danger Triangle before watching this? 😳👇 (I used to do it all the time...)",
        "title": "Why You Should NEVER Pop It 🩸💀 #shorts",
        "description": "Popping a pimple inside the danger triangle of your face can force bacteria backward through valveless veins directly toward your brain. Here is how squeezing a simple whitehead can trigger cavernous sinus thrombosis and why doctors warn against touching this zone. #shorts #medical #anatomy",
        "tags": [
            "danger triangle of face popping pimple",
            "what happens if you pop a pimple on your nose",
            "can popping a pimple cause a brain infection",
            "danger triangle face infection symptoms",
            "cavernous sinus thrombosis pimple",
            "shorts",
            "medical",
            "anatomy",
            "science"
        ]
    },
    {
        "id": "ear_bug_tweezer_danger",
        "contains_synthetic_media": True,
        "filenames": ["stickman_ear_bug_viral.mp4"],
        "thumbnail": "stickman_ear_bug_thumbnail.jpg",
        "pinned_comment": "Be honest: what would be your IMMEDIATE reaction if an insect crawled in your ear? 🪲😱👇 (Tweezers, Q-tip, or ER?)",
        "title": "Why You Should NEVER Dig Out an Ear Bug 🪲😱 #shorts",
        "description": "What actually happens if an insect crawls into your ear canal? Poking inside with tweezers or a cotton swab can shove it deeper and rupture your delicate eardrum! Here is why doctors use warm mineral oil instead. #shorts #medical #anatomy",
        "tags": [
            "why you should never dig out an ear bug",
            "bug in ear canal",
            "insect trapped in ear",
            "eardrum rupture tweezers",
            "mineral oil ear bug removal",
            "ear canal anatomy",
            "shorts",
            "medical",
            "anatomy",
            "science"
        ]
    },
    {
        "id": "qtip_eardrum_danger",
        "contains_synthetic_media": True,
        "filenames": ["stickman_qtip_viral.mp4"],
        "thumbnail": "stickman_qtip_thumbnail.jpg",
        "pinned_comment": "Be honest: do you STILL clean your ears with Q-tips after seeing this? 🚫👂👇 (Did it ever hurt your eardrum?)",
        "title": "Why You Should NEVER Clean Ears With Q-Tips 👂😱 #shorts",
        "description": "Pushing cotton swabs inside your ear canal packs wax backward like a piston against your delicate eardrum membrane. Here is how Q-tips cause compacted earwax rupture and permanent hearing damage. #shorts #medical #anatomy",
        "tags": [
            "why you should never clean ears with q tips",
            "cotton swabs push earwax eardrum",
            "q tip eardrum rupture",
            "cotton swab earwax impaction",
            "how to safely clean earwax",
            "ear canal anatomy 3d",
            "saline ear drops wax removal",
            "shorts",
            "medical",
            "anatomy",
            "science"
        ]
    },
    {
        "id": "fish_bone_bread_danger",
        "contains_synthetic_media": True,
        "filenames": ["stickman_fish_bone_viral.mp4"],
        "thumbnail": "stickman_fish_bone_thumbnail.jpg",
        "pinned_comment": "Be honest: when a fish bone got stuck in your throat, did you try the bread trick or rush to the doctor? 🍞👇 (What actually happened?)",
        "title": "Why You Should NEVER Eat Bread for a Fish Bone 🦴😱 #shorts",
        "description": "Swallowing dense balls of bread or white rice when a fish bone is stuck acts like a hammer against your throat lining. Here is how home remedies cause esophageal perforation and how an ENT removes it safely. #shorts #medical #anatomy",
        "tags": [
            "fish bone stuck in throat",
            "swallow bread for fish bone",
            "fish bone rice trick danger",
            "esophageal perforation fish bone",
            "ent fish bone removal",
            "swallowing fish bone myth",
            "shorts",
            "medical",
            "anatomy",
            "science"
        ]
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

CLOUD_QUEUE_FILE = os.path.join(BASE_DIR, "cloud_queue.json")


def load_viral_queue():
    """Return built-in queue items plus dynamically stocked cloud_queue.json items without duplicates."""
    items = list(VIRAL_QUEUE)
    seen = {q["id"] for q in items}
    if os.path.exists(CLOUD_QUEUE_FILE):
        try:
            with open(CLOUD_QUEUE_FILE, "r", encoding="utf-8") as f:
                extra = json.load(f)
            for q in extra:
                if isinstance(q, dict) and q.get("id") and q["id"] not in seen:
                    items.append(q)
                    seen.add(q["id"])
        except Exception as e:
            print(f"Warning loading cloud_queue.json: {e}")
    return items


def print_queue_status():
    queue_file = os.path.join(BASE_DIR, "uploaded_history.json")
    uploaded = []
    if os.path.exists(queue_file):
        try:
            with open(queue_file, "r") as f:
                uploaded = json.load(f)
        except:
            uploaded = []

    queue_items = load_viral_queue()
    print("\n" + "=" * 70)
    print(" 🚀 STICK NATION DAILY — AUTOMATED VIRAL QUEUE")
    print("=" * 70)
    for idx, item in enumerate(queue_items, 1):
        is_uploaded = item["id"] in uploaded
        target_file = find_video_file(item["filenames"])
        thumb_file = find_video_file([item["thumbnail"]]) if item.get("thumbnail") else None
        
        if is_uploaded:
            badge = "✅ PUBLISHED"
        elif target_file:
            badge = "🟡 READY TO UPLOAD"
        else:
            badge = "⏳ ASSET PENDING"
            
        print(f"[{idx}] {badge} | ID: {item['id']}")
        print(f"    🎬 Title: {item['title']}")
        print(f"    📹 Video: {os.path.basename(target_file) if target_file else '❌ Pending Render'}")
        if item.get("thumbnail"):
            print(f"    🖼️  Thumb: {os.path.basename(thumb_file) if thumb_file else '❌ Missing'}")
        print()
    print("=" * 70 + "\n")

def validate_ypp_compliance(item, uploaded_ids):
    """Block duplicate uploads, repetitive title templates, and thin descriptions (YPP Inauthentic Content policy)."""
    title_norm = item["title"].strip().lower()
    desc_words = [w for w in item["description"].split() if not w.startswith("#")]
    if len(item["description"].strip()) < 100 or len(set(desc_words)) < 15:
        raise ValueError(f"YPP Compliance Block [{item['id']}]: description too thin or templated.")

    prior_items = [q for q in load_viral_queue() if q["id"] in uploaded_ids]
    if any(q["title"].strip().lower() == title_norm for q in prior_items):
        raise ValueError(f"YPP Compliance Block [{item['id']}]: duplicate title already published.")
    if prior_items:
        prev_prefix = " ".join(prior_items[-1]["title"].lower().split()[:4])
        cur_prefix = " ".join(title_norm.split()[:4])
        if cur_prefix == prev_prefix and cur_prefix == "why you should never":
            raise ValueError(f"YPP Compliance Block [{item['id']}]: consecutive 'Why You Should NEVER...' title spam.")


def upload_next_in_queue(dry_run=False):
    queue_file = os.path.join(BASE_DIR, "uploaded_history.json")
    uploaded = []
    if os.path.exists(queue_file):
        try:
            with open(queue_file, "r") as f:
                uploaded = json.load(f)
        except:
            uploaded = []

    queue_items = load_viral_queue()
    for item in queue_items:
        if item["id"] not in uploaded:
            validate_ypp_compliance(item, uploaded)
            target_file = find_video_file(item["filenames"])
            if target_file:
                thumb_file = find_video_file([item["thumbnail"]]) if item.get("thumbnail") else None
                print(f"{'[DRY RUN] Would upload' if dry_run else 'Uploading'} next in queue: {item['title']} from {target_file}")
                if thumb_file:
                    print(f"Applying custom thumbnail: {thumb_file}")
                
                if dry_run:
                    print("[DRY RUN] Simulation complete. No video was published.")
                    return {"id": "dry_run_simulation", "title": item["title"]}
                    
                res = upload_video(
                    target_file,
                    item["title"],
                    item["description"],
                    item["tags"],
                    thumbnail_path=thumb_file,
                    comment_text=item.get("pinned_comment"),
                    contains_synthetic_media=item.get("contains_synthetic_media", False),
                )
                vid_id = res.get("id")
                uploaded.append(item["id"])
                with open(queue_file, "w") as f:
                    json.dump(uploaded, f, indent=2)
                alert = (
                    f"🎉 Boss, Short is LIVE on YouTube!\n\n"
                    f"🎬 Title: {item['title']}\n"
                    f"🔗 Link: https://youtube.com/shorts/{vid_id}\n\n"
                )
                if item.get("pinned_comment"):
                    status_tag = "✅ Auto-posted on video" if res.get("_comment_posted") else "⚠️ Needs manual post (refresh OAuth with youtube.force-ssl scope)"
                    alert += f"📌 Pinned Comment ({status_tag}):\n\"{item['pinned_comment']}\"\n\n"
                alert += "Published via 100% Free Cloud Automation (0% Laptop Load)! 💪\n"

                # Check remaining videos in queue
                remaining_ready = [
                    q for q in queue_items 
                    if q["id"] not in uploaded and find_video_file(q["filenames"]) is not None
                ]
                count_left = len(remaining_ready)
                alert += f"\n📊 Queue Status: {count_left} Short{'s' if count_left != 1 else ''} remaining on deck."
                if count_left <= 1:
                    alert += "\n\n⚠️ BOSS ALERT: Queue running low! When you return from college at 7:00 PM, open your laptop to batch-generate the next 3–4 Shorts! 💻"

                send_telegram_alert(alert)
                return res
            else:
                print(f"Warning: Video file for {item['id']} not found in search paths.")
    print("All queued videos have been uploaded!")
    return None

def refresh_auth_token():
    """Run local browser OAuth flow with youtube.upload + youtube.force-ssl scopes for GitHub secret update."""
    from google_auth_oauthlib.flow import InstalledAppFlow

    if not os.path.exists(CLIENT_SECRETS_FILE):
        raise FileNotFoundError(
            f"Missing {CLIENT_SECRETS_FILE}. Download OAuth Desktop JSON from Google Cloud Console first."
        )
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        [
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtube.force-ssl",
        ],
    )
    creds = flow.run_local_server(port=0)
    token_json = creds.to_json()
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(token_json)
    print("\nSUCCESS: Saved token.json locally with full upload + comment scopes.")
    print("Copy the JSON printed below into GitHub Repo Secret -> YOUTUBE_TOKEN_JSON:\n")
    print(token_json)


if __name__ == "__main__":
    if "--status" in sys.argv:
        print_queue_status()
    elif "--auth" in sys.argv or "--setup-auth" in sys.argv:
        refresh_auth_token()
    elif "--dry-run" in sys.argv:
        upload_next_in_queue(dry_run=True)
    else:
        upload_next_in_queue()
