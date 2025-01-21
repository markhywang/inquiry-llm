document.addEventListener('DOMContentLoaded', () => {
    var inquiryForm = document.getElementById('inquiry-form');
    var newInquiry = document.getElementById('new-inquiry');
    var generateDisplay = document.getElementById('generate-display');

    // Make sure inquiry is not empty when submitting form
    inquiryForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission

        // Get the value of the textarea
        const content = document.getElementById('inquiry-content');

        // Get the value of the selected radio button
        const numInsights = document.querySelector("input[type='radio'][name='num-insights']:checked").value;
        var errorMessage = document.getElementById('alert-message');

        if (!content.value.trim()) {
            console.log("Form submitted incorrectly.")
            content.style.borderColor = 'red';
            errorMessage.style.display = 'block';
        } else {
            console.log("Form submitted correctly.");
    
            content.style.borderColor = 'black';
            errorMessage.style.display = 'none';
            newInquiry.style.display = 'none';
            generateDisplay.innerHTML = "";

            console.log(`Content: ${content.value}`)
            console.log(`numInsights: ${numInsights}`)

            fetch('/generate', {
                method: 'POST',
                body: JSON.stringify({
                    content: content.value,
                    numInsights: numInsights
                })
            })
            .then(response => response.json())
            .then(data =>  {
                // Display screen on text
                for (let i = 0; i < data.responses.length; i++) {
                    if (i % 2 == 0) {
                        generateDisplay.innerHTML += `<div class="card answer-card" style="display: none;"><h2>LLM A</h2><p data-text="${data.responses[i]}"></p></div>`
                    } else {
                        generateDisplay.innerHTML += `<div class="card inquiry-card" style="display: none;"><h2>LLM B</h2><p data-text="${data.responses[i]}"></p></div>`
                    }
                }

                let cards = document.querySelectorAll(".card");
                typeSequentially(cards);

                // Show button to allow user to re-input a separate prompt
                newInquiry.style.display = 'inline-block';
            });
        }
    });

    // Typing animation for each LLM card
    const typeText = (element, text, callback) => {
        let index = 0;

        const typing = () => {
            if (index < text.length) {
                element.textContent += text[index];
                index++;
                setTimeout(typing, 10); // Typing speed in milliseconds
            } else if (callback) {
                callback(); // Call the next typing action once done
            }
        };

        typing();
    };

    // Make sure subsequent cards only appear after previous card is done typing
    const typeSequentially = (cards, index = 0) => {
        if (index >= cards.length) return; // Stop when all cards are done

        const currentCard = cards[index];
        const textElement = currentCard.querySelector("p");
        const text = textElement.getAttribute("data-text");

        // Show the current card
        currentCard.style.display = "block";

        // Start typing the text for the current card
        typeText(textElement, text, () => typeSequentially(cards, index + 1));
    };

    // When "New Inquiry" button is clicked, refresh to a clean index.html
    newInquiry.addEventListener("click", () => {
        newInquiry.style.display = 'none';
        generateDisplay.innerHTML = "";
        generateDisplay.style.display = 'none';

        window.location.href = '/';
    });
});