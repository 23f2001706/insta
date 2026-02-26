import hashlib
import hmac
import json
from flask import Flask, request, jsonify
from config import Config
from instagram_api import instagram_api
from gemini_handler import gemini_handler
from conversation_store import conversation_store

app = Flask(__name__)

# ─────────────────────────────────────────────
# YOUR BOT's Instagram-Scoped ID (IGID) & Page ID
# Add these to .env and config.py
# ─────────────────────────────────────────────
BOT_INSTAGRAM_IDS = {
    "17841468343963858",   # Your bot's IG account ID (entry.id)
    "17841414943450863",   # Your other linked IG account ID (entry.id)
}

# Track message IDs we've already processed (prevent duplicates)
processed_messages = set()
MAX_PROCESSED_CACHE = 10000

# Track message IDs we've SENT (prevent echo loop)
sent_message_ids = set()
MAX_SENT_CACHE = 5000


# ─────────────────────────────────────────────
# Webhook Verification (GET)
# ─────────────────────────────────────────────
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == Config.VERIFY_TOKEN:
        print("✅ Webhook verified!")
        return challenge, 200
    return "Forbidden", 403


# ─────────────────────────────────────────────
# Webhook Events (POST)
# ─────────────────────────────────────────────
@app.route("/webhook", methods=["POST"])
def handle_webhook():
    body = request.get_json()
    if not body:
        return "Bad Request", 400

    print(f"\n📨 Webhook received: {json.dumps(body, indent=2)}")

    if body.get("object") != "instagram":
        return "OK", 200

    for entry in body.get("entry", []):
        # ══════════════════════════════════════════
        # FIX 1: Only process webhooks for YOUR bot's page
        # Pick ONE entry ID that corresponds to your bot account
        # ══════════════════════════════════════════
        entry_id = entry.get("id")
        
        # IMPORTANT: Set this to YOUR BOT's Instagram account ID only
        # Based on your logs, your bot's account entry ID is "17841468343963858"
        if entry_id != Config.BOT_PAGE_ID:
            print(f"⏭️ Skipping entry from non-bot account: {entry_id}")
            continue

        for messaging_event in entry.get("messaging", []):
            process_message(messaging_event)

    return "OK", 200


def process_message(event: dict):
    sender_id = event.get("sender", {}).get("id")
    recipient_id = event.get("recipient", {}).get("id")
    message = event.get("message", {})
    postback = event.get("postback", {})

    if not sender_id:
        return

    # ══════════════════════════════════════════
    # FIX 2: Skip echo messages
    # ══════════════════════════════════════════
    if message.get("is_echo"):
        print(f"⏭️ Skipping echo from {sender_id}")
        return

    # ══════════════════════════════════════════
    # FIX 3: Skip messages FROM our own bot
    # The bot's sender ID when it sends = the recipient_id in config
    # ══════════════════════════════════════════
    if sender_id == Config.BOT_PAGE_ID or sender_id == Config.BOT_INSTAGRAM_ID:
        print(f"⏭️ Skipping message from bot itself: {sender_id}")
        return

    # ══════════════════════════════════════════
    # FIX 4: Deduplicate by message ID
    # Same message can arrive in multiple webhook entries
    # ══════════════════════════════════════════
    mid = message.get("mid") or postback.get("mid", "")
    if mid:
        if mid in processed_messages:
            print(f"⏭️ Skipping already-processed message: {mid[:50]}...")
            return
        
        # Add to processed set
        processed_messages.add(mid)
        
        # Prevent memory leak
        if len(processed_messages) > MAX_PROCESSED_CACHE:
            # Remove oldest half
            to_remove = list(processed_messages)[:MAX_PROCESSED_CACHE // 2]
            for item in to_remove:
                processed_messages.discard(item)

    # ══════════════════════════════════════════
    # FIX 5: Check if this message text matches what WE sent
    # (catches echoes that don't have is_echo flag)
    # ══════════════════════════════════════════
    if mid in sent_message_ids:
        print(f"⏭️ Skipping: this is a message WE sent (mid matched)")
        return

    # ══════════════════════════════════════════
    # FIX 6: Skip read receipts
    # ══════════════════════════════════════════
    if "read" in event:
        print(f"📖 Read receipt from {sender_id} — ignoring")
        return

    # Now process
    if message:
        handle_message(sender_id, message)
    elif postback:
        handle_postback(sender_id, postback)


def handle_message(sender_id: str, message: dict):
    text = message.get("text", "")

    # Handle attachments
    attachments = message.get("attachments", [])
    if attachments and not text:
        attachment_types = [a.get("type", "unknown") for a in attachments]
        text = f"[User sent: {', '.join(attachment_types)}]"

    # Handle quick replies
    quick_reply = message.get("quick_reply", {})
    if quick_reply:
        text = quick_reply.get("payload", text)

    if not text:
        send_and_track(sender_id, "I can only process text messages right now! 😊")
        return

    print(f"💬 Message from {sender_id}: {text}")

    # Generate AI reply
    reply = gemini_handler.generate_reply(sender_id, text)
    print(f"🤖 Reply to {sender_id}: {reply}")

    # Send reply
    send_and_track(sender_id, reply)


def handle_postback(sender_id: str, postback: dict):
    payload = postback.get("payload", "")
    title = postback.get("title", "")
    print(f"🔘 Postback from {sender_id}: {title} ({payload})")
    reply = gemini_handler.generate_reply(sender_id, payload or title)
    send_and_track(sender_id, reply)


def send_and_track(recipient_id: str, text: str):
    """Send message and track the message ID to prevent echo loops."""
    result = instagram_api.send_text_message(recipient_id, text)
    
    # Track the sent message ID
    sent_mid = result.get("message_id")
    if sent_mid:
        sent_message_ids.add(sent_mid)
        
        # Prevent memory leak
        if len(sent_message_ids) > MAX_SENT_CACHE:
            to_remove = list(sent_message_ids)[:MAX_SENT_CACHE // 2]
            for item in to_remove:
                sent_message_ids.discard(item)
    
    return result


# ─────────────────────────────────────────────
# Signature Verification
# ─────────────────────────────────────────────
@app.before_request
def verify_signature():
    if request.method != "POST" or request.path != "/webhook":
        return
    if not Config.INSTAGRAM_APP_SECRET:
        return
    signature = request.headers.get("X-Hub-Signature-256", "")
    if not signature:
        return
    expected = "sha256=" + hmac.new(
        Config.INSTAGRAM_APP_SECRET.encode(),
        request.get_data(),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return "Invalid signature", 403


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "bot": Config.BOT_NAME,
    })


if __name__ == "__main__":
    print(f"🤖 {Config.BOT_NAME} starting...")
    print(f"📡 Webhook URL: http://localhost:5000/webhook")
    app.run(host="0.0.0.0", port=5000, debug=True)