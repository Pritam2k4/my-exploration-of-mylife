import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { createUser, getRecentUsers } from "../api";

function LoginPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [recentUsers, setRecentUsers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    getRecentUsers().then(res => setRecentUsers(res));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const user = await createUser({ username: username.trim(), email: email.trim() });
      localStorage.setItem("user", JSON.stringify(user));
      navigate("/dashboard");
    } catch (err) {
      alert("Login failed: " + err.message);
    }
  };

  const autofill = u => {
    setUsername(u.username);
    setEmail(u.email);
  };

  return (
    <div className="login-card">
      <h1 className="logo">HabitFlow</h1>
      <p>Track your habits, build your future</p>
      <form onSubmit={handleSubmit}>
        <input placeholder="Enter username"
               value={username}
               onChange={e => setUsername(e.target.value)}
               required />
        <input placeholder="Enter email"
               type="email"
               value={email}
               onChange={e => setEmail(e.target.value)}
               required />
        <button type="submit">Get Started →</button>
      </form>
      <div>
        <b>Recent Users:</b>
        {recentUsers.length === 0 && <span> None yet.</span>}
        <ul>
          {recentUsers.map(u => (
            <li key={u.email} onClick={() => autofill(u)} style={{cursor:"pointer"}}>
              {u.username} &lt;{u.email}&gt;
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default LoginPage;