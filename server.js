const { log } = require('console');
const express = require('express');
const app = express();
const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');
const cron = require('node-cron');

const { parse } = require("csv-parse");


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
  res.sendFile('/public/index.html',{root:__dirname})
}





function postPage(req, res) {
 
  const newData = [req.body.a, req.body.b, req.body.day, req.body.month, req.body.year, req.body.hour];

  // Path to the CSV file
  const csvFilePath = path.join(__dirname, '/processing/data.csv'); // Update with your actual CSV file path

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




 // Create a nodemailer transporter with your email configuration
async function sendEmailWithLink(toEmail) {
 
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: 'shivangkaushal2324@gmail.com',
      pass: 'sgyu eidb uzav jytr',
    },
  });

  // Define the email options
  const mailOptions = {
    from: 'shivangkaushal2324@gmail.com',
    to: toEmail,
    subject: 'Link to Web Page',
    text: 'http://172.30.45.242:3000/rout',
  };


    // Send the email
    const info = await transporter.sendMail(mailOptions);
    console.log('Email sent: ' + info.response);
    return 'Email sent successfully.';
}


cron.schedule('0 7 * * *', () => {
  console.log('Running the task at 7:00 AM');
const path = "email.csv";

// Create a readstream
// Parse options: delimiter and start from line 1

fs.createReadStream(path)
  .pipe(parse({ delimiter: ",", from_line: 1 }))
  .on("data", function (row) {
    // executed for each row of data
   
    let date=row[3]
    const startDate = new Date(dateString.split('-').reverse().join('-'));
    const currentDate = new Date();
    const timeDifference = currentDate - startDate;
    const daysPassed = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    if(daysPassed>=90){
      sendEmailWithLink(row[2]);
      let day = currentDate.getDate().toString().padStart(2, '0');
      let month = (currentDate.getMonth() + 1).toString().padStart(2, '0'); // Month is zero-based
      let year = currentDate.getFullYear();
      row[3] = `${day}-${month}-${year}`;
    }
  })
 
  .on("end", function () {
    // executed when parsing is complete
    console.log("File read successful");
  });

});
