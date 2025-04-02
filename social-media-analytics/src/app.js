require("dotenv").config();
const express = require("express");
const axios = require("axios");

const app = express();
const PORT = 3000;

const BASE_URL = "http://20.244.56.144/evaluation-service";
const API_KEY = process.env.API_KEY || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQzNjAzOTc3LCJpYXQiOjE3NDM2MDM2NzcsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjUwMTdjMmE1LTg3MWUtNDlmMi04YzEzLTQyYjllNTgwOGUwZSIsInN1YiI6InNoYWhiaHVzaGFuNzNAZ21haWwuY29tIn0sImVtYWlsIjoic2hhaGJodXNoYW43M0BnbWFpbC5jb20iLCJuYW1lIjoiYmh1c2hhbiBzYWgiLCJyb2xsTm8iOiIyMjA1NDMyMSIsImFjY2Vzc0NvZGUiOiJud3B3cloiLCJjbGllbnRJRCI6IjUwMTdjMmE1LTg3MWUtNDlmMi04YzEzLTQyYjllNTgwOGUwZSIsImNsaWVudFNlY3JldCI6IlFUSHdNcXdhR1Zjcmp5cXEifQ.on2oYxaDy85tZhbuX-sdv5rP19dUNS7YQVJzytFmcDU"; 


const HEADERS = {
    headers: {
        Authorization: API_KEY
    }
};


app.get("/users", async (req, res) => {
    try {
        const response = await axios.get(`${BASE_URL}/users`, HEADERS);
        res.json(response.data);
    } catch (error) {
        console.error("Error fetching users:", error.response?.data || error.message);
        res.status(500).json({ error: "Failed to fetch users" });
    }
});


app.get("/users/:userId/posts", async (req, res) => {
    const { userId } = req.params;
    try {
        const response = await axios.get(`${BASE_URL}/users/${userId}/posts`, HEADERS);
        res.json(response.data);
    } catch (error) {
        console.error(`Error fetching posts for user ${userId}:`, error.response?.data || error.message);
        res.status(500).json({ error: "Failed to fetch user posts" });
    }
});


app.get("/posts/:postId/comments", async (req, res) => {
    const { postId } = req.params;
    try {
        const response = await axios.get(`${BASE_URL}/posts/${postId}/comments`, HEADERS);
        res.json(response.data);
    } catch (error) {
        console.error(`Error fetching comments for post ${postId}:`, error.response?.data || error.message);
        res.status(500).json({ error: "Failed to fetch comments" });
    }
});


app.listen(PORT, () => {
    console.log(`✅ Server running on port ${PORT}`);
});
