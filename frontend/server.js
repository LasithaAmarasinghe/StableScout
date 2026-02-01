const express = require('express');
const cors = require('cors');
const axios = require('axios');
const path = require('path');
require('dotenv').config({ path: '../.env' });

const app = express();
const PORT = process.env.PORT || 3000;
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:5000';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// API Routes
app.post('/api/analyze', async (req, res) => {
    try {
        const { query } = req.body;
        
        if (!query) {
            return res.status(400).json({ error: 'Query is required' });
        }

        console.log(`Processing query: ${query}`);

        // Call Python backend
        const response = await axios.post(`${PYTHON_API_URL}/api/analyze`, {
            query: query
        }, {
            timeout: 60000 // 60 second timeout
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error calling Python API:', error.message);
        res.status(500).json({ 
            error: 'Failed to analyze query',
            details: error.response?.data || error.message
        });
    }
});

// Health check
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        timestamp: new Date().toISOString(),
        pythonApiUrl: PYTHON_API_URL
    });
});

// Serve frontend
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`🚀 StableScout Frontend Server running on http://localhost:${PORT}`);
    console.log(`🔗 Python API URL: ${PYTHON_API_URL}`);
    console.log(`📊 Ready to analyze stablecoin yields!`);
});
