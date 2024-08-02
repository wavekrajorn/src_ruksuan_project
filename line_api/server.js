const express = require('express');
const bodyParser = require('body-parser');
const sendLineNotifyImage = require('./sendLineNotifyImage');
const sendLineNotify = require("./sendLineNotify");
const tokenID = "1OUFRqDMJWFx9WZHo2uBV16cQeDtGlefDEmPMS8Llr4";
const app = express();
const port = process.env.PORT || 3000;

// Middleware to parse JSON request bodies
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/notifyPeople', async (req, res) => {
    
    const message = "🤷‍♂️ พบบุคคล ต้องส่งสัยรีบกลับบ้านโดยทันที";
    const base64Image = req.body.image64; // Base64 image string from request

    const date_time = new Date();
    const messageWithTimestamp = `\n${message}\n\n🕒 เวลา: ${date_time}`;

    const result = await sendLineNotifyImage(tokenID, messageWithTimestamp, base64Image);
    res.json(result);
});
app.post('/notifyFire', async (req, res) => {
    const message = "🔥 ตรวจพบเปลวเพลิงลุกไหม้ รีบตรวจสอบโดยด่วน";

    const date_time = new Date();
    const messageWithTimestamp = `\n${message}\n\n🕒 เวลา: ${date_time}`;

    const result = await sendLineNotify(tokenID, messageWithTimestamp);
    res.json(result);
});

app.post('/notifyGas', async (req, res) => {
    const message = "⛽ ตรวจพบความผิดปกติของอากาศ รีบตรวจสอบโดยด่วน";

    const date_time = new Date();
    const messageWithTimestamp = `\n${message}\n\n🕒 เวลา: ${date_time}`;

    const result = await sendLineNotify(tokenID, messageWithTimestamp);
    res.json(result);
});

app.post('/notifyQuake', async (req, res) => {
    const message = "😵‍💫 ตรวจพบการสั่นไหว รีบตรวจสอบโดยด่วน";

    const date_time = new Date();
    const messageWithTimestamp = `\n${message}\n\n🕒 เวลา: ${date_time}`;

    const result = await sendLineNotify(tokenID, messageWithTimestamp);
    res.json(result);
});


app.post('/notifyWaterLow', async (req, res) => {
    const message = "💦 ตรวจพบน้ำท่วมปริมาณ \"น้อย\" ไม่ต้องรีบกลับไปโดยทันที!!";

    const date_time = new Date();
    const messageWithTimestamp = `\n${message}\n\n🕒 เวลา: ${date_time}`;

    const result = await sendLineNotify(tokenID, messageWithTimestamp);
    res.json(result);
});

app.post('/notifyWaterHigh', async (req, res) => {
    const message = "💦 ตรวจพบน้ำท่วมปริมาณ \"มาก\" รีบกลับไปโดยทันที!!";

    const date_time = new Date();
    const messageWithTimestamp = `\n${message}\n\n🕒 เวลา: ${date_time}`;

    const result = await sendLineNotify(tokenID, messageWithTimestamp);
    res.json(result);
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});