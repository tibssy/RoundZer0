document.addEventListener('DOMContentLoaded', function () {
    const addQuestionButton = document.getElementById('add-question');
    const questionInput = document.getElementById('question-input');
    const questionChipsContainer = document.getElementById('question-chips');

    addQuestionButton.addEventListener('click', function () {
        const questionText = questionInput.value.trim();
        if (questionText) {
            addQuestionChip(questionText);
            questionInput.value = '';
        }
    });

    questionInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            addQuestionButton.click();
        }
    });

    function addQuestionChip(question) {
        const chip = document.createElement('div');
        chip.classList.add('question-chip');
        chip.innerHTML = `
            ${question}
            <span class="remove-chip" data-question="${question}">×</span>
            <input type="hidden" name="questions" value="${question}">
        `;
        questionChipsContainer.appendChild(chip);
    }

    questionChipsContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-chip')) {
            event.target.parentNode.remove();
        }
    });
});

function updateDurationValue(val) {
    document.getElementById('duration-value').innerText = val;
}
