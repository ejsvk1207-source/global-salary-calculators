import os

# ===============================
# 0) 애드센스 코드 자리
# ===============================
# ▶ 애드센스 승인 받은 다음, 애드센스에서 준 "Auto ads 코드"를
#    아래 ADSENSE_SNIPPET 안에 그대로 붙여넣으면 됨.
#
# 예시 형태 (실제 ID는 네 계정 걸로 갈 것):
# <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
#         crossorigin="anonymous"></script>
#
# 처음에는 그냥 "" 비워둔 채로 사이트 만들고, 나중에 승인 나면 채워 넣고
# python generate.py 다시 실행 + git push 하면 끝.
ADSENSE_SNIPPET = """
"""

# ===============================
# 1) 기본 템플릿 / 스타일 / 스크립트 정의
# ===============================

TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{TITLE}}</title>
  <meta name="description" content="{{DESCRIPTION}}">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {{ADSENSE_SNIPPET}}
  <link rel="stylesheet" href="../style.css">
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
        This tool gives a <strong>rough, simplified estimate</strong> of your net salary (take-home pay).
        Real tax systems are more complex and change over time. For exact numbers, use official
        government calculators or consult a professional.
      </p>
    </section>

    <section class="calculator">
      <h2>Enter your salary</h2>
      <form id="salary-form">
        <label>
          Gross yearly salary (before tax) in {{CURRENCY}}:
          <input type="number" id="grossYearly" placeholder="e.g. 60000" required min="0" step="100">
        </label>

        <label>
          Optional yearly bonus in {{CURRENCY}}:
          <input type="number" id="bonusYearly" placeholder="e.g. 5000" min="0" step="100">
        </label>

        <button type="submit">Calculate net salary</button>
      </form>

      <div id="result" class="result hidden">
        <h2>Estimated take-home pay</h2>
        <p class="result-number">
          Yearly net: <span id="netYearly"></span> {{CURRENCY}}
        </p>
        <p class="result-number">
          Monthly net: <span id="netMonthly"></span> {{CURRENCY}}
        </p>
        <p class="result-number">
          Weekly net: <span id="netWeekly"></span> {{CURRENCY}}
        </p>

        <p class="details">
          We used an approximate income tax rate of <strong>{{TAX_RATE_PERCENT}}%</strong> and
          social contributions of <strong>{{SOCIAL_RATE_PERCENT}}%</strong> for
          {{COUNTRY}} {{JOB}}. This is a simplified model for quick reference only.
        </p>
      </div>
    </section>

    <section class="extra-info">
      <h2>How this calculator works (simplified)</h2>
      <ol>
        <li>You enter your <strong>gross yearly salary</strong> and optional bonus.</li>
        <li>We add them together to get your <strong>total gross income</strong>.</li>
        <li>We subtract an approximate <strong>income tax</strong> and
            <strong>social contributions</strong>.</li>
        <li>The remaining amount is your <strong>estimated net salary</strong>.</li>
      </ol>
      <p>
        Real tax rules usually include progressive brackets, deductions, allowances,
        and other local details. This tool is just a <strong>quick ballpark estimate</strong>
        to help you compare options between jobs, cities, or countries.
      </p>
    </section>

    <footer>
      <p>
        Part of the <strong>Global Salary Calculators</strong> project.
        Browse more calculators on the <a href="../index.html">main index page</a>.
      </p>
    </footer>
  </main>

  <script>
    window.calculatorConfig = {
      "tax_rate": {{TAX_RATE}},
      "social_rate": {{SOCIAL_RATE}},
      "currency": "{{CURRENCY}}",
      "country": "{{COUNTRY}}",
      "job": "{{JOB}}"
    };
  </script>
  <script src="../script.js"></script>
