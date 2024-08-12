function receiveData() {
    fetch('/create_cookies', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: {
                payload: {
                    call_control_id: 'call_control_id',
                    caller_id_name: 'caller_id_name'
                }
            }
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data.call_control_id);
        console.log(data.caller_id_name);
    })
    .catch(error => console.error('Error:', error));
}

window.onload = receiveData;


