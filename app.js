const express = require('express')
const fs = require("fs");
const os = require('os')

const app = express()
const port = 5000

app.use(express.static('public'));

app.get('/', (req, res) => {
  res.render('index')
})

app.post('/', (req, res) => {
  fs.readFile(os.homedir() + "/system_data_readings.txt", (err, data) => {
    if (err) {
      console.log("error reading file")
      res.send({"result": "error"})
      return
    }

    res.send({"result": JSON.parse(data.toString())});
  });
})

app.listen(port, () => console.log(`App listening on port ${port}`))