</body>
</html>
"""

SCRIPT_JS = """document.addEventListener("DOMContentLoaded", function () {
  const cfg = window.calculatorConfig || {};
  const form = document.getElementById("salary-form");
  const resultBox = document.getElementById("result");
  const netYearlyEl = document.getElementById("netYearly");
  const netMonthlyEl = document.getElementById("netMonthly");
  const netWeeklyEl = document.getElementById("netWeekly");

  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const grossYearlyInput = document.getElementById("grossYearly");
    const bonusYearlyInput = document.getElementById("bonusYearly");

    const grossYearly = parseFloat(grossYearlyInput.value || "0");
    const bonusYearly = parseFloat(bonusYearlyInput.value || "0");

    if (isNaN(grossYearly) || grossYearly <= 0) {
      alert("Please enter a valid gross yearly salary.");
      return;
    }

    const totalGross = grossYearly + bonusYearly;

    const taxRate = cfg.tax_rate || 0;
    const socialRate = cfg.social_rate || 0;
    const totalDeductionRate = taxRate + socialRate;
    const safeDeductionRate = Math.min(totalDeductionRate, 0.8);

    const netYearly = totalGross * (1 - safeDeductionRate);
    const netMonthly = netYearly / 12;
    const netWeekly = netYearly / 52;

    netYearlyEl.textContent = formatNumber(netYearly);
    netMonthlyEl.textContent = formatNumber(netMonthly);
    netWeeklyEl.textContent = formatNumber(netWeekly);

    resultBox.classList.remove("hidden");
  });

  function formatNumber(num) {
    return num.toLocaleString(undefined, {
      maximumFractionDigits: 2
    });
  }
});
"""

STYLE_CSS = """body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  margin: 0;
  padding: 0;
  background: #f5f5f7;
  color: #222;
}

header {
  background: white;
  padding: 20px;
  border-bottom: 1px solid #ddd;
}

h1 {
  margin: 0 0 8px;
  font-size: 1.6rem;
}

