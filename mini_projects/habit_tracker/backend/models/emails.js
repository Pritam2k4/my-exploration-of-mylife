const mongoose = require('mongoose');

const emailSchema = new mongoose.Schema(
  {
    address: { type: String, required: true, unique: true, lowercase: true }
  },
  { timestamps: true }
);

module.exports = mongoose.model('Email', emailSchema);
