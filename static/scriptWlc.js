document.addEventListener('DOMContentLoaded', function () {
    const athleticsAthletes = document.getElementById('athleticsAthletes');
    const weightliftingAthletes = document.getElementById('weightliftingAthletes');
    const tennisAthletes = document.getElementById('tennisAthletes');
    const eventInfo = document.getElementById('eventInfo');
    const storedUserId = localStorage.getItem('userId');

    // Fetch athlete data from API endpoint
    fetch('http://localhost:5000/athletes') // Replace with your API endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Display athlete data for each sport type
            data.forEach(athlete => {
                const athleteContainer = document.getElementById('athleteInfo');
                const athleteElement = document.createElement('div');
                athleteElement.innerHTML = `
                    <h3>${athlete.name}</h3>
                    <p><strong>Sport:</strong> ${athlete.sport_type}</p>
                    <p><strong>Achievements:</strong> ${athlete.achievements}</p>
                    <hr>
                `;
                athleteContainer.appendChild(athleteElement);
            });
        })
        .catch(error => {
            console.error('Error fetching athlete data:', error);
        });
    
    // Fetch event data from API endpoint
    fetch('http://localhost:5000/events') // Replace with your API endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Display event data
            data.forEach(event => {
                const eventElement = document.createElement('div');
                eventElement.innerHTML = `
                    <h3>${event.event_type}</h3>
                    <p><strong>Date:</strong> ${event.event_date}</p>
                    <p><strong>Location:</strong> ${event.location}</p>
                    <button class="book-now-btn">Book now</button>
                    <hr>
                    `;
                    const bookNowButton = eventElement.querySelector('.book-now-btn');
                    bookNowButton.addEventListener('click', function () {
                        redirectToBooking(event.id); 
                    });
                    eventInfo.appendChild(eventElement)
            });
        })
        .catch(error => {
            console.error('Error fetching event data:', error);
        });
        
});

function redirectToBooking(eventId) {
    window.location.href = `/booking?eventId=${eventId}`;
}

