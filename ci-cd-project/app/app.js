const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello from CI/CD Pipeline!');
});

app.get('/health', (req, res) => {
    res.status(200).send('OK');
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`App running on port ${PORT}`);
});

