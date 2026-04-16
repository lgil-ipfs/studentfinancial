class Quiz {
    constructor(containerId, questions) {
        this.container = document.getElementById(containerId);
        this.questions = questions;
        this.currentIndex = 0;
        this.score = 0;
        this.init();
    }

    init() {
        this.render();
    }

    render() {
        this.container.innerHTML = `
            <div class="quiz-header">
                <h2>Check Your Knowledge</h2>
                <p>See how much you've learned from this article!</p>
            </div>
            <div id="quiz-questions-container"></div>
            <div id="quiz-results-container" class="quiz-results">
                <h3>Quiz Complete!</h3>
                <div class="results-score" id="results-score">0/0</div>
                <p id="results-message"></p>
                <button class="btn btn-primary" onclick="location.reload()">Take Quiz Again</button>
            </div>
        `;
        this.questionsContainer = document.getElementById('quiz-questions-container');
        this.resultsContainer = document.getElementById('quiz-results-container');
        this.showQuestion(0);
    }

    showQuestion(index) {
        const q = this.questions[index];
        const questionHtml = `
            <div class="quiz-question active" id="q-${index}">
                <div class="quiz-progress">Question ${index + 1} of ${this.questions.length}</div>
                <div class="question-text">${q.question}</div>
                <div class="quiz-options">
                    ${q.options.map((opt, i) => `
                        <button class="quiz-option" data-index="${i}">${opt}</button>
                    `).join('')}
                </div>
                <div class="quiz-feedback" id="feedback-${index}"></div>
                <div class="quiz-footer">
                    <div class="quiz-progress-dots"></div>
                    <button class="btn btn-primary quiz-next-btn" id="next-${index}">Next Question</button>
                </div>
            </div>
        `;
        this.questionsContainer.innerHTML = questionHtml;

        const options = this.questionsContainer.querySelectorAll('.quiz-option');
        options.forEach(opt => {
            opt.addEventListener('click', (e) => this.handleAnswer(e, index));
        });

        const nextBtn = document.getElementById(`next-${index}`);
        nextBtn.addEventListener('click', () => {
            if (this.currentIndex < this.questions.length - 1) {
                this.currentIndex++;
                this.showQuestion(this.currentIndex);
            } else {
                this.showResults();
            }
        });
    }

    handleAnswer(e, index) {
        const selectedBtn = e.currentTarget;
        const selectedIndex = parseInt(selectedBtn.dataset.index);
        const q = this.questions[index];
        const feedback = document.getElementById(`feedback-${index}`);
        const nextBtn = document.getElementById(`next-${index}`);
        const allOptions = this.questionsContainer.querySelectorAll('.quiz-option');

        // Disable all options
        allOptions.forEach(opt => opt.style.pointerEvents = 'none');

        if (selectedIndex === q.correctIndex) {
            selectedBtn.classList.add('correct');
            feedback.innerHTML = `<strong>Correct!</strong> ${q.explanation}`;
            feedback.className = 'quiz-feedback show correct';
            this.score++;
        } else {
            selectedBtn.classList.add('wrong');
            allOptions[q.correctIndex].classList.add('correct');
            feedback.innerHTML = `<strong>Not quite.</strong> ${q.explanation}`;
            feedback.className = 'quiz-feedback show wrong';
        }

        nextBtn.classList.add('show');
        if (this.currentIndex === this.questions.length - 1) {
            nextBtn.textContent = 'See Results';
        }
    }

    showResults() {
        this.questionsContainer.style.display = 'none';
        this.resultsContainer.classList.add('active');
        const scoreDisplay = document.getElementById('results-score');
        const messageDisplay = document.getElementById('results-message');
        
        scoreDisplay.textContent = `${this.score}/${this.questions.length}`;
        
        const percentage = (this.score / this.questions.length) * 100;
        if (percentage === 100) {
            messageDisplay.textContent = "Perfect score! You're a financial pro.";
        } else if (percentage >= 70) {
            messageDisplay.textContent = "Great job! You've got a solid handle on this.";
        } else {
            messageDisplay.textContent = "Good effort! A quick re-read might help clear things up.";
        }
    }
}
