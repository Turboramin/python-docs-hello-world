from datetime import datetime, timezone
from flask import Flask, request, render_template_string

app = Flask(__name__)

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Subdomain Takeover PoC — Ramin Topfer / Bug Bounty Switzerland</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: radial-gradient(1200px 600px at 50% -10%, #1b2740 0%, #0b0f19 60%, #070a12 100%);
    color: #e7ecf5; line-height: 1.6;
    display: flex; justify-content: center; padding: 40px 20px;
  }
  .wrap { width: 100%; max-width: 860px; }
  .card {
    background: rgba(19, 25, 40, 0.75);
    border: 1px solid rgba(120, 140, 190, 0.18);
    border-radius: 16px; padding: 34px 34px 26px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
    backdrop-filter: blur(6px);
  }
  .badge {
    display: inline-block; font-size: 12px; letter-spacing: .12em; text-transform: uppercase;
    color: #ffb454; border: 1px solid rgba(255,180,84,.4); background: rgba(255,180,84,.08);
    padding: 5px 12px; border-radius: 999px; font-weight: 600;
  }
  h1 { font-size: 30px; margin: 18px 0 6px; letter-spacing: -0.02em; }
  h1 .accent { color: #6ea8ff; }
  .sub { color: #9fb0cc; margin: 0 0 22px; font-size: 15px; }
  .host {
    font-family: "SF Mono", ui-monospace, Consolas, Menlo, monospace;
    background: #0a1020; border: 1px solid rgba(110,168,255,.25);
    color: #7fe0a8; padding: 14px 16px; border-radius: 10px;
    font-size: 15px; word-break: break-all; margin: 0 0 26px;
  }
  .host .k { color: #6b7ea3; user-select: none; }
  h2 { font-size: 16px; text-transform: uppercase; letter-spacing: .08em;
       color: #9fb0cc; margin: 26px 0 12px; border-bottom: 1px solid rgba(120,140,190,.15); padding-bottom: 8px; }
  ul.impact { list-style: none; margin: 0; padding: 0; display: grid; gap: 12px; }
  ul.impact li {
    background: rgba(10, 16, 32, 0.6); border: 1px solid rgba(120,140,190,.12);
    border-left: 3px solid #6ea8ff; border-radius: 8px; padding: 12px 16px; font-size: 14.5px;
  }
  ul.impact li b { color: #e7ecf5; }
  ul.impact li span { color: #a9b8d4; }
  .disclaimer {
    margin-top: 26px; background: rgba(46, 160, 110, 0.08);
    border: 1px solid rgba(70, 200, 140, 0.3); border-radius: 10px;
    padding: 16px 18px; font-size: 13.5px; color: #cde9db;
  }
  .disclaimer b { color: #7fe0a8; }
  .footer {
    margin-top: 26px; padding-top: 18px; border-top: 1px solid rgba(120,140,190,.15);
    display: flex; flex-wrap: wrap; gap: 8px 18px; align-items: center; justify-content: space-between;
    font-size: 13px; color: #8598ba;
  }
  .footer a { color: #6ea8ff; text-decoration: none; }
  .footer a:hover { text-decoration: underline; }
  .who { font-weight: 600; color: #e7ecf5; }
</style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <span class="badge">● Security Research — Proof of Concept</span>
      <h1>Subdomain <span class="accent">Takeover</span> confirmed</h1>
      <p class="sub">This page is being served from infrastructure controlled by an independent security
      researcher — not by the domain owner. If you can read this, the hostname below was pointing
      (via a dangling DNS/CNAME record) to a decommissioned cloud resource that has now been re-registered.</p>

      <div class="host"><span class="k">Controlled hostname &rarr; </span>{{ host }}</div>

      <h2>Why this matters — what a real attacker could do</h2>
      <ul class="impact">
        <li><b>Credential phishing on a trusted domain.</b>
          <span>Host a pixel-perfect login page on your own subdomain. Victims (staff, customers)
          see the legitimate domain in the address bar and have no reason to suspect it.</span></li>
        <li><b>Session &amp; cookie theft.</b>
          <span>If any cookies are scoped to the parent domain, a controlled subdomain can read or
          set them — enabling session hijacking or CSRF against the main application.</span></li>
        <li><b>OAuth / SSO token theft.</b>
          <span>If this hostname is a whitelisted redirect URI for a login flow, auth codes and
          access tokens can be intercepted and replayed.</span></li>
        <li><b>CSP / CORS allow-list bypass.</b>
          <span>If the main site trusts <code>*.your-domain</code> in its Content-Security-Policy or
          CORS rules, an attacker can inject scripts or read cross-origin data on the primary app.</span></li>
        <li><b>Malware delivery &amp; brand abuse.</b>
          <span>Serve malware, scams, or defacement under your trusted brand — damaging reputation
          and potentially poisoning email/link reputation.</span></li>
      </ul>

      <div class="disclaimer">
        <b>Please read — nothing of yours was touched.</b> This is an <b>authorized, non-destructive</b>
        proof of concept. No data, files, content, configuration, or systems belonging to your organization
        were accessed, modified, or deleted. This page only appears because a dangling DNS record pointed to
        an unclaimed cloud resource, which was re-registered solely to demonstrate the issue — a harmless
        CNAME takeover. Please refer to the corresponding report on your <b>Bug Bounty Switzerland (BBS)</b>
        program for full details and remediation steps. The hostname can be released back to you immediately
        on request.
      </div>

      <div class="footer">
        <span>Reported by <span class="who">Ramin Topfer</span> · Bug Bounty Switzerland (BBS)</span>
        <span>
          <a href="https://www.linkedin.com/in/ramintopfer/" target="_blank" rel="noopener">LinkedIn</a>
          &nbsp;·&nbsp; PoC captured {{ ts }} UTC
        </span>
      </div>
    </div>
  </div>
</body>
</html>"""


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def poc(path):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(PAGE, host=request.host, ts=ts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
