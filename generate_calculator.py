import re

html_insertion = """
    <!-- CANADIAN STUDENT LOAN REPAYMENT CALCULATOR -->
    <section class="section-padding" style="background: var(--white); border-bottom: 1px solid #ECECEC;">
        <div class="container">
            <div style="max-width: 1000px; margin: 0 auto;">
                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px;">
                    <div>
                        <h2 style="font-size: 2.5rem; color: var(--primary);">Canadian Student Loan Repayment Calculator</h2>
                        <p style="color: var(--text); font-size: 1.1rem;">Model your exact repayment timeline, grace period, and RAP eligibility.</p>
                    </div>
                    <div id="boc-prime-badge" style="background: var(--bg); padding: 8px 16px; border-radius: 8px; border: 1px solid var(--primary); text-align: right; color: var(--primary); font-weight: 600; font-size: 0.9rem;">
                        Fetching Prime Rate...
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px;">
                    <!-- INPUTS -->
                    <div class="calc-card" style="box-shadow: none; border: 1px solid #E0E0E0;">
                        <h3 style="border-bottom: none; margin-bottom: 12px;">Your Loans</h3>
                        <div id="slc-loans-container"></div>
                        <button id="slc-add-loan-btn" class="btn btn-outline" style="width: 100%; margin-bottom: 32px; padding: 10px;">+ Add Another Loan</button>

                        <h3 style="border-bottom: none; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                            Repayment Assistance (RAP)
                            <label class="toggle-switch">
                                <input type="checkbox" id="slc-rap-toggle">
                                <span class="slider"></span>
                            </label>
                        </h3>
                        <div id="slc-rap-inputs" style="display: none; background: #f9f9f9; padding: 16px; border-radius: 8px; margin-bottom: 32px;">
                            <div class="form-group" style="margin-bottom: 12px;">
                                <label>Gross Annual Income ($)</label>
                                <input type="number" id="slc-rap-income" value="30000">
                            </div>
                            <div class="form-group" style="margin-bottom: 12px;">
                                <label>Family Size</label>
                                <select id="slc-rap-family">
                                    <option value="1">1 Person</option>
                                    <option value="2">2 People</option>
                                    <option value="3">3 People</option>
                                    <option value="4">4 People</option>
                                    <option value="5">5 or more People</option>
                                </select>
                            </div>
                            <div style="color: var(--primary); font-weight: 600; font-size: 0.95rem;">
                                Federal Affordable Payment: <span id="slc-rap-payment-display">$0.00</span>/month
                            </div>
                        </div>

                        <div style="background: var(--bg); padding: 24px; border-radius: 12px; text-align: center;">
                            <label style="font-weight: 700; color: var(--primary); font-size: 1.1rem; margin-bottom: 8px;">Total Monthly Payment</label>
                            <div style="font-size: 2.5rem; font-family: 'Fraunces', serif; color: var(--primary); font-weight: 700; margin-bottom: 16px;" id="slc-slider-value-display">
                                $0
                            </div>
                            <input type="range" id="slc-payment-slider" min="0" max="2000" value="0" style="width: 100%; cursor: pointer;">
                            <div style="display: flex; justify-content: space-between; margin-top: 8px; color: var(--muted); font-size: 0.85rem; font-weight: 600;">
                                <span>Minimum: <span id="slc-min-label">$0</span></span>
                                <span>Custom / Accelerated</span>
                            </div>
                        </div>
                    </div>

                    <!-- OUTPUTS -->
                    <div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
                            <div style="background: #f0f7f5; padding: 20px; border-radius: 12px; border: 1px solid rgba(26,107,90,0.1);">
                                <div style="font-size: 0.85rem; color: var(--muted); font-weight: 700; text-transform: uppercase;">Total Balance</div>
                                <div style="font-size: 1.8rem; color: var(--primary); font-weight: 700; font-family: 'Fraunces', serif;" id="slc-out-balance">$0</div>
                            </div>
                            <div style="background: #f0f7f5; padding: 20px; border-radius: 12px; border: 1px solid rgba(26,107,90,0.1);">
                                <div style="font-size: 0.85rem; color: var(--muted); font-weight: 700; text-transform: uppercase;">Time to Payoff</div>
                                <div style="font-size: 1.8rem; color: var(--primary); font-weight: 700; font-family: 'Fraunces', serif;" id="slc-out-time">0 yrs 0 mos</div>
                            </div>
                            <div style="background: #fff5eb; padding: 20px; border-radius: 12px; border: 1px solid rgba(232,160,32,0.2);">
                                <div style="font-size: 0.85rem; color: var(--muted); font-weight: 700; text-transform: uppercase;">Total Interest</div>
                                <div style="font-size: 1.8rem; color: var(--secondary); font-weight: 700; font-family: 'Fraunces', serif;" id="slc-out-interest">$0</div>
                            </div>
                            <div style="background: #f0f7f5; padding: 20px; border-radius: 12px; border: 1px solid rgba(26,107,90,0.1);">
                                <div style="font-size: 0.85rem; color: var(--muted); font-weight: 700; text-transform: uppercase;">Interest Saved</div>
                                <div style="font-size: 1.8rem; color: var(--primary); font-weight: 700; font-family: 'Fraunces', serif;" id="slc-out-saved">$0</div>
                            </div>
                        </div>

                        <div style="margin-bottom: 24px;">
                            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px;">
                                <span style="color: var(--primary);">Principal: <span id="slc-bar-prin-lbl">0%</span></span>
                                <span style="color: var(--secondary);">Interest: <span id="slc-bar-int-lbl">0%</span></span>
                            </div>
                            <div style="height: 12px; width: 100%; background: #eee; border-radius: 6px; overflow: hidden; display: flex;">
                                <div id="slc-bar-prin" style="height: 100%; background: var(--primary); width: 0%; transition: width 0.3s;"></div>
                                <div id="slc-bar-int" style="height: 100%; background: var(--secondary); width: 0%; transition: width 0.3s;"></div>
                            </div>
                        </div>

                        <div id="slc-callout" style="display: none; background: #e6f3f0; border-left: 4px solid var(--primary); padding: 16px; border-radius: 0 8px 8px 0; font-size: 0.95rem; margin-bottom: 24px; color: var(--text);">
                            <!-- Dynamic text -->
                        </div>

                        <div style="max-height: 400px; overflow-y: auto; border: 1px solid #E0E0E0; border-radius: 8px;">
                            <table style="width: 100%; border-collapse: collapse; text-align: right; font-size: 0.85rem;">
                                <thead style="background: var(--bg); position: sticky; top: 0; box-shadow: 0 1px 0 #E0E0E0;">
                                    <tr>
                                        <th style="padding: 12px; text-align: center;">Month</th>
                                        <th style="padding: 12px;">Payment</th>
                                        <th style="padding: 12px;">Interest</th>
                                        <th style="padding: 12px;">Principal</th>
                                        <th style="padding: 12px;">Balance</th>
                                    </tr>
                                </thead>
                                <tbody id="slc-table-body">
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                
                <p style="font-size: 0.8rem; color: #888; text-align: center; margin-top: 40px;">
                    This calculator is for educational and estimation purposes only. Actual payments, interest rates, and eligibility for programs like RAP will vary. Interest rates for variable-rate provincial loans are derived from the Bank of Canada overnight rate and will change when the Bank of Canada adjusts its policy rate. Always verify your terms with the NSLSC or your provincial student aid office.
                </p>
            </div>
        </div>

        <!-- RAP Modal -->
        <div id="slc-rap-modal" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 10000; align-items: center; justify-content: center;">
            <div style="background: #fff; padding: 32px; border-radius: 12px; max-width: 500px; width: 90%;">
                <h3 style="color: var(--primary); margin-bottom: 16px;">Enable Repayment Assistance (RAP)?</h3>
                <p style="font-size: 0.95rem; margin-bottom: 16px;">To qualify for the federal Repayment Assistance Plan, you must meet the following criteria:</p>
                <ul style="font-size: 0.9rem; margin-bottom: 24px; padding-left: 20px;">
                    <li style="margin-bottom: 8px;">Loans must be in repayment — at least 6 months post-graduation</li>
                    <li style="margin-bottom: 8px;">Loans must be in good standing and not in default</li>
                    <li style="margin-bottom: 8px;">Monthly income must fall below qualifying thresholds</li>
                    <li style="margin-bottom: 8px;">You must reapply every 6 months</li>
                    <li style="margin-bottom: 8px;"><strong>Note:</strong> RAP applies to the federal Canada Student Loan only — provincial assistance is calculated separately.</li>
                </ul>
                <div style="display: flex; gap: 16px; justify-content: flex-end;">
                    <button id="slc-rap-cancel" class="btn btn-outline" style="padding: 8px 16px;">Cancel</button>
                    <button id="slc-rap-confirm" class="btn btn-primary" style="padding: 8px 16px;">Confirm & Enable</button>
                </div>
            </div>
        </div>
    </section>
"""

with open("calculators.html", "r") as f:
    content = f.read()

# Insert after <header class="page-header">...</header>
header_end = content.find("</header>") + 9
new_content = content[:header_end] + "\n" + html_insertion + "\n" + content[header_end:]

# Add script tag before </body>
new_content = new_content.replace('</body>', '    <script src="js/student-loan-calc.js"></script>\n</body>')

with open("calculators.html", "w") as f:
    f.write(new_content)
