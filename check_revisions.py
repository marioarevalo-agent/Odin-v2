import subprocess, json

# Revisions from June 23 (Carlos Mario's work)
revisions = [
    "proy-anla-poc-00131-4fj", "proy-anla-poc-00132-b7f", "proy-anla-poc-00133-f7q",
    "proy-anla-poc-00134-7mp", "proy-anla-poc-00135-9hk", "proy-anla-poc-00136-ldn",
    "proy-anla-poc-00137-vfx", "proy-anla-poc-00138-zp2", "proy-anla-poc-00139-rnb",
    "proy-anla-poc-00140-7gv", "proy-anla-poc-00141-st5", "proy-anla-poc-00142-6mv",
    "proy-anla-poc-00143-mlr", "proy-anla-poc-00144-wk2", "proy-anla-poc-00145-4mc",
    "proy-anla-poc-00146-8kb", "proy-anla-poc-00147-k56", "proy-anla-poc-00148-7x5",
    "proy-anla-poc-00149-sdw", "proy-anla-poc-00150-dj9", "proy-anla-poc-00151-7mq",
    "proy-anla-poc-00152-2xk", "proy-anla-poc-00153-2dm", "proy-anla-poc-00154-5xt",
    "proy-anla-poc-00155-trc", "proy-anla-poc-00156-rh5", "proy-anla-poc-00157-jgv",
    "proy-anla-poc-00158-hv4"
]

for rev in revisions:
    try:
        result = subprocess.run(
            ["gcloud", "run", "revisions", "describe", rev, "--region", "us-central1", 
             "--project", "proy-anla-poc", "--format=json"],
            capture_output=True, text=True, timeout=15
        )
        data = json.loads(result.stdout)
        meta = data.get("metadata", {})
        ann = meta.get("annotations", {})
        creator = ann.get("serving.knative.dev/creator", "?")
        created = meta.get("creationTimestamp", "?")
        # Get image digest for change tracking
        containers = data.get("spec", {}).get("containers", [{}])
        image = containers[0].get("image", "?") if containers else "?"
        image_short = image.split("/")[-1][:50] if "/" in image else image[:50]
        print(f"{rev}  {created[:19]}  {creator:30s}  {image_short}")
    except Exception as e:
        print(f"{rev}  ERROR: {e}")
