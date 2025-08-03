const list = document.getElementById('habit-list');
const form = document.getElementById('add-form');
const input = document.getElementById('habit-name');
const API = 'http://localhost:3000/habits';

async function fetchHabits() {
  const res = await fetch(API);
  const habits = await res.json();
  list.innerHTML = '';
  habits.forEach(habit => {
    const div = document.createElement('div');
    div.className = 'habit';
   div.innerHTML = `
  <b>${habit.name}</b><br/>
  Streak: ${habit.streak}<br/>
  <button onclick="markHabit(${habit.id})">Mark Done</button>
  <button onclick="deleteHabit(${habit.id})" style="margin-left:10px; background:#ffcccc;">Delete</button>
`;
    div.style.marginBottom = '10px';
    div.style.padding = '10px';
    list.appendChild(div);
  });
}

async function markHabit(id) {
  await fetch(`${API}/${id}/mark`, { method: 'POST' });
  fetchHabits();
}

form.onsubmit = async (e) => {
  e.preventDefault();
  await fetch(API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: input.value })
  });
  input.value = '';
  fetchHabits();
};

fetchHabits();

async function deleteHabit(id) {
  const confirmed = confirm("Are you sure you want to delete this habit?");
  if (!confirmed) return;

  try {
    const res = await fetch(`${API}/${id}`, { method: 'DELETE' });
    if (res.ok) {
      fetchHabits(); // Refresh list
    } else {
      console.error("Failed to delete habit");
    }
  } catch (err) {
    console.error("Error deleting habit:", err);
  }
}

