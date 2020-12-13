var fs = require("fs");
var request = require("request");
var cheerio = require("cheerio");

url = "https://www.mohfw.gov.in/";

request(url, function(error, response, html) {
  if (!error) {
    var $ = cheerio.load(html);

    var states = [];

    $("body > div.main-section > div > div > div.contribution > div.content.newtab > div > table > tbody > tr").each(function() {
      let row = $(this);
      let td = row.children(); //.eq(1).text())
      states.push({
        state: td.eq(1).text(),
        confirmed: td.eq(2).text(),
        deaths: td.eq(5).text(),
        recovered: td.eq(4).text()
      });
    });
  }
  

  // To write to the system we will use the built in 'fs' library.
  // In this example we will pass 3 parameters to the writeFile function
  // Parameter 1 :  output.json - this is what the created filename will be called
  // Parameter 2 :  JSON.stringify(json, null, 4) - the data to write, here we do an extra step by calling JSON.stringify to make our JSON easier to read
  // Parameter 3 :  callback function - a callback function to let us know the status of our function

  fs.writeFile("output.json", JSON.stringify(states, null, 4), function(err) {
    console.log("File successfully written in output.json file");
  });

});

// 
