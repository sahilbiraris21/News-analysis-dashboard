const { google } = require('googleapis');
const path = require('path');
const fs = require('fs');
const credentials = require('../secrets/client_secret.json');

const readline = require('node:readline');
const { stdin: input, stdout: output } = require('node:process');

const rl = readline.createInterface({ input, output });
rl.question("Enter code: ", (code) => {
  const { client_secret, client_id, redirect_uris } = credentials.installed;
  const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

  oAuth2Client.getToken(code).then(({ tokens }) => {
    const tokenPath = path.join(__dirname, '../secrets/token.json');
    fs.writeFileSync(tokenPath, JSON.stringify(tokens));
    console.log('Access token and refresh token stored to token.json');
  });

  rl.close();
});