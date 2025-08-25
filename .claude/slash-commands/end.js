#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const sessionDir = path.join(__dirname, '..');
const sessionFile = path.join(sessionDir, 'session.json');
const archiveDir = path.join(sessionDir, 'archives');

if (!fs.existsSync(sessionFile)) {
    console.log('❌ No active session found');
    process.exit(1);
}

const sessionData = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
const timestamp = new Date().toISOString();

sessionData.status = 'completed';
sessionData.ended_at = timestamp;

if (!fs.existsSync(archiveDir)) {
    fs.mkdirSync(archiveDir, { recursive: true });
}

const archiveFileName = `session_${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
const archiveFile = path.join(archiveDir, archiveFileName);

fs.writeFileSync(archiveFile, JSON.stringify(sessionData, null, 4));
fs.unlinkSync(sessionFile);

console.log(`✅ Session '${sessionData.name}' ended at ${timestamp}`);
console.log(`📁 Session archived to: ${archiveFile}`);
console.log('');
console.log(`Session started: ${sessionData.started_at}`);
console.log(`Session ended:   ${timestamp}`);