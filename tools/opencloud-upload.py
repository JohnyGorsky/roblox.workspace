# -*- coding: utf-8 -*-
"""opencloud-upload.py -- upload 3D models (.glb / .fbx) to Roblox as Model assets via Open Cloud, print their ids.

Owner, 2026-11-03 ("guide me to create access token so you can upload"): Claude cannot click Studio's Import 3D, so
models made with Meshy are uploaded through the Open Cloud Assets API and then inserted into the place by id.

The API key is the OWNER's: an "Assets" (Read + Write) key from create.roblox.com/dashboard/credentials, saved by the
owner as plain text in   C:\\Users\\janis\\.roblox\\opencloud-key.txt   (override: env ROBLOX_OPENCLOUD_KEY_FILE).
This tool reads it from there, sends it only to apis.roblox.com, and NEVER prints, logs or copies it. Never put the
key in a repo, a job file or a chat.

Usage (from anywhere; Python's -I keeps the downloaded-files folder off the import path):
    python -I opencloud-upload.py --check                       # key file present + accepted? uploads nothing
    python -I opencloud-upload.py --user-id 5025640608 --out results.json  model1.glb [model2.glb ...]
Options:
    --name-prefix cf_     display name = prefix + file stem (default: the file stem)
    --description TEXT    asset description (default: "MAGNET SWEEP model")
Exit 0 = every file uploaded; 1 = at least one failed (each file's outcome is printed and written to --out).

API (create.roblox.com/docs/cloud/guides/usage-assets): POST https://apis.roblox.com/assets/v1/assets, multipart:
`request` (JSON: assetType "Model", displayName, description, creationContext.creator.userId) + `fileContent`
(model/gltf-binary for .glb, model/fbx for .fbx; 20 MB max). The reply is an operation; poll
GET /assets/v1/operations/{id} until done -> response.assetId. Models arrive as packages (Toolbox > My Packages).
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

API = "https://apis.roblox.com/assets/v1"
DEFAULT_KEY_FILE = os.path.join(os.path.expanduser("~"), ".roblox", "opencloud-key.txt")
CONTENT_TYPES = {".glb": "model/gltf-binary", ".fbx": "model/fbx", ".gltf": "model/gltf+json"}
MAX_BYTES = 20 * 1024 * 1024


def read_key() -> str:
    path = os.environ.get("ROBLOX_OPENCLOUD_KEY_FILE", DEFAULT_KEY_FILE)
    if not os.path.isfile(path):
        sys.exit("NO KEY FILE at %s -- create the Open Cloud key and save it there (see this file's header)" % path)
    with open(path, encoding="utf-8-sig") as f:
        key = f.read().strip()
    if not key or any(c.isspace() for c in key):
        sys.exit("KEY FILE at %s is empty or holds more than one line -- paste only the key" % path)
    return key


def call(method: str, url: str, key: str, body: bytes = None, content_type: str = None):
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("x-api-key", key)
    if content_type:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        text = e.read().decode("utf-8", "replace")[:500]
        return e.code, {"error": text}


def multipart(fields: dict, file_field: str, filename: str, file_type: str, data: bytes):
    boundary = "----msweep" + uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n" % (boundary, name, value)).encode("utf-8"))
    parts.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\nContent-Type: %s\r\n\r\n"
                  % (boundary, file_field, filename, file_type)).encode("utf-8"))
    parts.append(data)
    parts.append(("\r\n--%s--\r\n" % boundary).encode("utf-8"))
    return b"".join(parts), "multipart/form-data; boundary=" + boundary


def upload(path: str, key: str, user_id: str, prefix: str, description: str) -> dict:
    stem, ext = os.path.splitext(os.path.basename(path))
    ext = ext.lower()
    if ext not in CONTENT_TYPES:
        return {"file": path, "ok": False, "error": "unsupported type %s (use .glb or .fbx)" % ext}
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        return {"file": path, "ok": False, "error": "%.1f MB is over Open Cloud's 20 MB limit" % (size / 1048576)}
    request = {
        "assetType": "Model",
        "displayName": (prefix + stem)[:50],
        "description": description,
        "creationContext": {"creator": {"userId": str(user_id)}},
    }
    with open(path, "rb") as f:
        body, ctype = multipart({"request": json.dumps(request)}, "fileContent", os.path.basename(path), CONTENT_TYPES[ext], f.read())
    status, reply = call("POST", API + "/assets", key, body, ctype)
    if status >= 300 or "path" not in reply:
        return {"file": path, "ok": False, "error": "HTTP %d %s" % (status, reply.get("error", reply))}
    op = reply["path"]  # "operations/<id>"
    for _ in range(90):  # up to ~3 minutes
        time.sleep(2)
        status, state = call("GET", API + "/" + op, key)
        if status >= 300:
            return {"file": path, "ok": False, "error": "poll HTTP %d %s" % (status, state.get("error", state))}
        if state.get("done"):
            resp = state.get("response") or {}
            asset_id = resp.get("assetId")
            if asset_id:
                return {"file": path, "ok": True, "assetId": str(asset_id), "displayName": request["displayName"],
                        "moderation": (resp.get("moderationResult") or {}).get("moderationState")}
            return {"file": path, "ok": False, "error": "done without an asset id: %s" % json.dumps(state)[:400]}
    return {"file": path, "ok": False, "error": "still processing after 3 min (operation %s)" % op}


def main():
    ap = argparse.ArgumentParser(description="Upload .glb/.fbx models to Roblox via Open Cloud (see the file header).")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--check", action="store_true", help="only check the key file exists and is non-empty; uploads nothing")
    ap.add_argument("--user-id", help="the owner's Roblox user id (the asset's creator)")
    ap.add_argument("--out", help="write the results as JSON here")
    ap.add_argument("--name-prefix", default="")
    ap.add_argument("--description", default="MAGNET SWEEP model")
    args = ap.parse_args()
    key = read_key()
    if args.check:
        # Roblox's own introspect endpoint: the key's scopes and status, never the key itself
        status, info = call("POST", "https://apis.roblox.com/api-keys/v1/introspect", key,
                            json.dumps({"apiKey": key}).encode("utf-8"), "application/json")
        if status >= 300:
            print("KEY FILE read (%d characters, not shown) but introspect said HTTP %d: %s" % (len(key), status, info.get("error", info)))
            return 1
        scopes = info.get("scopes") or []
        print("KEY OK -- name %r, enabled %s, expired %s, scopes %s" % (info.get("name"), info.get("enabled"), info.get("expired"),
              ", ".join("%s:%s" % (s.get("name"), "/".join(s.get("operations") or [])) for s in scopes) or "none"))
        return 0
    if not args.files or not args.user_id:
        ap.error("give --user-id and at least one file (or --check)")
    results = []
    for path in args.files:
        r = upload(path, key, args.user_id, args.name_prefix, args.description)
        results.append(r)
        print(("OK   %s -> %s (%s)" % (os.path.basename(path), r["assetId"], r.get("moderation"))) if r["ok"]
              else ("FAIL %s: %s" % (os.path.basename(path), r["error"])))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
