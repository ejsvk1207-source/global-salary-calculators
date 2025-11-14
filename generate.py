import os

# 0. AdSense snippet (your real code here)
ADSENSE_SNIPPET = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5480469641280477"
     crossorigin="anonymous"></script>
"""

SITE_URL = "https://ejsvk1207-source.github.io"

TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{TITLE}}</title>
  <meta name="description" content="{{DESCRIPTION}}">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {{ADSENSE_SNIPPET}}
  <link rel="stylesheet" href="style.css">
</head>
<body>

<header>
  <h1>{{TITLE}}</h1>
  <p class="subtitle">{{COUNTRY}} · {{JOB}} · {{CURRENCY}}</p>
</header>

<main>
  <section class="intro">
    <p>{{DESCRIPTION}}</p>
    <p class="disclaimer">
      This tool gives a simplified estimate of take-home salary.
      Real tax systems are more complex and vary by region.
    </p>
  </section>

  <section class="calculator">
    <h2>Enter your salary</h2>
    <form id="salary-form">
      <label>
        Gross yearly salary ({{CURRENCY}}):
        <input type="number" id="grossYearly" required min="0" step="100">
      </label>

      <label>
        Optional yearly bonus ({{CURRENCY}}):
        <input type="number" id="bonusYearly" min="0" step="100">
      </label>

      <button type="submit">Calculate net salary</button>
    </form>

    <div id="result" class="result hidden">
      <h2>Estimated take-home pay</h2>
      <p>Yearly net: <span id="netYearly"></span> {{CURRENCY}}</p>
      <p>Monthly net: <span id="netMonthly"></span> {{CURRENCY}}</p>
      <p>Weekly net: <span id="netWeekly"></span> {{CURRENCY}}</p>
    </div>
  </section>

  <footer>
    <p>
      Part of the Global Salary Calculators project —
      <a href="index.html">Back to index</a> ·
      <a href="privacy.html">Privacy Policy</a> ·
      <a href="disclaimer.html">Disclaimer</a>
    </p>
  </footer>
</main>

<script>
  window.calculatorConfig = {
    "tax_rate": {{TAX_RATE}},
    "social_rate": {{SOCIAL_RATE}}
  };
</script>
<script src="script.js"></script>

</body>
</html>
"""

SCRIPT_JS = """document.addEventListener("DOMContentLoaded", () => {
  const cfg = window.calculatorConfig;
  const form = document.getElementById("salary-form");
  const result = document.getElementById("result");
  const netY = document.getElementById("netYearly");
  const netM = document.getElementById("netMonthly");
  const netW = document.getElementById("netWeekly");

  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    let g = Number(document.getElementById("grossYearly").value);
    let b = Number(document.getElementById("bonusYearly").value || 0);
    if (!g) return alert("Enter valid salary.");

    let total = g + b;
    let rate = Math.min(cfg.tax_rate + cfg.social_rate, 0.8);

    let net = total * (1 - rate);
    netY.textContent = net.toLocaleString();
    netM.textContent = (net / 12).toLocaleString();
    netW.textContent = (net / 52).toLocaleString();

    result.classList.remove("hidden");
  });
});
"""

STYLE_CSS = """body {
  font-family: system-ui;
  background: #f6f6f6;
  margin: 0;
  padding: 0;
}
header {
  background: #fff;
  padding: 20px;
  border-bottom: 1px solid #ddd;
}
h1 { margin: 0 0 5px; }
.subtitle { color: #777; font-size: 0.9rem; }
main { max-width: 900px; margin: 20px auto; padding: 0 20px; }
section {
  background: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
}
.hidden { display: none; }
button {
  background: #0070f3;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  color: #fff;
  cursor: pointer;
}
button:hover { background: #0059d1; }
a { color: #0070f3; }
"""

README_CONTENT = """# Global Salary Calculators

Static salary calculator site for many countries and jobs.
Generated automatically by generate.py and hosted on GitHub Pages.

Site URL: https://ejsvk1207-source.github.io
"""

