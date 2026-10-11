import json
import urllib.request

from dotenv import load_dotenv

load_dotenv()

ENDPOINT = "https://opencode.ai/zen/v1/systemone"


def score_urgency(transcription_text):
    """
    Scores a transcript for urgency with jev-1.13-free.

    Returns the score answer dict (score, confidence, legend, probabilities)
    on a 0-4 rubric, or None if the API call fails.
    """
    payload = {
        "model": "jev-1.13-free",
        "state": transcription_text,
        "questions": {
            "urgency": {
                "type": "score",
                "instructions": "How urgent is this situation?",
                "criteria": [
                    "Not urgent",
                    "Low",
                    "Medium",
                    "High",
                    "Critical",
                ],
            }
        },
    }

    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "jev-project/0.1.0",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)["answers"]["urgency"]
    except Exception as e:
        print(f"Error during API call: {e}")
        return None


# --- Quick Test ---
if __name__ == "__main__":
    sample_transcript = "My foot is dying"
    print("Scoring transcript...")
    result = score_urgency(sample_transcript)
    print(json.dumps(result, indent=2))
