// Tab switching
document.querySelectorAll(".calc-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
        const target = tab.dataset.target;
        document.querySelectorAll(".calc-tab").forEach((t) => t.classList.remove("active"));
        document.querySelectorAll(".calc-panel").forEach((p) => p.classList.remove("active"));
        tab.classList.add("active");
        document.getElementById(`panel-${target}`).classList.add("active");
    });
});

// Currency formatter
const fmt = (n) =>
    new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(n || 0);

// ---- Loan ----
const loanInputs = ["loan-amount", "loan-rate", "loan-term"].map((id) => document.getElementById(id));
function calcLoan() {
    const [P, ratePct, years] = loanInputs.map((el) => parseFloat(el.value) || 0);
    const r = ratePct / 100 / 12;
    const n = years * 12;
    let monthly = 0;
    if (r === 0) monthly = P / n;
    else monthly = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
    const total = monthly * n;
    const interest = total - P;
    document.getElementById("loan-monthly").textContent = isFinite(monthly) ? fmt(monthly) : "—";
    document.getElementById("loan-total").textContent = isFinite(total) ? fmt(total) : "—";
    document.getElementById("loan-interest").textContent = isFinite(interest) ? fmt(interest) : "—";
}
loanInputs.forEach((el) => el.addEventListener("input", calcLoan));
calcLoan();

// ---- Tip ----
const tipInputs = ["tip-bill", "tip-percent", "tip-people"].map((id) => document.getElementById(id));
function calcTip() {
    const [bill, pct, people] = tipInputs.map((el) => parseFloat(el.value) || 0);
    const tip = bill * (pct / 100);
    const total = bill + tip;
    const each = people > 0 ? total / people : 0;
    document.getElementById("tip-amount").textContent = fmt(tip);
    document.getElementById("tip-total").textContent = fmt(total);
    document.getElementById("tip-each").textContent = fmt(each);
}
tipInputs.forEach((el) => el.addEventListener("input", calcTip));
calcTip();

// ---- BMI ----
const bmiInputs = ["bmi-height", "bmi-weight"].map((id) => document.getElementById(id));
function calcBMI() {
    const [h, w] = bmiInputs.map((el) => parseFloat(el.value) || 0);
    const m = h / 100;
    const bmi = m > 0 ? w / (m * m) : 0;
    let cat = "—";
    if (bmi > 0) {
        if (bmi < 18.5) cat = "Underweight";
        else if (bmi < 25) cat = "Normal";
        else if (bmi < 30) cat = "Overweight";
        else cat = "Obese";
    }
    document.getElementById("bmi-value").textContent = bmi ? bmi.toFixed(1) : "—";
    document.getElementById("bmi-category").textContent = cat;
}
bmiInputs.forEach((el) => el.addEventListener("input", calcBMI));
calcBMI();
