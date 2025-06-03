const express = require('express');
const app = express();
const port = process.env.PORT || 4000;

app.get('/', (req, res) => {
  res.send('Telegram bot server is running.');
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
