const axios = require('axios');
const FormData = require('form-data');
const { Buffer } = require('buffer');

async function sendLineNotifyImage(token, message, base64Image) {
    try {
        // Decode base64 to Buffer
        const decodedImage = Buffer.from(base64Image, 'base64');
        
        // Create a FormData instance
        const form = new FormData();
        form.append('message', message);
        form.append('imageFile', decodedImage, {
            filename: 'image.jpg',
            contentType: 'image/jpeg'
        });
        
        // Make POST request to LINE Notify
        const response = await axios.post('https://notify-api.line.me/api/notify', form, {
            headers: {
                ...form.getHeaders(),
                'Authorization': `Bearer ${token}`
            }
        });

        // Check the response
        const result = response.data;
        if (result.status === 200) {
            console.log('Notification sent successfully.');
            return { resultoutput: 'in_notisent' };
        } else {
            console.log('Error sending notification:', result);
            return { resultoutput: 'in_notierror' };
        }
    } catch (error) {
        console.error('Error:', error.message);
        return { resultoutput: 'in_notierror' };
    }
}

module.exports = sendLineNotifyImage;
