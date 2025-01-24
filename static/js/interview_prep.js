document.addEventListener('DOMContentLoaded', function () {
    const addQuestionButton = document.getElementById('add-question');
    const questionInput = document.getElementById('question-input');
    const questionChipsContainer = document.getElementById('question-chips');

    /**
     * Handles the 'Add Question' button click to create a new question chip.
     */
    addQuestionButton.addEventListener('click', function () {
        const questionText = questionInput.value.trim();
        if (questionText) {
            addQuestionChip(questionText);
            questionInput.value = '';
        }
    });

    /**
     * Adds a question chip when the Enter key is pressed in the input field.
     * @param {KeyboardEvent} event - The keyboard event triggered.
     */
    questionInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            addQuestionButton.click();
        }
    });

    /**
     * Creates and appends a question chip to the container.
     * @param {string} question - The question text to add.
     */
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

    /**
     * Removes a question chip when its remove button is clicked.
     * @param {MouseEvent} event - The mouse event triggered.
     */
    questionChipsContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-chip')) {
            event.target.parentNode.remove();
        }
    });
});

/**
 * Updates the displayed duration value based on the slider input.
 * @param {string|number} val - The new duration value.
 */
function updateDurationValue(val) {
    document.getElementById('duration-value').innerText = val;
}
