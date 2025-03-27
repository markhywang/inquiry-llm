document.addEventListener('DOMContentLoaded', () => {
    var inquiryForm = document.getElementById('inquiry-form');
    var newInquiry = document.getElementById('new-inquiry');
    var generateDisplay = document.getElementById('generate-display');

    inquiryForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission

        // Get the value of the textarea
        const content = document.getElementById('inquiry-content');

        // Get the value of the selected radio button
        const numInsights = document.querySelector("input[type='radio'][name='num-insights']:checked").value;
        var errorMessage = document.getElementById('alert-message');

        if (!content.value.trim()) {
            console.log("Form submitted incorrectly.");
            content.style.borderColor = 'red';
            errorMessage.style.display = 'block';
        } else {
            console.log("Form submitted correctly.");
    
            content.style.borderColor = 'black';
            errorMessage.style.display = 'none';
            newInquiry.style.display = 'none';
            generateDisplay.innerHTML = "";

            console.log(`Content: ${content.value}`);
            console.log(`numInsights: ${numInsights}`);

            fetch('/generate', {
                method: 'POST',
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    content: content.value,
                    numInsights: numInsights
                })
            }).then(response => {
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';
                // Object to accumulate text per round
                let roundsText = {};

                function processText(text) {
                    // Each line should be a complete JSON object
                    let lines = text.split("\n");
                    // The last element may be an incomplete line; keep it in the buffer
                    buffer = lines.pop();
                    lines.forEach(line => {
                        if (line.trim()) {
                            let data = JSON.parse(line);
                            // When a new round starts, create a new card
                            if (data.start) {
                                let cardClass = (data.model === "LLM A") ? "answer-card" : "inquiry-card";
                                generateDisplay.innerHTML += `
                                    <div class="card ${cardClass}" id="card-${data.round}" style="display: block;">
                                        <h2>${data.model}</h2>
                                        <p></p>
                                    </div>`;
                                roundsText[data.round] = "";
                            }
                            if (data.token) {
                                roundsText[data.round] += data.token;
                                let card = document.getElementById(`card-${data.round}`);
                                if (card) {
                                    let p = card.querySelector("p");
                                    // Process the accumulated text: first replace LaTeX markers,
                                    // then parse Markdown so both are rendered correctly.
                                    let updatedText = roundsText[data.round]
                                        .replace(/\$\$(.*?)\$\$/g, "<span class='math'>$$$1$$</span>")
                                        .replace(/\\\((.*?)\\\)/g, "<span class='math'>\\($1\\)</span>");
                                    // Parse Markdown into HTML
                                    updatedText = marked.parse(updatedText);
                                    p.innerHTML = updatedText;
                                    // Render LaTeX/math (if you use KaTeX or similar)
                                    renderMathInElement(p);
                                }
                            }
                        }
                    });
                }

                function read() {
                    reader.read().then(({done, value}) => {
                        if (done) {
                            newInquiry.style.display = 'inline-block';
                            return;
                        }
                        buffer += decoder.decode(value, {stream: true});
                        processText(buffer);
                        read();
                    });
                }
                read();
            });
        }
    });

    // Retain your original typing animation functions in case you want to use them elsewhere.
    const typeText = (element, rawText, callback) => {
        let index = 0;
        const decodedText = decodeURIComponent(rawText); // Decode special characters
        const formattedText = marked.parse(decodedText); // Convert Markdown to HTML

        const typing = () => {
            if (index < formattedText.length) {
                element.innerHTML = formattedText.substring(0, index + 1); // Render as HTML
                index++;
                setTimeout(typing, 5); // Typing speed in milliseconds
            } else {
                // Ensure LaTeX is properly rendered once typing completes
                renderMathInElement(document.body);

                if (callback) {
                    callback(); // Call the next typing action once done
                }
            }
        };

        typing();
    };

    const typeSequentially = (cards, index = 0) => {
        if (index >= cards.length) return; // Stop when all cards are done

        const currentCard = cards[index];
        const textElement = currentCard.querySelector("p");
        const rawText = textElement.getAttribute("data-text");

        // Show the current card
        currentCard.style.display = "block";

        // Start typing the text for the current card
        typeText(textElement, rawText, () => typeSequentially(cards, index + 1));
    };

    newInquiry.addEventListener("click", () => {
        newInquiry.style.display = 'none';
        generateDisplay.innerHTML = "";
        generateDisplay.style.display = 'none';
        window.location.href = '/';
    });
});
