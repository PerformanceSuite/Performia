#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const sessionName = process.argv[2] || 'default';
const timestamp = new Date().toISOString();
const sessionDir = path.join(__dirname, '..');
const sessionFile = path.join(sessionDir, 'session.json');

const sessionData = {
    name: sessionName,
    started_at: timestamp,
    status: 'active',
    project: 'Performia',
    working_directory: path.resolve(path.join(__dirname, '..', '..'))
};

fs.writeFileSync(sessionFile, JSON.stringify(sessionData, null, 4));

console.log(`✅ Session '${sessionName}' started at ${timestamp}`);
console.log(`📁 Working directory: ${sessionData.working_directory}`);
console.log('');
console.log(`Session context saved to: ${sessionFile}`);