// ✅ 1. Load environment variables first
require('dotenv').config(); 

// ✅ 2. Import dependencies
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

// ✅ 3. Import models
const User = require('./models/users');
const Habit = require('./models/habits');

// ✅ 4. Create Express app and middleware
const app = express();
app.use(cors());
app.use(express.json());

// ✅ 5. Connect to MongoDB Atlas
mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log("MongoDB connected"))
  .catch(err => console.error("MongoDB connection error:", err));

// ✅ 6. Define API routes

// Create user
app.post('/api/users', async (req, res) => {
  const { username } = req.body;
  try {
    const user = new User({ username });
    await user.save();
    res.json(user);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Add habit
app.post('/api/habits', async (req, res) => {
  const { userId, title, frequency } = req.body;
  try {
    const habit = new Habit({ title, frequency, user: userId });
    await habit.save();

    const user = await User.findById(userId);
    user.habits.push(habit);
    await user.save();

    res.json(habit);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Get all habits for a user
app.get('/api/users/:id/habits', async (req, res) => {
  try {
    const user = await User.findById(req.params.id).populate('habits');
    res.json(user.habits);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// ✅ 7. Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
