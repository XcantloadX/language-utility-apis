const express = require('express');
const ojad = require('./ojad');
const app = express();
 
app.get('/', function (req, res) {
   res.send('Hello World');
})

app.get('/ojad/verb_conjugations', function(req, res) {
  const {word} = req.query;
  console.log(word);
  ojad.verb_conjugations(word).then(ret => res.send(JSON.stringify(ret)));
});
 
var server = app.listen(8081, function () {
 
  var host = server.address().address
  var port = server.address().port
 
  console.log("应用实例，访问地址为 http://%s:%s", host, port)
 
})