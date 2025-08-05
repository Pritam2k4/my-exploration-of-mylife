/*  ─────────────────────────  server.js  ─────────────────────────
 *  Express + MongoDB Atlas API for HabitFlow
 *  ----------------------------------------------------------------
 *  Endpoints
 *    GET    /api/users                   – all users
 *    GET    /api/users/recent?limit=5    – newest → oldest
 *    POST   /api/users                   – create user  (+Email doc)
 *    GET    /api/users/:id               – user + habits
 *
 *    POST   /api/habits                  – create habit
 *    GET    /api/habits/:userId          – habits for user
 *    POST   /api/habits/:id/complete     – mark today complete
 *    DELETE /api/habits/:id              – delete habit
 *  ---------------------------------------------------------------- */

require('dotenv').config();
const express  = require('express');
const mongoose = require('mongoose');
const cors     = require('cors');
const path     = require('path');

const app  = express();
const PORT = process.env.PORT || 5000;

/* ───────────────────────────  middleware  ────────────────────────── */
app.use(
  cors({
    origin: [
      'http://localhost:3000',     // react dev
      'http://127.0.0.1:5500',     // VS-Code Live Server
      'http://localhost:5500',     // "
      'http://localhost'           // static file open
    ],
    credentials: true
  })
);
app.use(express.json());

/* ────────────────────  serve the static frontend  ────────────────── */
app.use(express.static(path.join(__dirname, '..', 'frontend')));

/* ───────────────────────────  database  ──────────────────────────── */
mongoose
  .connect(process.env.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
  })
  .then(() => console.log('✅  MongoDB Atlas connected'))
  .catch(err => {
    console.error('❌  Mongo connection error:', err.message);
    process.exit(1);
  });

/* ───────────────────────────  models  ────────────────────────────── */
const User  = require('./models/users');
const Habit = require('./models/habits');
const Email = require('./models/emails');   // new lightweight email collection

/* ───────────────────────────  routes  ────────────────────────────── */
// -------- USERS ----------------------------------------------------

// create new user  (also store e-mail separately)
app.post('/api/users', async (req, res) => {
  try {
    const { username, email } = req.body;

    // duplication check
    const dup = await User.findOne({ $or: [{ username }, { email }] });
    if (dup) return res.status(400).json({ error: 'User already exists' });

    const user = await User.create({ username, email });
    await Email.create({ address: email.toLowerCase() });

    res.status(201).json({ user: { id: user._id, username, email } });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// all users (admin / debug)
app.get('/api/users', async (_req, res) => {
  const users = await User.find().select('-__v').sort({ createdAt: -1 });
  res.json(users);
});

// newest N users for “recent users” list
app.get('/api/users/recent', async (req, res) => {
  const limit = parseInt(req.query.limit, 10) || 5;
  const recent = await User.find()
    .sort({ createdAt: -1 })
    .limit(limit)
    .select('username email createdAt');
  res.json(recent);
});

// single user + their habits
app.get('/api/users/:id', async (req, res) => {
  try {
    const user   = await User.findById(req.params.id).select('-__v');
    const habits = await Habit.find({ userId: user._id }).select('-__v');
    if (!user) return res.status(404).json({ error: 'User not found' });
    res.json({ user, habits });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// -------- HABITS ---------------------------------------------------

// helper for streak calc
function streak(arr) {
  if (arr.length === 0) return 0;
  const sorted = [...arr].sort().reverse();
  let s = 1;
  for (let i = 1; i < sorted.length; i++) {
    const d1 = new Date(sorted[i - 1]), d2 = new Date(sorted[i]);
    const diff = (d1 - d2) / 86_400_000;          // ms → days
    if (diff === 1) s++;
    else break;
  }
  return s;
}

// create habit
app.post('/api/habits', async (req, res) => {
  try {
    const habit = await Habit.create(req.body);
    // bump user counter
    await User.findByIdAndUpdate(habit.userId, { $inc: { totalHabits: 1 } });
    res.status(201).json({ habit });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// habits for a user
app.get('/api/habits/:userId', async (req, res) => {
  const list = await Habit.find({ userId: req.params.userId }).select('-__v');
  res.json(list);
});

// complete today
app.post('/api/habits/:id/complete', async (req, res) => {
  try {
    const today = new Date().toISOString().split('T')[0];
    const habit = await Habit.findById(req.params.id);
    if (!habit) return res.status(404).json({ error: 'Habit not found' });

    if (!habit.completedDates.includes(today)) {
      habit.completedDates.push(today);
      habit.currentStreak = streak(habit.completedDates);
      habit.longestStreak = Math.max(habit.longestStreak, habit.currentStreak);
      await habit.save();

      // bump “completedToday” for the owner
      await User.findByIdAndUpdate(habit.userId, { $inc: { completedToday: 1 } });
    }
    res.json({ habit });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// delete habit
app.delete('/api/habits/:id', async (req, res) => {
  try {
    const h = await Habit.findByIdAndDelete(req.params.id);
    if (h) await User.findByIdAndUpdate(h.userId, { $inc: { totalHabits: -1 } });
    res.json({ success: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

/* ─────────────────────────  fallback route  ─────────────────────────
 *  Needed when a user reloads dashboard.html directly (static hosting)
 */
app.get('*', (_req, res) => {
  res.sendFile(path.join(__dirname, '..', 'frontend', 'login.html'));
});

/* ───────────────────────────  start  ─────────────────────────────── */
app.listen(PORT, () => console.log(`🚀  Server running on http://localhost:${PORT}`));

