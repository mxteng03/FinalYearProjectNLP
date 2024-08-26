async function processText(event) {
    event.preventDefault();
    const text = document.getElementById('input_text').value;

    try {

        const normalizeResult = await postData('/normalize', { text });
        if (!normalizeResult) {
            alert("Normalization failed");
            return;
        }


        const translateResult = await postData('/translate', { text: normalizeResult.normalized_text });
        if (!translateResult) {
            alert("Translation failed");
            return;
        }


        const sentimentResult = await postData('/sentiment', { text: translateResult.translation });
        if (!sentimentResult) {
            alert("Sentiment analysis failed");
            return;
        }


        updateChatOutput(text, normalizeResult.normalized_text, translateResult.translation, sentimentResult.sentiment);


        const saveResult = await postData('/history/save', {
            input_text: text,
            normalized_text: normalizeResult.normalized_text,
            translated_text: translateResult.translation
        });

        if (!saveResult) {
            alert("Failed to save history");
        } else {
            await loadHistory();
        }

    } catch (error) {
        console.error("Error processing text:", error);
        alert("An error occurred while processing the text");
    }

    document.getElementById('input_text').value = '';
}

async function postData(url = '', data = {}) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            console.error(`Failed to fetch ${url}:`, response.statusText);
            return null;
        }
        return await response.json();
    } catch (error) {
        console.error(`Error in postData to ${url}:`, error);
        return null;
    }
}

function updateChatOutput(originalText, normalizedText, translatedText, sentimentEmoji) {
    const chatOutput = document.getElementById('chat-output');

    const userMessage = document.createElement('div');
    userMessage.classList.add('user-message');
    userMessage.innerText = `${originalText}`;
    chatOutput.appendChild(userMessage);

    const botMessage = document.createElement('div');
    botMessage.classList.add('bot-message');
    botMessage.innerText = `Meaning: ${normalizedText}\nTranslated: ${translatedText}\nSentiment: ${sentimentEmoji}`;
    chatOutput.appendChild(botMessage);

    chatOutput.scrollTop = chatOutput.scrollHeight;
}

async function loadHistory() {
    try {
        const historyResponse = await fetch('/history/get');

        if (!historyResponse.ok) {
            console.error("Failed to fetch history:", historyResponse.statusText);
            alert("Failed to load history");
            return;
        }

        const history = await historyResponse.json();
        const historyList = document.getElementById('history-list');
        historyList.innerHTML = '';  // Clear existing list
        history.forEach(item => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `Input: ${item.input_text}<br>Result: ${item.translated_text}`;
            historyList.appendChild(listItem);
        });
    } catch (error) {
        console.error("Error loading history:", error);
        alert("An error occurred while loading history");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadHistory();

    document.getElementById('clear-history-btn').addEventListener('click', async () => {
        if (confirm('Are you sure you want to clear your history?')) {
            const response = await fetch('/history/clear', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                alert('History cleared successfully.');
                await loadHistory();
            } else {
                alert('Failed to clear history.');
                console.error('Failed to clear history:', response.statusText);
            }
        }
    });
});
