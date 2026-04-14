const quizzes = [
    {
        title: "Student Loan Basics",
        questions: [
            {
                q: "What is the NSLSC?",
                options: ["National Student Loan Service Centre", "New Student Lending Support Community", "National Savings and Loan Security Council"],
                correct: 0,
                explanation: "The NSLSC is the National Student Loan Service Centre, where most Canadian federal and integrated provincial loans are managed."
            },
            {
                q: "As of 2023, what is the interest rate on federal Canada Student Loans?",
                options: ["Prime + 2%", "5%", "0%"],
                correct: 2,
                explanation: "The federal government eliminated interest on Canada Student Loans starting in April 2023."
            },
            {
                q: "What is the Repayment Assistance Plan (RAP)?",
                options: ["A way to skip payments without telling anyone", "A program that adjusts your payments based on your income", "A loan to help you pay off other loans"],
                correct: 1,
                explanation: "RAP helps you manage your student loan payments by making them more affordable based on your gross family income and family size."
            }
        ]
    },
    {
        title: "Budgeting Fundamentals",
        questions: [
            {
                q: "What is the 50/30/20 rule?",
                options: ["50% Needs, 30% Wants, 20% Savings/Debt", "50% Rent, 30% Food, 20% Fun", "50% Savings, 30% Fixed Costs, 20% Wants"],
                correct: 0,
                explanation: "The 50/30/20 rule is a simple guide: 50% for needs, 30% for wants, and 20% for savings or extra debt repayment."
            },
            {
                q: "Which of these is a 'Variable Expense'?",
                options: ["Internet bill", "Groceries", "Rent"],
                correct: 1,
                explanation: "Variable expenses change month to month, like groceries or dining out, whereas rent is usually a 'Fixed Expense'."
            }
        ]
    },
    {
        title: "Credit & Debt",
        questions: [
            {
                q: "What are the two main credit bureaus in Canada?",
                options: ["Visa and Mastercard", "Equifax and TransUnion", "CRA and NSLSC"],
                correct: 1,
                explanation: "Equifax and TransUnion are the two major credit reporting agencies in Canada."
            },
            {
                q: "How does 'Credit Utilization' affect your score?",
                options: ["Using more of your limit is always better", "Using more than 30% of your limit can lower your score", "It has no effect on your score"],
                correct: 1,
                explanation: "Keeping your credit balance below 30% of your limit is generally recommended to maintain a healthy credit score."
            }
        ]
    },
    {
        title: "Saving & Investing 101",
        questions: [
            {
                q: "What does TFSA stand for?",
                options: ["Tax-Free Savings Account", "Total Financial Stability Asset", "Trust Fund Student Account"],
                correct: 0,
                explanation: "A TFSA allows you to set money aside tax-free throughout your lifetime."
            },
            {
                q: "What is 'Compound Interest'?",
                options: ["Interest that is only paid once", "Interest earned on both the initial principal and the accumulated interest", "A high interest rate for bad borrowers"],
                correct: 1,
                explanation: "Compound interest is 'interest on interest,' which allows your savings to grow exponentially over time."
            }
        ]
    }
];

let currentQuiz = null;
let currentQuestionIndex = 0;
let score = 0;

function startQuiz(quizIndex) {
    currentQuiz = quizzes[quizIndex];
    currentQuestionIndex = 0;
    score = 0;
    
    document.getElementById('selection-screen').style.display = 'none';
    document.getElementById('quiz-container').style.display = 'block';
    
    showQuestion();
}

function showQuestion() {
    const question = currentQuiz.questions[currentQuestionIndex];
    const questionArea = document.getElementById('question-area');
    const feedbackArea = document.getElementById('feedback-area');
    const nextBtn = document.getElementById('next-btn');
    const progress = document.getElementById('progress');
    
    feedbackArea.style.display = 'none';
    feedbackArea.className = 'feedback';
    nextBtn.style.display = 'none';
    
    const progressPercent = (currentQuestionIndex / currentQuiz.questions.length) * 100;
    progress.style.width = progressPercent + "%";
    
    questionArea.innerHTML = `
        <div class="question-text">${question.q}</div>
        <div class="options-list">
            ${question.options.map((opt, i) => `
                <button class="option-btn" onclick="checkAnswer(${i})">${opt}</button>
            `).join('')}
        </div>
    `;
}

function checkAnswer(selectedIndex) {
    const question = currentQuiz.questions[currentQuestionIndex];
    const feedbackArea = document.getElementById('feedback-area');
    const nextBtn = document.getElementById('next-btn');
    const options = document.querySelectorAll('.option-btn');
    
    options.forEach(btn => btn.disabled = true);
    
    if (selectedIndex === question.correct) {
        score++;
        options[selectedIndex].classList.add('correct');
        feedbackArea.innerHTML = `<strong>Correct!</strong> ${question.explanation}`;
        feedbackArea.classList.add('correct');
    } else {
        options[selectedIndex].classList.add('incorrect');
        options[question.correct].classList.add('correct');
        feedbackArea.innerHTML = `<strong>Not quite.</strong> ${question.explanation}`;
        feedbackArea.classList.add('incorrect');
    }
    
    feedbackArea.style.display = 'block';
    nextBtn.style.display = 'block';
    
    if (currentQuestionIndex === currentQuiz.questions.length - 1) {
        nextBtn.innerText = "See Results";
    } else {
        nextBtn.innerText = "Next Question →";
    }
}

function nextQuestion() {
    currentQuestionIndex++;
    
    if (currentQuestionIndex < currentQuiz.questions.length) {
        showQuestion();
    } else {
        showResults();
    }
}

function showResults() {
    const quizContainer = document.getElementById('quiz-container');
    const progress = document.getElementById('progress');
    progress.style.width = "100%";
    
    let message = "";
    if (score === currentQuiz.questions.length) message = "Perfect score! You're a financial wizard.";
    else if (score >= currentQuiz.questions.length / 2) message = "Great job! You have a solid foundation.";
    else message = "Good start! There's plenty more to learn in our Articles section.";
    
    quizContainer.innerHTML = `
        <div class="result-screen">
            <h2 style="color: var(--primary);">Quiz Complete!</h2>
            <div class="result-score">${score} / ${currentQuiz.questions.length}</div>
            <p style="font-size: 1.25rem; margin-bottom: 32px;">${message}</p>
            <div style="display: flex; gap: 16px; justify-content: center;">
                <button class="btn btn-primary" onclick="location.reload()">Try Another Quiz</button>
                <a href="articles.html" class="btn btn-outline">Read More Articles</a>
            </div>
        </div>
    `;
}
