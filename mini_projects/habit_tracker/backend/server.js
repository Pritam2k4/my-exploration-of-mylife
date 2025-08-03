const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

const DB_FILE = './backend/db.json';

function readDB() {
  return JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
}

function writeDB(data) {
  fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
}

app.get('/habits', (req, res) => {
  const db = readDB();
  const today = new Date().toISOString().split('T')[0];
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const yDay = yesterday.toISOString().split('T')[0];

  db.forEach(habit => {
    if (habit.history && Object.keys(habit.history).length > 0) {
      const didYesterday = habit.history[yDay];
      const didToday = habit.history[today];

      if (!didYesterday && !didToday) {
        habit.streak = 0; // Missed both yesterday and today
      } else if (!didYesterday && didToday) {
        habit.streak = 1; // Only did it today
      }
      // If didYesterday and/or didToday, streak is already updated by /mark
    }
  });

  writeDB(db);
  res.json(db);
});

app.delete('/habits/:id', (req, res) => {
  const db = readDB();
  const idToDelete = parseInt(req.params.id);
  const updatedDB = db.filter(habit => habit.id !== idToDelete);
  writeDB(updatedDB);
  res.json({ success: true });
});



app.post('/habits', (req, res) => {
  const db = readDB();
  const newHabit = {
    id: Date.now(),
    name: req.body.name,
    streak: 0,
    history: {}
  };
  db.push(newHabit);
  writeDB(db);
  res.status(201).json(newHabit);
});

app.post('/habits/:id/mark', (req, res) => {
  const db = readDB();
  const habit = db.find(h => h.id == req.params.id);
  const today = new Date().toISOString().split('T')[0];

  if (!habit.history[today]) {
    habit.history[today] = true;
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yDay = yesterday.toISOString().split('T')[0];

    habit.streak = habit.history[yDay] ? habit.streak + 1 : 1;
    writeDB(db);
  }

  res.json(habit);
});

app.listen(PORT, () => console.log(`✅ Server running on http://localhost:${PORT}`));
