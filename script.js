document.getElementById('emailForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const url = document.getElementById('urlInput').value;
    
    if (!url) {
        alert("Please enter a valid URL.");
        return;
    }

    try {
        // Fetch data from the backend (assume you have a backend API endpoint)
        const response = await fetch('http://127.0.0.1:5000/extract-emails', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();
        displayEmails(data.emails);
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
    }
});

function displayEmails(emails) {
    const emailList = document.getElementById('emailList');
    emailList.innerHTML = '';
    if (emails && emails.length) {
        emails.forEach(email => {
            const li = document.createElement('li');
            li.textContent = email;
            emailList.appendChild(li);
        });
    } else {
        emailList.innerHTML = '<li>No emails found.</li>';
    }
}
