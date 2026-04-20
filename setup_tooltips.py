import os
import re
import json

terms_raw = """
**OSAP (Ontario Student Assistance Program)**
A government program that provides financial aid — including grants and loans — to eligible Ontario post-secondary students. Grants don't need to be repaid; loans do. Your OSAP funding is based on your financial need, tuition, and living costs.
https://www.ontario.ca/page/osap-ontario-student-assistance-program

**NSLSC (National Student Loans Service Centre)**
The federal government body that manages your Canada Student Loan after you leave school. This is where you make your loan payments, apply for repayment assistance, and manage your repayment schedule. You pay the NSLSC — not OSAP directly.
https://www.csnpe-nslsc.canada.ca/en/home

**Canada Student Loan**
The federal portion of your student loan, administered by the federal government and managed through the NSLSC. As of April 1, 2023, the federal government eliminated interest on Canada Student Loans entirely — so no interest accrues on this portion.
https://www.canada.ca/en/services/benefits/education/student-aid/grants-loans.html

**Grace Period**
A six-month window after you graduate or stop full-time studies before you must begin repaying your student loans. During this period, no payments are required. Ontario student loans may accrue interest during this time — federal loans do not (as of 2023).
https://www.ontario.ca/page/pay-back-osap

**RAP (Repayment Assistance Plan)**
A federal program that reduces or eliminates your monthly student loan payments based on your income and family size. If approved, the government covers any interest your reduced payment doesn't cover. You must reapply every six months.
https://www.canada.ca/en/services/benefits/education/student-aid/grants-loans/repay/assistance/rap.html

**Loan Default**
When you stop making required loan payments for a prolonged period — for OSAP, this is 270 days without payment. Defaulting can damage your credit score, result in collection action, and block you from future government student aid.
https://www.ontario.ca/page/pay-back-osap

**Master Student Financial Assistance Agreement (MSFAA)**
The legal contract you sign when you first receive OSAP funding. It outlines the terms of your loan — including interest rates, repayment obligations, and your rights. Once signed, it covers all future OSAP loans during your studies.
https://www.ontario.ca/page/osap-master-student-financial-assistance-agreement

**Grant vs. Loan**
A grant is money you receive that does not need to be repaid — it is essentially free financial support. A loan must be repaid, usually with interest. Your OSAP package may include both. Always spend grants before dipping into loan funds.
https://www.ontario.ca/page/osap-grants-and-loans

**Loan Amortization Period**
The total length of time you have to repay your student loan. For OSAP, the standard repayment schedule is 9.5 years. You can extend this up to 14.5 years to lower your monthly payments, though you will pay more interest over time.
https://www.ontario.ca/page/pay-back-osap

**Student Loan Rehabilitation**
A program that allows you to bring a defaulted Ontario student loan back into good standing through a series of agreed payments. Once rehabilitated, you regain access to OSAP funding and your credit history begins to recover.
https://osap.gov.on.ca/OSAPPortal/en/A-ZListofAid/POCONT1_102278

**Credit Score**
A three-digit number (300–900 in Canada) that reflects how reliably you manage borrowed money. Lenders use it to decide whether to approve you for loans, credit cards, or even rental housing. The higher your score, the lower the risk you appear to be.
https://www.canada.ca/en/financial-consumer-agency/services/credit-reports-score/credit-report-score-basics.html

**Credit Report**
A detailed record of your borrowing history — every credit card, loan, and payment — compiled by credit bureaus (Equifax and TransUnion). Landlords, banks, and employers may review it. You can request yours for free.
https://www.canada.ca/en/financial-consumer-agency/services/credit-reports-score/order-credit-report.html

**Credit Bureau**
Private companies — Equifax and TransUnion are Canada's two main ones — that collect and store information about how Canadians use credit. They calculate your credit score and sell credit reports to lenders who request them.
https://www.canada.ca/en/financial-consumer-agency/services/credit-reports-score/credit-report-score-basics.html

**Hard Hit (Hard Inquiry)**
A formal check of your credit report by a lender when you apply for credit — a loan, credit card, or mortgage. Hard hits temporarily lower your credit score slightly and remain on your report for up to six years (TransUnion) or three years (Equifax).
https://www.canada.ca/en/financial-consumer-agency/services/credit-reports-score/improve-credit-score.html

**Soft Hit (Soft Inquiry)**
A credit check that does not affect your credit score — such as checking your own credit report or a background check by an employer. Soft hits are not visible to lenders and have no negative impact.
https://www.canada.ca/en/financial-consumer-agency/services/credit-reports-score/improve-credit-score.html

**Credit Utilization**
The percentage of your available credit that you are currently using. For example, if your credit limit is $5,000 and you have spent $2,000, your utilization is 40%. Staying below 30% is recommended for a healthy credit score.
https://www.canada.ca/en/financial-consumer-agency/services/credit-reports-score/improve-credit-score.html

**Credit Limit**
The maximum amount a lender allows you to borrow on a credit card or line of credit. Going over this limit can result in fees and a lower credit score. Lenders set this limit based on your income, credit history, and other factors.
https://www.canada.ca/en/financial-consumer-agency/services/credit-cards/credit-card-basics.html

**Consumer Proposal**
A formal legal arrangement, set up through a licensed insolvency trustee, where you agree to pay back a portion of what you owe. It is an alternative to bankruptcy and stays on your credit report for three years after you pay it off, or six years from signing — whichever is sooner.
https://www.canada.ca/en/financial-consumer-agency/services/credit-reports-score/information-credit-report.html

**TFSA (Tax-Free Savings Account)**
A registered account available to Canadians 18 and older that lets you save and invest money — and pay zero tax on any interest or growth, even when you withdraw. It is flexible: use it for emergencies, a trip, a car, or retirement. The 2025 annual contribution limit is $7,000.
https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/tax-free-savings-account.html

**RRSP (Registered Retirement Savings Plan)**
A registered account designed for retirement saving. Contributions reduce your taxable income now, and your money grows tax-free inside the account. You pay tax when you withdraw in retirement — ideally when your income and tax rate are lower.
https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/rrsps-related-plans/registered-retirement-savings-plan-rrsp.html

**FHSA (First Home Savings Account)**
A registered account introduced in 2023 for first-time home buyers. You can contribute up to $8,000 per year (lifetime max $40,000), get a tax deduction on contributions, and withdraw tax-free when buying your first home.
https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/first-home-savings-account.html

**RESP (Registered Education Savings Plan)**
A savings account designed for a child's post-secondary education. The government adds 20% on the first $2,500 contributed each year through the Canada Education Savings Grant. Earnings grow tax-sheltered until withdrawn.
https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/registered-education-savings-plans-resps.html

**Compound Interest**
Interest calculated on both your original deposit and the interest you have already earned. Over time, this creates a snowball effect — your money grows faster the longer it sits. The same effect works against you on debt: unpaid interest gets added to your balance and then earns more interest.
https://www.canada.ca/en/financial-consumer-agency/services/savings-investments/compound-interest.html

**GIC (Guaranteed Investment Certificate)**
A low-risk savings product offered by banks and credit unions where you deposit money for a fixed term (e.g., one year) at a guaranteed interest rate. Your principal is protected. GICs can be held inside a TFSA or RRSP.
https://www.canada.ca/en/financial-consumer-agency/services/savings-investments/gics.html

**Contribution Room**
The maximum amount you are allowed to contribute to your TFSA or RRSP in a given year. Unused TFSA room carries forward every year. RRSP room is based on your prior year's earned income. Exceeding your limit triggers a penalty tax.
https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/tax-free-savings-account/contributions.html

**Emergency Fund**
A savings buffer — typically three to six months of living expenses — set aside for unexpected costs like a job loss, medical expense, or car repair. Financial advisors recommend keeping this in a liquid, low-risk account such as a high-interest savings account or TFSA.
https://www.canada.ca/en/financial-consumer-agency/services/savings-investments/emergency-fund.html

**T4 Slip**
A tax form issued by your employer that shows how much you earned and how much tax was deducted from your pay in a calendar year. You receive it by the end of February and need it to file your income tax return.
https://www.canada.ca/en/revenue-agency/services/forms-publications/forms/t4.html

**T2202 (Tuition and Enrolment Certificate)**
A tax slip issued by your post-secondary institution that certifies your eligible tuition fees. You can use it to claim the tuition tax credit, which reduces the amount of federal and provincial income tax you owe — or carry it forward to future years.
https://www.canada.ca/en/revenue-agency/services/forms-publications/forms/t2202.html

**CRA (Canada Revenue Agency)**
The federal government agency responsible for collecting taxes and administering tax laws and benefit programs in Canada. This is where you file your annual tax return. Creating a free CRA My Account gives you access to your tax slips, refunds, benefit payments, and contribution room.
https://www.canada.ca/en/revenue-agency.html

**Marginal Tax Rate**
The percentage of tax you pay on each additional dollar earned — not on your entire income. Canada uses progressive tax brackets, meaning you pay a higher rate only on income above certain thresholds. Most students are in the lowest brackets.
https://www.canada.ca/en/revenue-agency/services/tax/individuals/frequently-asked-questions-individuals/canadian-income-tax-rates-individuals-current-previous-years.html

**Tax Refund**
Money returned to you by the CRA after you file your tax return, if more tax was withheld from your paycheques than you actually owed for the year. Filing your return — even if you earned very little — is important because it unlocks benefit payments like the GST/HST credit.
https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return.html

**GST/HST Credit**
A tax-free quarterly payment from the federal government to help individuals and families with low or moderate incomes offset the cost of GST or HST. Students who file a tax return — even with zero income — are often eligible.
https://www.canada.ca/en/revenue-agency/services/child-family-benefits/gsthstc-apply.html

**Tuition Tax Credit**
A non-refundable federal tax credit based on your eligible tuition fees shown on your T2202 slip. It reduces the amount of federal tax you owe. If you have no tax owing this year, you can transfer unused credits to a parent or carry them forward to a future year.
https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/deductions-credits-expenses/line-32300-your-tuition-education-textbook-amounts.html

**Interest Rate**
The cost of borrowing money, expressed as a percentage of the amount owed per year. A 19.99% credit card interest rate means you will pay roughly $20 per year for every $100 of unpaid balance. The higher the rate, the more expensive carrying debt becomes.
https://www.canada.ca/en/financial-consumer-agency/services/interest-rates.html

**Minimum Payment**
The smallest amount you can pay on your credit card or line of credit each month to avoid a penalty. Paying only the minimum is extremely costly: with a high interest rate, most of your payment goes to interest — not reducing what you owe. It can take years to pay off even small balances.
https://www.canada.ca/en/financial-consumer-agency/services/credit-cards/credit-card-basics.html

**Debt Consolidation**
Combining multiple debts — credit card balances, student loans, lines of credit — into a single loan or payment, often at a lower interest rate. It can simplify your finances and reduce overall interest, but does not reduce the total amount owed.
https://www.canada.ca/en/financial-consumer-agency/services/debt/debt-consolidation.html

**Line of Credit (LOC)**
A flexible borrowing arrangement where a lender approves a maximum limit you can draw from as needed. You only pay interest on what you have actually borrowed. Interest rates are typically lower than credit cards. Student lines of credit are common for professional program students.
https://www.canada.ca/en/financial-consumer-agency/services/loans/line-of-credit.html

**Payday Loan**
A short-term, high-cost loan typically due on your next payday. While they may seem convenient, they carry extremely high interest rates — sometimes equivalent to over 400% annually. They can create a debt cycle that is very difficult to escape. Avoid if at all possible.
https://www.canada.ca/en/financial-consumer-agency/services/loans/payday-loans.html

**Bankruptcy**
A legal process administered by a licensed insolvency trustee that allows individuals to be relieved of most unsecured debts when they can no longer repay them. It has serious long-term consequences for your credit. Student loans are only discharged in bankruptcy after seven years out of school.
https://www.canada.ca/en/financial-consumer-agency/services/debt/bankruptcy.html

**Debt Management Plan**
An informal arrangement negotiated by a non-profit credit counsellor on your behalf, where creditors agree to reduced or frozen interest rates so you can pay off what you owe through one affordable monthly payment. It stays on your credit report for two years after you complete it.
https://www.canada.ca/en/financial-consumer-agency/services/debt/debt-management-plans.html

**Overdraft**
When your bank account goes below $0 because a payment exceeded your balance. Banks may cover the shortfall through overdraft protection but charge a fee and/or interest. Repeated overdrafts are expensive and signal cash flow problems worth addressing.
https://www.canada.ca/en/financial-consumer-agency/services/banking/overdraft-protection.html

**Chequing Account**
An everyday bank account used for spending — receiving your paycheque, paying bills, and making purchases. It typically earns little to no interest. Transactions are processed quickly and balances are accessible at any time.
https://www.canada.ca/en/financial-consumer-agency/services/banking/bank-accounts.html

**Savings Account**
A bank account that earns interest on your balance, intended for money you do not need to access daily. High-interest savings accounts offer better rates. A savings account at a bank is different from a TFSA — the latter provides tax advantages.
https://www.canada.ca/en/financial-consumer-agency/services/banking/bank-accounts.html

**NSF Fee (Non-Sufficient Funds)**
A fee charged by your bank when a payment bounces because your account does not have enough money to cover it. As of 2024, federally regulated banks must cap NSF fees at $10 per transaction.
https://www.canada.ca/en/financial-consumer-agency/news/2024/06/the-government-of-canada-caps-non-sufficient-funds-fees.html

**CDIC (Canada Deposit Insurance Corporation)**
A federal Crown corporation that insures eligible deposits at member banks up to $100,000 per depositor category. If your bank fails, your deposits up to this limit are protected. Most major Canadian banks and credit unions are CDIC members.
https://www.cdic.ca/en/

**Pre-Authorized Debit (PAD)**
An arrangement where you give a company permission to automatically withdraw money from your bank account on set dates — for example, rent, subscriptions, or loan payments. PADs are convenient but require you to maintain sufficient funds on withdrawal dates.
https://www.canada.ca/en/financial-consumer-agency/services/banking/pre-authorized-debit.html

**EFT / Interac e-Transfer**
An Electronic Funds Transfer moves money between bank accounts electronically. Interac e-Transfer is Canada's most common form — fast, simple, and widely used for splitting bills, paying rent, or sending money to family.
https://www.canada.ca/en/financial-consumer-agency/services/banking/electronic-banking.html

**Social Insurance Number (SIN)**
A nine-digit number issued by the federal government that is required to work in Canada, file taxes, and open registered accounts like TFSAs and RRSPs. Treat your SIN like a password — sharing it unnecessarily increases your risk of identity theft.
https://www.canada.ca/en/employment-social-development/services/sin.html

**Direct Deposit**
An arrangement where funds — such as your paycheque, tax refund, or government benefits — are deposited automatically into your bank account. Setting up direct deposit with CRA My Account ensures you receive refunds and benefit payments faster.
https://www.canada.ca/en/revenue-agency/services/about-canada-revenue-agency-cra/direct-deposit.html
"""

