import streamlit as st
import os
import re

st.set_page_config(page_title="AirWrite", layout="wide")

DIST_DIR = os.path.join(os.getcwd(), "dist")

def main():
    if not os.path.exists(DIST_DIR):
        st.error(f"Build artifacts not found at {DIST_DIR}. Please run 'npm run build'.")
        return

    index_path = os.path.join(DIST_DIR, "index.html")
    if not os.path.exists(index_path):
        st.error(f"Index not found at {index_path}. Please run 'npm run build'.")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    error_script = """
    <script>
      (function() {
        // Patch URL to prevent crashes in srcdoc (iframe) environment
        var OriginalURL = window.URL;
        var SafeURL = function(url, base) {
          try {
            if (base) return new OriginalURL(url, base);
            return new OriginalURL(url);
          } catch (e) {
            console.warn("Streamlit Patch: URL construction failed. URL:", url, "Base:", base, "Error:", e.message);
            try {
              // Attempt to recover with a dummy base
              return new OriginalURL(url, "https://example.com");
            } catch (e2) {
              // Complete fallback if even that fails
              return new OriginalURL("https://example.com");
            }
          }
        };
        SafeURL.prototype = OriginalURL.prototype;
        // Copy static methods like createObjectURL
        for (var prop in OriginalURL) {
          if (Object.prototype.hasOwnProperty.call(OriginalURL, prop)) {
            SafeURL[prop] = OriginalURL[prop];
          }
        }
        window.URL = SafeURL;
      })();

      window.onerror = function(message, source, lineno, colno, error) {
        var errorDiv = document.createElement("div");
        errorDiv.style.color = "red";
        errorDiv.style.fontFamily = "monospace";
        errorDiv.style.backgroundColor = "#ffe6e6";
        errorDiv.style.padding = "10px";
        errorDiv.style.border = "1px solid red";
        errorDiv.style.margin = "10px";
        errorDiv.style.whiteSpace = "pre-wrap";
        errorDiv.innerText = "Runtime Error: " + message + "\\nSource: " + source + ":" + lineno + ":" + colno;
        document.body.prepend(errorDiv);
        console.error("Streamlit Caught Error:", message, error);
      };
      window.addEventListener('unhandledrejection', function(event) {
        var errorDiv = document.createElement("div");
        errorDiv.style.color = "orange";
        errorDiv.style.fontFamily = "monospace";
        errorDiv.style.backgroundColor = "#fff0e0";
        errorDiv.style.padding = "10px";
        errorDiv.style.border = "1px solid orange";
        errorDiv.style.margin = "10px";
        errorDiv.style.whiteSpace = "pre-wrap";
        errorDiv.innerText = "Promise Rejection: " + event.reason;
        document.body.prepend(errorDiv);
        console.error("Streamlit Caught Rejection:", event.reason);
      });
    </script>
    """

    if "<head>" in html_content:
        html_content = html_content.replace("<head>", "<head>" + error_script)
    elif "<body>" in html_content:
        html_content = html_content.replace("<body>", "<body>" + error_script)
    else:
        html_content = error_script + html_content

    # Inline CSS
    for match in list(re.finditer(r'<link([^>]+)>', html_content)):
        attrs = match.group(1)
        if 'rel="stylesheet"' in attrs or "rel='stylesheet'" in attrs:
            href_match = re.search(r"href=[\"']([^\"']+)[\"']", attrs)
            if href_match:
                css_href = href_match.group(1)
                css_path = css_href.lstrip("./").lstrip("/")
                full_css_path = os.path.join(DIST_DIR, css_path)
                if os.path.exists(full_css_path):
                    with open(full_css_path, "r", encoding="utf-8") as f:
                        css_content = f.read()
                    html_content = html_content.replace(match.group(0), f"<style>{css_content}</style>")

    # Inline JS bundle
    for match in list(re.finditer(r"<script([^>]*?)src=[\"']([^\"']+)[\"']([^>]*?)></script>", html_content)):
        full_tag = match.group(0)
        js_src = match.group(2)
        js_path = js_src.lstrip("./").lstrip("/")
        full_js_path = os.path.join(DIST_DIR, js_path)
        if os.path.exists(full_js_path):
            with open(full_js_path, "r", encoding="utf-8") as f:
                js_content = f.read()
            js_content = js_content.replace("http://localhost", "https://example.local")
            html_content = html_content.replace(full_tag, f"<script type='module'>{js_content}</script>")

    st.components.v1.html(html_content, height=900, scrolling=True)

if __name__ == "__main__":
    main()
