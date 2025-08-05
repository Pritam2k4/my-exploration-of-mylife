import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getHabits, addHabit, completeHabit, deleteHabit } from "../api";

function DashboardPage() {
  const [habits, setHabits] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [habitData, setHabitData] = useState({
    habitName: "",
    description: "",
    category: "Health",
    targetDays: 30,
    color: "#4F46E5",
  });
  const user = JSON.parse(localStorage.getItem("user"));
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) return navigate("/");
    getHabits(user.id).then(setHabits);
    // eslint-disable-next-line
  }, []);

  const handleHabitChange = e => {
    setHabitData({ ...habitData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    const habit = await addHabit({ ...habitData, userId: user.id });
    setHabits([...habits, habit]);
    setHabitData({ habitName: "", description: "", category: "Health", targetDays: 30, color: "#4F46E5" });
    setShowModal(false);
  };

  const handleComplete = async id => {
    const updated = await completeHabit(id);
    setHabits(habits.map(h => h._id === id ? updated : h));
  };

  const handleDelete = async id => {
    if (!window.confirm("Delete this habit?")) return;
    await deleteHabit(id);
    setHabits(habits.filter(h => h._id !== id));
  };

  const logout = () => {
    localStorage.removeItem("user");
    navigate("/");
  };

  const today = new Date().toISOString().split("T")[0];
  const totalHabits = habits.length;
  const completedToday = habits.filter(h => h.completedDates.includes(today)).length;
  const longestStreak = Math.max(...habits.map(h => h.longestStreak || 0), 0);
  const totalDone = habits.reduce((a, h) => a + h.completedDates.length, 0);
  const totalPossible = habits.reduce((a, h) => a + (h.targetDays || 0), 0) || 1;
  const completionRate = Math.round((totalDone / totalPossible) * 100);

  return (
    <div className="dashboard-container">
      <header>
        <span>Welcome, {user?.username}!</span>
        <button onClick={logout}>⟵ Log Out</button>
        <button onClick={() => setShowModal(true)}>+ Add Habit</button>
      </header>

      <section className="stats">
        <div>Total Habits: {totalHabits}</div>
        <div>Completed Today: {completedToday}</div>
        <div>Longest Streak: {longestStreak}</div>
        <div>Completion Rate: {completionRate}%</div>
      </section>

      <section>
        <h2>Your Habits</h2>
        {habits.length === 0 ? (
          <p>No habits yet.</p>
        ) : (
          <ul>
            {habits.map(h => (
              <li key={h._id} style={{ borderLeft: `5px solid ${h.color}` }}>
                <b>{h.habitName}</b> ({h.category})
                <br />Streak: {h.currentStreak} | Done: {h.completedDates.length}/{h.targetDays}
                <br />
                <button disabled={h.completedDates.includes(today)}
                        onClick={() => handleComplete(h._id)}>
                  {h.completedDates.includes(today) ? "✓ Done Today" : "Complete Today"}
                </button>
                <button onClick={() => handleDelete(h._id)}>Delete</button>
                <p>{h.description}</p>
              </li>
            ))}
          </ul>
        )}
      </section>

      {/* Modal */}
      {showModal && (
        <div className="modal">
          <form onSubmit={handleSubmit} className="modal-form">
            <h3>Add New Habit</h3>
            <input name="habitName" placeholder="Name" required
                   value={habitData.habitName}
                   onChange={handleHabitChange}/>
            <textarea name="description" placeholder="Description (optional)"
                      value={habitData.description}
                      onChange={handleHabitChange}/>
            <select name="category" value={habitData.category} onChange={handleHabitChange}>
              <option>Health</option><option>Fitness</option>
              <option>Productivity</option><option>Learning</option>
              <option>Mindfulness</option><option>Other</option>
            </select>
            <input name="targetDays" type="number" min={1}
                   value={habitData.targetDays} onChange={handleHabitChange} />
            <input name="color" type="color"
                   value={habitData.color} onChange={handleHabitChange} />
            <button type="submit">Add Habit</button>
            <button onClick={e => { e.preventDefault(); setShowModal(false); }}>Cancel</button>
          </form>
        </div>
      )}
    </div>
  );
}
export default DashboardPage;