const mongoose = require('mongoose');

const habitSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  habitName: {
    type: String,
    required: true,
    trim: true,
    maxlength: 50
  },
  description: {
    type: String,
    maxlength: 200
  },
  targetDays: {
    type: Number,
    default: 30
  },
  completedDates: [{
    type: String // Store dates as YYYY-MM-DD strings
  }],
  currentStreak: {
    type: Number,
    default: 0
  },
  longestStreak: {
    type: Number,
    default: 0
  },
  category: {
    type: String,
    enum: ['Health', 'Productivity', 'Learning', 'Fitness', 'Mindfulness', 'Other'],
    default: 'Other'
  },
  color: {
    type: String,
    default: '#4F46E5'
  },
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

// Calculate completion percentage
habitSchema.virtual('completionPercentage').get(function() {
  return Math.round((this.completedDates.length / this.targetDays) * 100);
});

module.exports = mongoose.model('Habit', habitSchema);