.subtitle {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

main {
  max-width: 900px;
  margin: 20px auto 40px;
  padding: 0 16px;
}

.intro, .calculator, .extra-info, .calculator-list, .country-group {
  background: white;
  margin-bottom: 16px;
  padding: 16px 20px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}

.disclaimer {
  font-size: 0.85rem;
  color: #555;
  margin-top: 10px;
}

.calculator h2,
.extra-info h2 {
  margin-top: 0;
}

form label {
  display: block;
  margin-bottom: 12px;
  font-size: 0.95rem;
}

input[type="number"] {
  width: 100%;
  padding: 8px;
  margin-top: 4px;
  border-radius: 6px;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

button {
  margin-top: 8px;
  padding: 10px 18px;
  border-radius: 999px;
  border: none;
  background: #0070f3;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

button:hover {
  background: #005ad2;
}

.result {
  margin-top: 20px;
  border-top: 1px solid #eee;
  padding-top: 16px;
}

.result-number {
  font-size: 1.05rem;
  margin: 4px 0;
}

.details {
  margin-top: 10px;
  font-size: 0.9rem;
  color: #555;
}

.hidden {
  display: none;
}

footer {
  text-align: center;
  font-size: 0.85rem;
  color: #666;
  margin-top: 20px;
}

.calculator-list ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.calculator-list li {
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.calculator-list a {
  color: #0070f3;
  text-decoration: none;
}

.calculator-list a:hover {
  text-decoration: underline;
}

.country-group h2 {
  margin-top: 0;
}
"""

# ===============================
# 2) 국가 / 직업 데이터 정의
# ===============================

COUNTRIES = [
    {"code": "us", "name": "United States", "currency": "USD", "tax_rate": 0.22, "social_rate": 0.0765},
    {"code": "in", "name": "India", "currency": "INR", "tax_rate": 0.18, "social_rate": 0.03},
    {"code": "id", "name": "Indonesia", "currency": "IDR", "tax_rate": 0.08, "social_rate": 0.04},
    {"code": "br", "name": "Brazil", "currency": "BRL", "tax_rate": 0.17, "social_rate": 0.11},
    {"code": "ng", "name": "Nigeria", "currency": "NGN", "tax_rate": 0.10, "social_rate": 0.02},
    {"code": "mx", "name": "Mexico", "currency": "MXN", "tax_rate": 0.16, "social_rate": 0.06},
    {"code": "ph", "name": "Philippines", "currency": "PHP", "tax_rate": 0.12, "social_rate": 0.08},
    {"code": "bd", "name": "Bangladesh", "currency": "BDT", "tax_rate": 0.10, "social_rate": 0.03},
    {"code": "pk", "name": "Pakistan", "currency": "PKR", "tax_rate": 0.10, "social_rate": 0.03},
    {"code": "vn", "name": "Vietnam", "currency": "VND", "tax_rate": 0.10, "social_rate": 0.08},
    {"code": "uk", "name": "United Kingdom", "currency": "GBP", "tax_rate": 0.20, "social_rate": 0.12},
    {"code": "de", "name": "Germany", "currency": "EUR", "tax_rate": 0.22, "social_rate": 0.195},
    {"code": "fr", "name": "France", "currency": "EUR", "tax_rate": 0.22, "social_rate": 0.16},
    {"code": "ca", "name": "Canada", "currency": "CAD", "tax_rate": 0.20, "social_rate": 0.08},
    {"code": "au", "name": "Australia", "currency": "AUD", "tax_rate": 0.19, "social_rate": 0.095},
    # 추가 국가
    {"code": "jp", "name": "Japan", "currency": "JPY", "tax_rate": 0.20, "social_rate": 0.10},
    {"code": "kr", "name": "South Korea", "currency": "KRW", "tax_rate": 0.18, "social_rate": 0.09},
    {"code": "es", "name": "Spain", "currency": "EUR", "tax_rate": 0.19, "social_rate": 0.065},
    {"code": "it", "name": "Italy", "currency": "EUR", "tax_rate": 0.21, "social_rate": 0.10},
    {"code": "ru", "name": "Russia", "currency": "RUB", "tax_rate": 0.13, "social_rate": 0.30},
    {"code": "za", "name": "South Africa", "currency": "ZAR", "tax_rate": 0.18, "social_rate": 0.05},
    {"code": "ar", "name": "Argentina", "currency": "ARS", "tax_rate": 0.20, "social_rate": 0.06},
    {"code": "co", "name": "Colombia", "currency": "COP", "tax_rate": 0.18, "social_rate": 0.04},
    {"code": "eg", "name": "Egypt", "currency": "EGP", "tax_rate": 0.15, "social_rate": 0.05},
    {"code": "th", "name": "Thailand", "currency": "THB", "tax_rate": 0.10, "social_rate": 0.05},
    {"code": "my", "name": "Malaysia", "currency": "MYR", "tax_rate": 0.12, "social_rate": 0.05},
    {"code": "tr", "name": "Turkey", "currency": "TRY", "tax_rate": 0.15, "social_rate": 0.10},
    {"code": "sa", "name": "Saudi Arabia", "currency": "SAR", "tax_rate": 0.00, "social_rate": 0.10},
    {"code": "ae", "name": "United Arab Emirates", "currency": "AED", "tax_rate": 0.00, "social_rate": 0.05},
]

JOBS = [
    "Software Engineer",
    "Web Developer",
    "Mobile App Developer",
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "System Administrator",
    "Data Scientist",
    "Data Analyst",
    "Machine Learning Engineer",
    "AI Engineer",
    "Product Manager",
    "Project Manager",
    "Business Analyst",
    "Scrum Master",
    "Accountant",
    "Auditor",
    "Financial Analyst",
    "Investment Banker",
    "Bank Teller",
    "Loan Officer",
    "Insurance Agent",
    "Real Estate Agent",
    "Lawyer",
    "Paralegal",
    "Judge Assistant",
    "Teacher",
    "High School Teacher",
    "Primary School Teacher",
    "University Professor",
    "Private Tutor",
    "Nurse",
    "Doctor",
    "Dentist",
    "Pharmacist",
    "Physiotherapist",
    "Psychologist",
    "Social Worker",
    "Police Officer",
    "Firefighter",
    "Soldier",
    "Security Guard",
    "Civil Engineer",
    "Mechanical Engineer",
    "Electrical Engineer",
    "Chemical Engineer",
    "Industrial Engineer",
    "Architect",
    "Interior Designer",
    "Construction Worker",
    "Plumber",
    "Electrician",
    "Carpenter",
    "Factory Worker",
    "Machine Operator",
    "Warehouse Worker",
    "Logistics Coordinator",
    "Truck Driver",
    "Taxi Driver",
    "Delivery Driver",
    "Uber Driver",
    "Bus Driver",
    "Call Center Agent",
    "Customer Support Representative",
    "Sales Representative",
    "Sales Manager",
    "Marketing Manager",
    "Digital Marketer",
    "SEO Specialist",
    "Content Writer",
    "Copywriter",
    "Journalist",
    "Graphic Designer",
    "UI UX Designer",
    "Photographer",
    "Videographer",
    "Chef",
    "Cook",
    "Waiter",
    "Bartender",
    "Barista",
    "Hotel Receptionist",
    "Housekeeper",
    "Office Administrator",
    "Receptionist",
    "Data Entry Clerk",
    "Human Resources Manager",
    "Recruiter",
    "Fitness Trainer",
    "Personal Trainer",
    "Hairdresser",
    "Beauty Therapist",
    "Flight Attendant",
    "Pilot",
    "Farmer",
    "Agricultural Worker",
    "Miner",
    "Software Tester",
    "QA Engineer",
    "Game Developer",
    "Youtuber",
    "Content Creator",
]

def slugify(text: str) -> str:
    return (
        text.lower()
        .replace("&", "and")
        .replace("/", "-")
        .replace(" ", "-")
        .replace(",", "")
        .replace(".", "")
    )

# ===============================
# 3) 파일 생성 보조 함수
# ===============================

def ensure_file(path: str, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ===============================
# 4) 메인 생성 로직
# ===============================

def main():
    # 1) 공통 파일 생성
    ensure_file("template.html", TEMPLATE_HTML)
    ensure_file("script.js", SCRIPT_JS)
    ensure_file("style.css", STYLE_CSS)

    adsense_injected_template = TEMPLATE_HTML.replace("{{ADSENSE_SNIPPET}}", ADSENSE_SNIPPET.strip())

    # 2) docs 폴더
    output_dir = "docs"
    os.makedirs(output_dir, exist_ok=True)

    calculators_meta = []

    # 3) 국가 × 직업 조합으로 페이지 생성
    for country in COUNTRIES:
        for job in JOBS:
            slug = f"{country['code']}-{slugify(job)}-salary-calculator"
            title = f"{country['name']} {job} Net Salary Calculator (Simplified Take-Home Pay)"
            description = (
                f"Estimate your net salary (take-home pay) as a {job} in {country['name']}."
                f" Enter your gross yearly salary to see an approximate yearly, monthly,"
                f" and weekly net income after tax and social contributions."
            )

            tax_rate = country["tax_rate"]
            social_rate = country["social_rate"]
            tax_rate_percent = round(tax_rate * 100, 1)
            social_rate_percent = round(social_rate * 100, 1)

            page = adsense_injected_template
            page = page.replace("{{TITLE}}", title)
            page = page.replace("{{DESCRIPTION}}", description)
            page = page.replace("{{COUNTRY}}", country["name"])
            page = page.replace("{{JOB}}", job)
            page = page.replace("{{CURRENCY}}", country["currency"])
            page = page.replace("{{TAX_RATE_PERCENT}}", str(tax_rate_percent))
            page = page.replace("{{SOCIAL_RATE_PERCENT}}", str(social_rate_percent))
            page = page.replace("{{TAX_RATE}}", str(tax_rate))
            page = page.replace("{{SOCIAL_RATE}}", str(social_rate))

            output_path = os.path.join(output_dir, f"{slug}.html")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(page)

            calculators_meta.append(
                {
                    "slug": slug,
                    "title": title,
                    "country": country["name"],
                    "job": job,
                    "currency": country["currency"],
                    "country_code": country["code"],
                }
            )

    print(f"Generated {len(calculators_meta)} calculator pages.")

    # 4) index.html (여기도 애드센스 삽입)
    base_index_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Global Salary Calculators (Net Salary, Take-Home Pay)</title>
  <meta name="description" content="A large collection of simplified net salary calculators for popular jobs in high-population countries. Estimate your take-home pay quickly.">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {{ADSENSE_SNIPPET}}
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <header>
    <h1>Global Salary Calculators</h1>
    <p class="subtitle">Net salary &amp; take-home pay estimators for popular jobs in high-population countries.</p>
  </header>
  <main>
    <section class="intro">
      <p>This site provides <strong>simplified</strong> net salary calculators.
         Choose your country and job below to estimate your take-home pay (yearly, monthly, weekly).</p>
      <p class="disclaimer">
        All calculators use rough average rates. Real tax systems are more complex and change over time.
        Use these tools for quick comparison only.</p>
    </section>
    <section class="calculator-list">
"""
    base_index_html = base_index_html.replace("{{ADSENSE_SNIPPET}}", ADSENSE_SNIPPET.strip())

    calculators_meta.sort(key=lambda x: (x["country"], x["job"]))

    index_html = base_index_html
    current_country = None

    for meta in calculators_meta:
        if meta["country"] != current_country:
            if current_country is not None:
                index_html += "      </ul>\n    </section>\n"
            current_country = meta["country"]
            index_html += f'    <section class="country-group">\n'
            index_html += f'      <h2>{current_country}</h2>\n'
            index_html += "      <ul>\n"

        index_html += (
            f'        <li><a href="{meta["slug"]}.html">'
            f'{meta["title"]}</a> — {meta["job"]} · {meta["currency"]}</li>\n'
        )

    if current_country is not None:
        index_html += "      </ul>\n    </section>\n"

    index_html += """    <footer>
      <p>Generated automatically by a single Python script. No manual page creation needed.</p>
    </footer>
  </main>
</body>
</html>
"""

    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    print("Generated docs/index.html")


if __name__ == "__main__":
    main()
