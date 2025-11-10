const { google } = require('googleapis');
const MailComposer = require('nodemailer/lib/mail-composer');
const credentials = require('../secrets/client_secret.json');
const tokens = require('../secrets/token.json');

const express = require("express");
const app = express();

var bodyParser = require('body-parser');
app.use(bodyParser.json());

const getGmailService = () => {
    const { client_secret, client_id, redirect_uris } = credentials.installed;
    const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
    oAuth2Client.setCredentials(tokens);
    const gmail = google.gmail({ version: 'v1', auth: oAuth2Client });
    return gmail;
};

const encodeMessage = (message) => {
    return Buffer.from(message).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
};

const createMail = async (options) => {
    const mailComposer = new MailComposer(options);
    const message = await mailComposer.compile().build();
    return encodeMessage(message);
};

const sendMail = async (options) => {
    const gmail = getGmailService();
    const rawMessage = await createMail(options);
    const { data: { id } = {} } = await gmail.users.messages.send({
    userId: 'me',
    resource: {
        raw: rawMessage,
    },
    });
    return id;
};

app.post("/sendmail", async (req, res) => {
    const { email } = req.body;

    const options =  {
        to: email,
        subject: "Your department sucks",
        html: `
        <div>
            <h1>Please look into your department, Wo bigad raha hai!!!</h1>
        </div>
        `,
        textEncoding: 'base64',
        headers: [
            { key: 'X-Application-Developer', value: 'Atish Shah' },
        ],
    };

    try {
        await sendMail(options);
    } catch(err) {
        console.log(err);
        res.status(500).send("error");
    }

    res.status(200).send("done");
})

app.listen(6969, () => {
    console.log('listening to send mails on port 6969')
})