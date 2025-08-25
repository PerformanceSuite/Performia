#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const sessionDir = path.join(__dirname, '..');
const sessionFile = path.join(sessionDir, 'session.json');

if (fs.existsSync(sessionFile)) {
    const sessionData = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
    console.log('📊 Active Session Status:');
    console.log('========================');
    console.log(JSON.stringify(sessionData, null, 4));
} else {
    console.log('❌ No active session');
    console.log('');
    console.log("Use '/start [session-name]' to begin a new session");
}