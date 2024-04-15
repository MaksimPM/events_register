// Получение списка мероприятий и отображение их на странице
axios.get('/events/')
    .then(response => {
        const events = response.data;
        const eventListElement = document.getElementById('event-list');
        eventListElement.innerHTML = '<h2>Список мероприятий</h2>';
        events.forEach(event => {
            const eventItem = document.createElement('div');
            eventItem.innerHTML = `
                <p><strong>${event.title}</strong></p>
                <p><em>Дата: ${event.date}</em></p>
                <p>Место проведения: ${event.location}</p>
                <p>Описание: ${event.description}</p>
            `;
            eventListElement.appendChild(eventItem);
        });
    })
    .catch(error => console.error('Ошибка при получении списка мероприятий:', error));

// Обработка создания нового мероприятия
document.getElementById('create-event-form').addEventListener('submit', event => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const eventData = {
        title: formData.get('title'),
        date: formData.get('date'),
        location: formData.get('location'),
        description: formData.get('description')
    };

    axios.post('/events/', eventData)
        .then(response => {
            alert('Мероприятие успешно создано!');
            location.reload();
        })
        .catch(error => console.error('Ошибка при создании мероприятия:', error));
});
