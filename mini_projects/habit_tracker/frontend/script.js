let currentUserId = null;

async function createUser() {
    const username = document.getElementById('username').value;

    const res = await fetch('http://localhost:3000/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username })
    });

    const data = await res.json();
    currentUserId = data._id;
    document.getElementById('habit-section').style.display = 'block';
    loadHabits();
}

async function addHabit() {
    const title = document.getElementById('habit-title').value;
    const frequency = document.getElementById('habit-frequency').value;

    await fetch('http://localhost:3000/api/habits', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: currentUserId, title, frequency })
    });

    loadHabits();
}

async function loadHabits() {
    const res = await fetch(`http://localhost:3000/api/users/${currentUserId}/habits`);
    const habits = await res.json();
    const list = document.getElementById('habit-list');
    list.innerHTML = '';
    habits.forEach(h => {
        const li = document.createElement('li');
        li.innerText = `${h.title} (${h.frequency})`;
        list.appendChild(li);
    });
}
