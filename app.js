const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({ message: 'Hello from Techcrush Node.js App running in Docker!', status: 'ok' });
});

app.get('/health', (req, res) => res.send('healthy'));

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`));
