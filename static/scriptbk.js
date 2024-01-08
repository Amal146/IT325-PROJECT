document.addEventListener('DOMContentLoaded', function () {
    const ticketsContainer = document.getElementById('ticketsContainer');
    const urlParams = new URLSearchParams(window.location.search);
    const eventId = urlParams.get('eventId');
    const storedUserId = localStorage.getItem('userId');

    if (eventId) {
        // Fetch tickets for the specific event
        fetch(`/tickets/event/${eventId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Display tickets for the event
                data.forEach(ticket => {
                    const ticketElement = document.createElement('div');
                    ticketElement.innerHTML = `
                        <h3>Ticket Type: ${ticket.ticket_type}</h3>
                        <p><strong>Price:</strong> $${ticket.ticket_price}</p>
                        <button class="book-now-btn" data-ticket-id="${ticket.id}">Book now</button>
                        <hr>
                    `;
                    ticketsContainer.appendChild(ticketElement);

                    // Event listener for the "Book now" button
                    const bookNowButton = ticketElement.querySelector('.book-now-btn');
                    bookNowButton.addEventListener('click', () => {
                        const ticketId = bookNowButton.getAttribute('data-ticket-id');
                        bookTicket(ticketId, storedUserId); // Pass storedUserId as an argument
                    });
                });
            })
            .catch(error => {
                console.error('Error fetching ticket data:', error);
            });
    } else {
        console.error('Event ID is missing in the URL');
    }
});

function bookTicket(ticketId, storedUserId) {
    console.log(`Book now clicked for ticket ID: ${ticketId}`);
    const paymentData = {
        user_id: storedUserId,
        ticket_id: ticketId,
        payment_date: new Date().toISOString()
    };

    fetch('/payments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(paymentData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Payment failed');
        }
        return response.json();
    })
    .then(data => {
        console.log('Payment successful:', data);
        displayBookingSuccess();
    })
    .catch(error => {
        console.error('Error:', error.message , paymentData);
    });
}

function displayBookingSuccess() {
    alert('Booking successful!');
}
