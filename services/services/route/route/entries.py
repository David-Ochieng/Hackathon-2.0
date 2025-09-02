from flask import Blueprint, request, jsonify
from models import db, Entry
from services.hf_api import analyze_emotion
from utils.auth_utils import token_required
import json

entries_bp = Blueprint("entries_bp", __name__)

@entries_bp.route("", methods=["POST"])
@token_required
def create_entry(user):
    data = request.get_json() or {}
    text = data.get("text")
    if not text:
        return jsonify({"error": "Text required"}), 400
    hf_result = analyze_emotion(text)
    # hf_result is usually a list like [{"label":"joy","score":0.98}, ...] or error
    emotion_label = None
    try:
        if isinstance(hf_result, list):
            # pick label with max score
            top = max(hf_result, key=lambda x: x.get("score", 0))
            emotion_label = top.get("label")
        elif isinstance(hf_result, dict) and "error" in hf_result:
            emotion_label = "unknown"
        else:
            emotion_label = str(hf_result)
    except Exception:
        emotion_label = "unknown"

    entry = Entry(user_id=user.id, text=text, emotion=emotion_label, scores=json.dumps(hf_result))
    db.session.add(entry)
    db.session.commit()
    return jsonify({"id": entry.id, "text": entry.text, "emotion": entry.emotion, "created_at": entry.created_at.isoformat()})

@entries_bp.route("", methods=["GET"])
@token_required
def list_entries(user):
    entries = Entry.query.filter_by(user_id=user.id).order_by(Entry.created_at.desc()).all()
    out = []
    for e in entries:
        out.append({"id": e.id, "text": e.text, "emotion": e.emotion, "scores": e.scores, "created_at": e.created_at.isoformat()})
    return jsonify(out)

@entries_bp.route("/<int:entry_id>", methods=["PUT"])
@token_required
def update_entry(user, entry_id):
    entry = Entry.query.filter_by(id=entry_id, user_id=user.id).first()
    if not entry:
        return jsonify({"error": "Entry not found"}), 404
    data = request.get_json() or {}
    text = data.get("text")
    if text:
        hf_result = analyze_emotion(text)
        try:
            if isinstance(hf_result, list):
                top = max(hf_result, key=lambda x: x.get("score", 0))
                entry.emotion = top.get("label")
            else:
                entry.emotion = "unknown"
            import json
            entry.scores = json.dumps(hf_result)
        except Exception:
            entry.emotion = "unknown"
        entry.text = text
    db.session.commit()
    return jsonify({"id": entry.id, "text": entry.text, "emotion": entry.emotion})

@entries_bp.route("/<int:entry_id>", methods=["DELETE"])
@token_required
def delete_entry(user, entry_id):
    entry = Entry.query.filter_by(id=entry_id, user_id=user.id).first()
    if not entry:
        return jsonify({"error": "Entry not found"}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"success": True})
