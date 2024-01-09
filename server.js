const { log } = require('console');
const express = require('express');
const app = express();
const fs = require('fs');
const path = require('path');



app.use(express.json());

app.listen(3000, () => {
  console.log('Server is listening on port 3000');
});

const userRout=express.Router();
app.use('/rout',userRout)

userRout.route('/')
 .get(getPage)
 .post(postPage);

function getPage(req,res){
  res.sendFile('index.html',{root:__dirname})
}





function postPage(req, res) {
  // Get the 5 variables from the request body
  
 
 
  const newData = [req.body.a, req.body.b, req.body.day, req.body.month, req.body.year, req.body.hour];

  // Path to the CSV file
  const csvFilePath = path.join(__dirname, 'data.csv'); // Update with your actual CSV file path

  // Read the existing content of the CSV file
  fs.readFile(csvFilePath, 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: 'Error reading CSV file.' });
    }

    // Split the existing content into rows
    const rows = data.split('\n');

    // Add a new row with the data
    const newRow = newData.join(',') + '\n';

    // Add the new row to the existing content
    const updatedContent = `${data.trim()}\n${newRow}`;

    // Write the updated content back to the CSV file
    fs.writeFile(csvFilePath, updatedContent, 'utf8', (err) => {
      if (err) {
        console.error(err);
        return res.status(500).json({ error: 'Error writing to CSV file.' });
      }

      console.log('Data added to CSV file successfully.');

      // Respond with a JSON message
      res.json({
        message: 'Data added to CSV file successfully.',
      });
    });
  });
}

