IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp")
VIDEO_HINTS = ("youtube.com", "youtu.be", ".mp4", "loom.com")
DEMO_HINTS = ("streamlit.app", "vercel.app", "netlify.app", "huggingface.co")


def analyze_proof_of_work(readme_text: str):
    if not readme_text:
        return {"score": "WEAK", "signals": []}

    text = readme_text.lower()
    signals = []

    # Markdown images or raw image links
    if any(ext in text for ext in IMAGE_EXTS):
        signals.append("screenshots")

    if any(v in text for v in VIDEO_HINTS):
        signals.append("video-demo")

    if any(d in text for d in DEMO_HINTS):
        signals.append("live-demo")

    score = "STRONG" if signals else "WEAK"

    return {
        "score": score,
        "signals": sorted(set(signals))
    }