blocks = [b.strip() for b in terms_raw.split("\n\n") if b.strip()]
parsed_terms = []

for block in blocks:
    lines = block.split("\n")
    if len(lines) >= 3 and lines[0].startswith("**"):
        title = lines[0].replace("**", "").strip()
        definition = lines[1].strip()
        link = lines[2].strip()
        
        # Check if title has alternate form in parentheses
        if "(" in title and title.endswith(")"):
            main_term = title.split("(")[0].strip()
            alt_term = title.split("(")[1].replace(")", "").strip()
            parsed_terms.append({"term": main_term, "definition": definition, "link": link})
            parsed_terms.append({"term": alt_term, "definition": definition, "link": link})
        elif " vs. " in title:
            parsed_terms.append({"term": title.split("vs.")[0].strip(), "definition": definition, "link": link})
            parsed_terms.append({"term": title.split("vs.")[1].strip(), "definition": definition, "link": link})
            parsed_terms.append({"term": title, "definition": definition, "link": link})
        elif " / " in title:
            parsed_terms.append({"term": title.split(" / ")[0].strip(), "definition": definition, "link": link})
            parsed_terms.append({"term": title.split(" / ")[1].strip(), "definition": definition, "link": link})
        else:
            parsed_terms.append({"term": title, "definition": definition, "link": link})

