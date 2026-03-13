import json
import os
from datetime import datetime
from flask import Flask, jsonify, render_template, request

import anthropic

app = Flask(__name__)

EVENTS_FILE = os.path.join(os.path.dirname(__file__), "events.json")
KRYO_MD = os.path.join(os.path.dirname(__file__), "..", "KRYO.md")

def load_events():
    with open(EVENTS_FILE) as f:
        return json.load(f)

def save_events(data):
    with open(EVENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_kryo_context():
    try:
        with open(KRYO_MD) as f:
            return f.read()
    except FileNotFoundError:
        return "KRYO is an apartment-friendly cold shower system launching in Dubai."

def build_system_prompt():
    kryo_context = load_kryo_context()
    events_data = load_events()
    today = datetime.now().strftime("%Y-%m-%d")

    events_text = "\n".join([
        f"- [{e['status'].upper()}] {e['title']} ({e['start']} to {e['end']}): {e['description']}"
        for e in events_data["events"]
    ])

    return f"""You are the KRYO Launch Assistant — an expert on the KRYO product launch in Dubai.
Today's date is {today}.

## KRYO Product Context
{kryo_context}

## Current Launch Calendar
{events_text}

## Your Role
You help the founder (Happy) stay on top of the KRYO launch by:
- Answering questions about the schedule and what's happening now
- Flagging what needs attention this week
- Suggesting next actions based on where things stand
- Tracking progress and providing strategic advice
- Creating new calendar events when asked (respond with JSON in this exact format when creating events):
  SCHEDULE_EVENT: {{"title": "...", "start": "YYYY-MM-DD", "end": "YYYY-MM-DD", "description": "...", "category": "creative|technical|paid-media|analysis|milestone", "color": "#3B82F6|#8B5CF6|#F59E0B|#10B981|#EF4444"}}

Keep responses concise and actionable. You know this business inside out.
Category colors: creative=#3B82F6, technical=#8B5CF6, paid-media=#F59E0B, analysis=#10B981, milestone=#EF4444"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/events", methods=["GET"])
def get_events():
    data = load_events()
    return jsonify(data["events"])


@app.route("/api/events", methods=["POST"])
def add_event():
    body = request.get_json()
    if not body or not body.get("title") or not body.get("start"):
        return jsonify({"error": "title and start are required"}), 400

    data = load_events()
    new_id = str(max((int(e["id"]) for e in data["events"]), default=0) + 1)
    category = body.get("category", "milestone")
    color_map = {
        "creative": "#3B82F6",
        "technical": "#8B5CF6",
        "paid-media": "#F59E0B",
        "analysis": "#10B981",
        "milestone": "#EF4444",
    }
    event = {
        "id": new_id,
        "title": body["title"],
        "start": body["start"],
        "end": body.get("end", body["start"]),
        "description": body.get("description", ""),
        "category": category,
        "color": body.get("color", color_map.get(category, "#EF4444")),
        "status": body.get("status", "upcoming"),
    }
    data["events"].append(event)
    save_events(data)
    return jsonify(event), 201


@app.route("/api/chat", methods=["POST"])
def chat():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY environment variable not set. Run: export ANTHROPIC_API_KEY=your_key"}), 500

    body = request.get_json()
    if not body or not body.get("messages"):
        return jsonify({"error": "messages array required"}), 400

    messages = body["messages"]

    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=build_system_prompt(),
        messages=messages,
    )

    reply_text = next(
        (block.text for block in response.content if block.type == "text"), ""
    )

    # Parse any SCHEDULE_EVENT commands from the reply
    scheduled = None
    if "SCHEDULE_EVENT:" in reply_text:
        try:
            marker = "SCHEDULE_EVENT:"
            idx = reply_text.index(marker) + len(marker)
            json_str = reply_text[idx:].strip()
            # Find end of JSON object
            brace_count = 0
            end_idx = 0
            for i, ch in enumerate(json_str):
                if ch == "{":
                    brace_count += 1
                elif ch == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            event_data = json.loads(json_str[:end_idx])

            data = load_events()
            new_id = str(max((int(e["id"]) for e in data["events"]), default=0) + 1)
            category = event_data.get("category", "milestone")
            color_map = {
                "creative": "#3B82F6",
                "technical": "#8B5CF6",
                "paid-media": "#F59E0B",
                "analysis": "#10B981",
                "milestone": "#EF4444",
            }
            event = {
                "id": new_id,
                "title": event_data.get("title", "New Event"),
                "start": event_data.get("start", datetime.now().strftime("%Y-%m-%d")),
                "end": event_data.get("end", event_data.get("start", datetime.now().strftime("%Y-%m-%d"))),
                "description": event_data.get("description", ""),
                "category": category,
                "color": event_data.get("color", color_map.get(category, "#EF4444")),
                "status": "upcoming",
            }
            data["events"].append(event)
            save_events(data)
            scheduled = event

            # Clean the SCHEDULE_EVENT marker from the reply
            reply_text = reply_text[:reply_text.index("SCHEDULE_EVENT:")].strip()
        except Exception:
            pass  # If parsing fails, just return the reply as-is

    return jsonify({
        "reply": reply_text,
        "scheduled_event": scheduled,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"\n KRYO Launch Calendar running at http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
