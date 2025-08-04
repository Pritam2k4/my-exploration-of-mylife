const mongoose = require('mongoose');

const HabitSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true
    },
    frequency: {
        type: String, // daily, weekly, etc.
        required: true
    },
    completedDates: [{
        type: Date
    }],
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    }
});

module.exports = mongoose.model('Habit', HabitSchema);

