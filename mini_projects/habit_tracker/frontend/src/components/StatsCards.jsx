import React from "react";

export default function StatsCards({ totalHabits, completedToday, longestStreak, completionRate }) {
  return (
    <div className="stats">
      <div>Total Habits: {totalHabits}</div>
      <div>Completed Today: {completedToday}</div>
      <div>Longest Streak: {longestStreak}</div>
      <div>Completion Rate: {completionRate}%</div>
    </div>
  );
}
