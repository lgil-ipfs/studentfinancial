// Helper function to format currency
const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-CA', { style: 'currency', currency: 'CAD' }).format(amount);
};

// 1. Student Loan Repayment
const calcLoan = () => {
    const p = parseFloat(document.getElementById('loan-amount').value) || 0;
    const r = (parseFloat(document.getElementById('loan-rate').value) || 0) / 100 / 12;
    const n = parseFloat(document.getElementById('loan-term').value) || 1;

    let monthlyPayment = 0;
    if (r === 0) {
        monthlyPayment = p / n;
    } else {
        monthlyPayment = p * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
    }

    const totalCost = monthlyPayment * n;
    const totalInterest = totalCost - p;

    document.getElementById('loan-payment-res').innerText = formatCurrency(monthlyPayment);
    document.getElementById('loan-interest-res').innerText = formatCurrency(totalInterest);
    document.getElementById('loan-total-res').innerText = formatCurrency(totalCost);
};

// 3. Budget Surplus/Deficit
let budgetChart;
const calcBudget = () => {
    const income = parseFloat(document.getElementById('budget-income').value) || 0;
    const expenses = parseFloat(document.getElementById('budget-expenses').value) || 0;
    const diff = income - expenses;

    document.getElementById('budget-diff').innerText = formatCurrency(Math.abs(diff));
    document.getElementById('budget-status').innerText = diff >= 0 ? "Surplus" : "Deficit";
    document.getElementById('budget-status').style.color = diff >= 0 ? "var(--primary)" : "var(--accent)";

    const ctx = document.getElementById('budgetChart').getContext('2d');
    if (budgetChart) budgetChart.destroy();
    budgetChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Income', 'Expenses'],
            datasets: [{
                data: [income, expenses],
                backgroundColor: ['#1A6B5A', '#E8614A'],
                borderWidth: 0
            }]
        },
        options: {
            cutout: '70%',
            plugins: { legend: { display: false } }
        }
    });
};

// 4. Net Worth Tracker
let nwChart;
const calcNetWorth = () => {
    const assets = parseFloat(document.getElementById('assets-val').value) || 0;
    const liabilities = parseFloat(document.getElementById('liabilities-val').value) || 0;
    const nw = assets - liabilities;

    document.getElementById('networth-res').innerText = formatCurrency(nw);
    document.getElementById('networth-res').style.color = nw >= 0 ? "var(--primary)" : "var(--accent)";

    const ctx = document.getElementById('nwChart').getContext('2d');
    if (nwChart) nwChart.destroy();
    nwChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Assets', 'Liabilities'],
            datasets: [{
                data: [assets, liabilities],
                backgroundColor: ['#1A6B5A', '#E8614A'],
                borderRadius: 8
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
};

// 5. Credit Card Danger
const calcCC = () => {
    const balance = parseFloat(document.getElementById('cc-balance').value) || 0;
    const rate = (parseFloat(document.getElementById('cc-rate').value) || 0) / 100 / 12;
    const minPayRate = 0.03; // Approx 3%
    
    let currentBalance = balance;
    let totalInterest = 0;
    let months = 0;

    // Simplified simulation
    while (currentBalance > 1 && months < 600) { // Max 50 years to avoid infinite
        const interest = currentBalance * rate;
        let payment = currentBalance * minPayRate;
        if (payment < 10) payment = 10; // Assume min payment of at least $10
        
        totalInterest += interest;
        currentBalance = currentBalance + interest - payment;
        months++;
    }

    document.getElementById('cc-years').innerText = (months / 12).toFixed(1) + " Years";
    document.getElementById('cc-interest').innerText = formatCurrency(totalInterest);
};

// 6. TFSA Growth
let tfsaChart;
const calcTFSA = () => {
    const monthly = parseFloat(document.getElementById('tfsa-monthly').value) || 0;
    const rate = (parseFloat(document.getElementById('tfsa-return').value) || 0) / 100 / 12;
    const years = parseFloat(document.getElementById('tfsa-years').value) || 0;
    const months = years * 12;

    let balance = 0;
    const history = [];
    const labels = [];

    for (let i = 1; i <= months; i++) {
        balance = (balance + monthly) * (1 + rate);
        if (i % 12 === 0) {
            history.push(balance);
            labels.push(`Year ${i/12}`);
        }
    }

    document.getElementById('tfsa-res').innerText = formatCurrency(balance);

    const ctx = document.getElementById('tfsaChart').getContext('2d');
    if (tfsaChart) tfsaChart.destroy();
    tfsaChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Projected TFSA Value',
                data: history,
                borderColor: '#1A6B5A',
                backgroundColor: 'rgba(26, 107, 90, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            plugins: { legend: { display: false } }
        }
    });
};

// Event Listeners
const inputs = document.querySelectorAll('input');
inputs.forEach(input => {
    input.addEventListener('input', () => {
        calcLoan();
        calcBudget();
        calcNetWorth();
        calcCC();
        calcTFSA();
    });
});

// Initial Calc
window.onload = () => {
    calcLoan();
    calcBudget();
    calcNetWorth();
    calcCC();
    calcTFSA();
};