PRIVACY_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Privacy Policy</title></head>
<body>
<h1>Privacy Policy</h1>
<p>This website may use third-party advertising networks such as Google AdSense.</p>
<p>These networks may use cookies to personalize and measure ads. We do not store
personally identifiable information on this site. Any salary values you enter are
processed only in your browser.</p>
<p>For more information, see Google's privacy policy.</p>
<p><a href="index.html">Back to main page</a></p>
</body></html>
"""

DISCLAIMER_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Disclaimer</title></head>
<body>
<h1>Disclaimer</h1>
<p>All salary calculators on this site use simplified average tax and social
contribution rates. Real results may differ significantly.</p>
<p>Nothing on this site is financial, legal, or tax advice. Please consult official
resources or a professional advisor for accurate information.</p>
<p><a href="index.html">Back to main page</a></p>
</body></html>
"""

# 일단은 테스트용으로 나라/직업을 줄여두었음 (애드센스 통과 후 다시 늘리자)
COUNTRIES = [
    {"code": "us", "name": "United States", "currency": "USD", "tax_rate": 0.22, "social_rate": 0.076},
    {"code": "in", "name": "India", "currency": "INR", "tax_rate": 0.18, "social_rate": 0.03},
]

JOBS = [
    "Software Engineer",
    "Teacher",
    "Nurse",
    "Doctor",
    "Factory Worker",
]

def slugify(text):
    return (
        text.lower()
        .replace(" ", "-")
        .replace("&", "and")
        .replace("/", "-")
        .replace(",", "")
        .replace(".", "")
    )

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # 공통 파일
    write("template.html", TEMPLATE_HTML)
    write("script.js", SCRIPT_JS)
    write("style.css", STYLE_CSS)
    write("README.md", README_CONTENT)

    calculators = []
    template = TEMPLATE_HTML.replace("{{ADSENSE_SNIPPET}}", ADSENSE_SNIPPET.strip())

    # 각 계산기 페이지 생성
    for c in COUNTRIES:
        for j in JOBS:
            slug = f"{c['code']}-{slugify(j)}-salary-calculator"
            filename = f"{slug}.html"
            title = f"{c['name']} {j} Net Salary Calculator"
            desc = f"Calculate simplified take-home pay for a {j} in {c['name']}."

            html = (
                template
                .replace("{{TITLE}}", title)
                .replace("{{DESCRIPTION}}", desc)
                .replace("{{COUNTRY}}", c["name"])
                .replace("{{JOB}}", j)
                .replace("{{CURRENCY}}", c["currency"])
                .replace("{{TAX_RATE}}", str(c["tax_rate"]))
                .replace("{{SOCIAL_RATE}}", str(c["social_rate"]))
            )

            write(filename, html)
            calculators.append({"slug": slug, "title": title})

    # index.html (여기도 애드센스 코드 포함)
    index_html = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Global Salary Calculators</title>"
    index_html += "<meta name='description' content='Simplified net salary calculators for many jobs and countries.'>"
    index_html += ADSENSE_SNIPPET
    index_html += "<link rel='stylesheet' href='style.css'></head><body>"
    index_html += "<header><h1>Global Salary Calculators</h1></header><main><ul>"
    for m in calculators:
        index_html += f"<li><a href='{m['slug']}.html'>{m['title']}</a></li>"
    index_html += "</ul>"
    index_html += "<p><a href='privacy.html'>Privacy Policy</a> · <a href='disclaimer.html'>Disclaimer</a></p>"
    index_html += "</main></body></html>"
    write("index.html", index_html)

    # privacy / disclaimer
    write("privacy.html", PRIVACY_HTML)
    write("disclaimer.html", DISCLAIMER_HTML)

    # sitemap.xml
    sitemap = "<?xml version='1.0' encoding='UTF-8'?>\n<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>\n"
    sitemap += f"  <url><loc>{SITE_URL}/</loc></url>\n"
    for m in calculators:
        sitemap += f"  <url><loc>{SITE_URL}/{m['slug']}.html</loc></url>\n"
    sitemap += f"  <url><loc>{SITE_URL}/privacy.html</loc></url>\n"
    sitemap += f"  <url><loc>{SITE_URL}/disclaimer.html</loc></url>\n"
    sitemap += "</urlset>\n"
    write("sitemap.xml", sitemap)

    # robots.txt
    robots = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    write("robots.txt", robots)

    print("DONE: all pages generated in repo root.")

if __name__ == "__main__":
    main()
