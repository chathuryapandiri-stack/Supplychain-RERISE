"""
ResilientAI - Stlite / Vercel WebAssembly Static Bundler
Packages Python application modules, CSV datasets, and Streamlit pages
into a standalone static web application runnable directly in the browser on Vercel.
"""

import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(ROOT_DIR, "public")
os.makedirs(PUBLIC_DIR, exist_ok=True)

# Collect all application code and datasets
bundled_files = {}

include_dirs = ["core", "pages", "data"]
include_single_files = ["app.py"]

for f in include_single_files:
    file_path = os.path.join(ROOT_DIR, f)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as src:
            bundled_files[f] = src.read()

for dir_name in include_dirs:
    dir_path = os.path.join(ROOT_DIR, dir_name)
    if not os.path.exists(dir_path):
        continue
    for root, _, files in os.walk(dir_path):
        if "__pycache__" in root:
            continue
        for file_name in files:
            if file_name.endswith(".py") or file_name.endswith(".csv"):
                full_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")
                with open(full_path, "r", encoding="utf-8") as src:
                    bundled_files[rel_path] = src.read()

print(f"Bundled {len(bundled_files)} files into Vercel static distribution:")
for k in sorted(bundled_files.keys()):
    print(f"  - {k} ({len(bundled_files[k])} bytes)")

html_content = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>ResilientAI | Supply Chain Command Center</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.73.0/build/stlite.css" />
    <style>
      html, body {{
        margin: 0;
        padding: 0;
        background-color: #0D1117;
        color: #E6EDF3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
        height: 100%;
        overflow-x: hidden;
      }}
      #loading-screen {{
        position: fixed;
        inset: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #0D1117;
        z-index: 99999;
        transition: opacity 0.4s ease, visibility 0.4s ease;
      }}
      .loader-card {{
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 32px 40px;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        max-width: 420px;
        text-align: center;
      }}
      .spinner {{
        width: 36px;
        height: 36px;
        border: 3px solid #21262D;
        border-top-color: #388BFD;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        margin-bottom: 20px;
      }}
      @keyframes spin {{
        to {{ transform: rotate(360deg); }}
      }}
      .loader-title {{
        font-size: 1.15rem;
        font-weight: 700;
        color: #F0F6FC;
        margin-bottom: 6px;
        letter-spacing: -0.01em;
      }}
      .loader-sub {{
        font-size: 0.80rem;
        color: #8B949E;
        line-height: 1.4;
      }}
      .loader-pill {{
        margin-top: 16px;
        font-size: 0.70rem;
        font-family: "JetBrains Mono", monospace;
        color: #58A6FF;
        background: rgba(56, 139, 253, 0.1);
        padding: 4px 10px;
        border-radius: 12px;
        border: 1px solid rgba(56, 139, 253, 0.25);
      }}
    </style>
  </head>
  <body>
    <div id="loading-screen">
      <div class="loader-card">
        <div class="spinner"></div>
        <div class="loader-title">ResilientAI Command Center</div>
        <div class="loader-sub">Initializing browser WebAssembly Python environment & optimization models...</div>
        <div class="loader-pill">Vercel Serverless Frontend • Pyodide</div>
      </div>
    </div>
    <div id="root"></div>

    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.73.0/build/stlite.js"></script>
    <script>
      const bundledFiles = {json.dumps(bundled_files, indent=2)};

      stlite.mount({{
        requirements: ["pandas", "numpy", "plotly"],
        entrypoint: "app.py",
        files: bundledFiles
      }}, document.getElementById("root")).then(() => {{
        const loader = document.getElementById("loading-screen");
        if (loader) {{
          loader.style.opacity = "0";
          setTimeout(() => {{
            loader.style.visibility = "hidden";
            loader.remove();
          }}, 400);
        }}
      }}).catch(err => {{
        console.error("Failed to mount Stlite:", err);
        const sub = document.querySelector(".loader-sub");
        if (sub) {{
          sub.innerText = "Error initializing WebAssembly runtime: " + err.message;
          sub.style.color = "#DA3633";
        }}
      }});
    </script>
  </body>
</html>
"""

output_html_path = os.path.join(PUBLIC_DIR, "index.html")
with open(output_html_path, "w", encoding="utf-8") as out:
    out.write(html_content)

print(f"\nSuccessfully generated Vercel frontend entrypoint at: {output_html_path}")
print(f"Total HTML bundle size: {len(html_content):,} bytes")
