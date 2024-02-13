// main.js

function startSurvey() {
    window.location.href = 'survey.html';
}

function calculateAnxiety() {
    // Check if any radio button is selected for each question
    const questions = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7'];
    let allQuestionsAnswered = true;

    questions.forEach(question => {
        const selectedOption = document.querySelector(`input[name="${question}"]:checked`);
        if (!selectedOption) {
            allQuestionsAnswered = false;
        }
    });

    // Display a message if not all questions are answered
    if (!allQuestionsAnswered) {
        alert('Please fill out all questions before proceeding.');
        return;
    }

    // Code to store results
    const surveyForm = document.getElementById('anxietyForm');
    const formData = new FormData(surveyForm);

    const results = {};
    formData.forEach((value, key) => {
        results[key] = value;
    });

    const jsonData = JSON.stringify(results);

    // Save the results or perform other actions
    console.log(jsonData);

    // Redirect to the next page after storing results
    window.location.href = 'nextpage.html';  // Replace 'nextpage.html' with the appropriate next page
}
