document.addEventListener('DOMContentLoaded', () => {
    // Make sure inquiry is not empty when submitting form
    document.getElementById('inquiry-form').addEventListener('submit', function(event) {
        var content = document.getElementById('inquiry-content');
        if (!content.value.trim()) {
            event.preventDefault(); // Prevent the event of form submission
            content.style.borderColor = 'red';
        } else {
            content.style.borderColor = 'black';
        }
    });
})