# Sort by length descending to match longest terms first (e.g. "Credit Score" before "Credit")
parsed_terms.sort(key=lambda x: len(x["term"]), reverse=True)

# Generate JS
js_content = """
// Auto-generated term popup script
document.addEventListener('DOMContentLoaded', () => {
    const financialTerms = """ + json.dumps(parsed_terms, indent=4) + """;
    
    // Escape regex characters
    const escapeRegExp = (string) => string.replace(/[.*+?^${}()|[\]\\\\]/g, '\\\\$&');
    
    // Sort terms by length to match the longest terms first
    financialTerms.sort((a, b) => b.term.length - a.term.length);
    
    // Create regex pattern for all terms
    const termsPattern = financialTerms.map(t => escapeRegExp(t.term)).join('|');
    if (!termsPattern) return;
    const regex = new RegExp(`\\\\b(${termsPattern})\\\\b`, 'gi');
    
    // Create popup element
    const popup = document.createElement('div');
    popup.className = 'financial-term-popup';
    document.body.appendChild(popup);
    
    // Add close button functionality for mobile
    popup.addEventListener('click', (e) => {
        if(e.target.closest('.close-btn')) {
            popup.classList.remove('active');
        }
    });

    let activeTermEl = null;

    const showPopup = (el, termData) => {
        popup.innerHTML = `
            <div class="popup-header">
                <strong>${termData.term}</strong>
                <button class="close-btn" aria-label="Close">&times;</button>
            </div>
            <div class="popup-body">${termData.definition}</div>
            <a href="${termData.link}" target="_blank" class="popup-link">Learn More &rarr;</a>
        `;
        
        const rect = el.getBoundingClientRect();
        
        // Calculate position
        let top = rect.bottom + window.scrollY + 10;
        let left = rect.left + window.scrollX;
        
        popup.style.display = 'block';
        
        // Adjust if it goes off screen
        const popupRect = popup.getBoundingClientRect();
        if (left + popupRect.width > window.innerWidth - 20) {
            left = window.innerWidth - popupRect.width - 20;
        }
        
        popup.style.top = top + 'px';
        popup.style.left = left + 'px';
        
        // Use a slight timeout for CSS transition
        setTimeout(() => popup.classList.add('active'), 10);
        activeTermEl = el;
    };

    const hidePopup = () => {
        popup.classList.remove('active');
        setTimeout(() => {
            if(!popup.classList.contains('active')) {
                popup.style.display = 'none';
            }
        }, 300);
        activeTermEl = null;
    };

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.financial-term') && !e.target.closest('.financial-term-popup')) {
            hidePopup();
        }
    });

    // We only process specific elements to avoid breaking the DOM
    const parseNodes = document.querySelectorAll('p, li, dd, span');
    
    parseNodes.forEach(node => {
        // Skip links, headings, or already processed
        if (node.closest('a') || node.closest('h1, h2, h3, h4') || node.closest('.financial-term')) return;
        
        const treeWalker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, null, false);
        const textNodes = [];
        let textNode;
        while (textNode = treeWalker.nextNode()) {
            if (!textNode.parentNode.closest('a') && regex.test(textNode.nodeValue)) {
                textNodes.push(textNode);
            }
            regex.lastIndex = 0; // reset
        }
        
        textNodes.forEach(tNode => {
            const frag = document.createDocumentFragment();
            let lastIdx = 0;
            const text = tNode.nodeValue;
            let match;
            regex.lastIndex = 0;
            
            while ((match = regex.exec(text)) !== null) {
                // Add text before match
                if (match.index > lastIdx) {
                    frag.appendChild(document.createTextNode(text.substring(lastIdx, match.index)));
                }
                
                // Add term span
                const termMatch = match[0];
                const termObj = financialTerms.find(t => t.term.toLowerCase() === termMatch.toLowerCase());
                
                if (termObj) {
                    const span = document.createElement('span');
                    span.className = 'financial-term';
                    span.textContent = termMatch;
                    span.setAttribute('data-term', termObj.term);
                    
                    // Event listeners
                    span.addEventListener('mouseenter', () => showPopup(span, termObj));
                    span.addEventListener('mouseleave', () => { setTimeout(() => { if (!popup.matches(':hover')) hidePopup(); }, 100); });
                    span.addEventListener('click', (e) => { e.preventDefault(); showPopup(span, termObj); });
                    
                    frag.appendChild(span);
                } else {
                    frag.appendChild(document.createTextNode(termMatch));
                }
                
                lastIdx = regex.lastIndex;
            }
            
            if (lastIdx < text.length) {
                frag.appendChild(document.createTextNode(text.substring(lastIdx)));
            }
            
            tNode.parentNode.replaceChild(frag, tNode);
        });
    });
    
    // Popup hover state to keep it open
    popup.addEventListener('mouseenter', () => popup.classList.add('active'));
    popup.addEventListener('mouseleave', hidePopup);
});
"""

