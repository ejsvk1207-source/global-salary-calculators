document.addEventListener("DOMContentLoaded", function () {
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
