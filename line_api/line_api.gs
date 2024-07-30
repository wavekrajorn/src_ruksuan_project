function sendLineNotify(token, message) {
  var options = {
    "Method": "POST",
    "payload": {"message": message},
    "headers": {"Authorization" : "Bearer " + token}
  }
  var response = UrlFetchApp.fetch("https://notify-api.line.me/api/notify", options)
  response = response.getContentText()
  var result = JSON.parse(response)

  if (result['status'] == 200) {
    res = {}
    res['resultoutput'] = 'in_notisent'
    Logger.log('ok')
  }
  else {
    res = {}
    res['resultoutput'] = 'in_notierror'
  }
  Logger.log(res)
  return res
}
function doGet(request) {
    var tokenID = request.parameters.tokenID // <<<<< SEND FROM parameters
    // var message = request.parameters.message
    var message = "เด็กหายไปจากเตียงแล้ว ไปดูด่วน!!"
    var date_time = new Date()
    message = "\n⚠️ " + message + "\n🕒 เวลา: " + date_time
    var result = sendLineNotify(tokenID, message)
    result = JSON.stringify(message);
    return ContentService.createTextOutput(result).setMimeType(ContentService.MimeType.JSON);
}


// Craft By : Vish Siriwatana