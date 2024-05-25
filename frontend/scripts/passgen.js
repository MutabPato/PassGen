document.getElementById('generate').addEventListener('click', async function generatePass() {
	
	const length = document.getElementById('length').value;
	const hasLower = document.getElementById('lower').checked;
	const hasUpper = document.getElementById('upper').checked;
	const hasDigits = document.getElementById('digits').checked;
	const hasSymbols = document.getElementById('symbols').checked;
	
	if (!length || length <4 || length >20) {
		alert('Please enter a valid password length between 4 to 20.');
		return;
	}

	try {
		const response = await fetch('http://127.0.0.1:5000/', {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				length: parseInt(length),
				hasLower,
				hasUpper,
				hasDigits,
				hasSymbols
			})
		
		});

		if (!response.ok) {
			throw new Error('Network response was not ok');
		}

		const responseData = await response.json();
		document.getElementById('output').innerHTML = responseData.password;
		} catch(error) {
			console.error('Error:', error);
			alert('An error occured while generating the password. Please try again');
		}
});

document.getElementById('copy').addEventListener('click', async function copy() {
	const text = document.getElementById('output').innerHTML;

	if (!text) {
		alert('Nothing to copy. Generate a password first.');
		return;
	}

	try {

		await navigator.clipboard.writeText(text);
		alert('Password copied to clipboard');
	} catch(error) {
		console.error('Error:', error);
		alert('Failed to copy the password. Please try again.');
	}
});
