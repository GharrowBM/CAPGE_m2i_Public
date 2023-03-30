const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const app = express();
const upload = multer({ dest: '/app/uploads' });

app.use(express.static('public'));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/upload', upload.single('file'), (req, res) => {
  res.json({ filename: req.file.filename });
});

app.get('/uploads', (req, res) => {
  const dirPath = path.join(__dirname, 'uploads');
  fs.readdir(dirPath, (err, files) => {
    if (err) {
      console.error(err);
      res.status(500).send('Server error');
    } else {
      res.json(files);
    }
  });
});

app.get('/uploads/:filename', (req, res) => {
  const { filename } = req.params;
  const filePath = path.join('/app/uploads', filename);
  const exists = fs.existsSync(filePath);
  if (exists) {
    res.sendFile(filePath);
  } else {
    res.status(404).send('File not found');
  }
});

const port = process.env.PORT || 3000;

app.listen(port, () => console.log(`App listening on port ${port}!`));
