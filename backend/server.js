const express = require('express');
const cors = require('cors');
const multer = require('multer');
const sql = require('mssql');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Upload configuration
const upload = multer({ dest: 'uploads/' });

// Route for image upload
app.post('/upload', upload.single('image'), (req, res) => {
    if (!req.file) return res.status(400).send("No file uploaded.");
    res.send({ message: "File uploaded successfully", filename: req.file.filename });
});

app.listen(5000, () => console.log("Server running on port 5000"));