with open("js/term-popups.js", "w") as f:
    f.write(js_content)

# Update HTML files
html_files = [f for f in os.listdir(".") if f.endswith(".html")]
for html_file in html_files:
    with open(html_file, "r") as f:
        content = f.read()
    
    if '<script src="js/term-popups.js"></script>' not in content:
        content = content.replace("</body>", '    <script src="js/term-popups.js"></script>\n</body>')
        with open(html_file, "w") as f:
            f.write(content)

# Update CSS
css_path = "css/styles.css"
popup_css = """
/* Financial Term Highlights */
.financial-term {
    text-decoration: underline;
    text-decoration-style: dotted;
    text-decoration-color: var(--primary);
    text-underline-offset: 4px;
    cursor: help;
    color: var(--primary);
    font-weight: 600;
    transition: all 0.2s;
}

.financial-term:hover {
    background-color: rgba(26, 107, 90, 0.1);
    border-radius: 4px;
}

/* Financial Term Popup Wrapper */
.financial-term-popup {
    position: absolute;
    z-index: 9999;
    background: var(--white);
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    width: 320px;
    max-width: 90vw;
    padding: 20px;
    display: none;
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.3s ease, transform 0.3s ease;
    border: 1px solid rgba(26, 107, 90, 0.1);
    font-size: 0.95rem;
}

.financial-term-popup.active {
    opacity: 1;
    transform: translateY(0);
}

.financial-term-popup .popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    padding-bottom: 8px;
}

.financial-term-popup .popup-header strong {
    color: var(--primary);
    font-size: 1.1rem;
    font-family: 'Fraunces', serif;
}

.financial-term-popup .close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    line-height: 1;
    cursor: pointer;
    color: var(--muted);
}

.financial-term-popup .popup-body {
    color: var(--text);
    margin-bottom: 16px;
    line-height: 1.5;
}

.financial-term-popup .popup-link {
    display: inline-block;
    color: var(--secondary);
    font-weight: 700;
    font-size: 0.9rem;
}

.financial-term-popup .popup-link:hover {
    color: var(--secondary-light);
}
"""

with open(css_path, "r") as f:
    css_content = f.read()

if ".financial-term-popup" not in css_content:
    with open(css_path, "a") as f:
        f.write("\n" + popup_css)

print("Done")
