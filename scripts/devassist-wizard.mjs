#!/usr/bin/env node

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { createInterface } from 'readline/promises';
import { stdin as input, stdout as output } from 'process';

const projectRoot = process.cwd();
const defaultProjectName = path.basename(projectRoot);
const moduleDir = path.dirname(fileURLToPath(import.meta.url));
const sharedDefaultAbs = process.env.DEVASSIST_SHARED_SERVER
  ? path.resolve(process.env.DEVASSIST_SHARED_SERVER)
  : path.resolve(projectRoot, '..', 'Custom_MCP', 'DevAssist', 'index.js');
const sharedDefaultRel = path.relative(projectRoot, sharedDefaultAbs) || './Custom_MCP/DevAssist/index.js';

const rl = createInterface({ input, output });

async function prompt(question, defaultValue) {
  const suffix = defaultValue !== undefined && defaultValue !== null && defaultValue !== ''
    ? ` [${defaultValue}]`
    : '';
  const answer = (await rl.question(`${question}${suffix}: `)).trim();
  return answer || defaultValue;
}

try {
  console.log('DevAssist Project Setup Wizard');
  console.log('--------------------------------');

  const projectName = await prompt('Project name', defaultProjectName);
  const sharedServerRel = await prompt('Shared DevAssist server path (relative or absolute)', sharedDefaultRel);
  const enableVizitrtrAnswer = (await prompt('Enable vizitrtr tool? (Y/n)', 'Y')).toLowerCase();
  const enableVizitrtr = enableVizitrtrAnswer !== 'n' && enableVizitrtrAnswer !== 'no';
  const defaultIterations = enableVizitrtr
    ? Number(await prompt('Default vizitrtr iterations', '3')) || 3
    : 3;

  const configDir = path.join(projectRoot, '.devassist');
  await fs.mkdir(configDir, { recursive: true });

  const config = {
    version: '1.0.0',
    sharedServer: sharedServerRel,
    project: {
      name: projectName,
      path: projectRoot
    },
    clients: ['codex', 'claude', 'llm'],
    technologies: [],
    tools: {
      vizitrtr: {
        enabled: enableVizitrtr,
        defaultIterations,
        backendEnv: 'VIZITRTR_API'
      }
    },
    consentLogging: {
      enabled: true,
      logDir: '.devassist/logs'
    },
    artifactStore: {
      path: '.devassist/data/artifacts'
    }
  };

  const configPath = path.join(configDir, 'config.json');
  await fs.writeFile(configPath, JSON.stringify(config, null, 2));
  console.log(`✔ Wrote ${path.relative(projectRoot, configPath)}`);

  const sharedFallback = sharedServerRel.replace(/\\/g, '\\\\');
  const launcherLines = [
    '#!/usr/bin/env node',
    '',
    "import fs from 'fs/promises';",
    "import path from 'path';",
    "import { fileURLToPath } from 'url';",
    '',
    'const __dirname = path.dirname(fileURLToPath(import.meta.url));',
    "const projectRoot = path.resolve(__dirname, '..');",
    "const configPath = path.join(__dirname, 'config.json');",
    '',
    'let config = {};',
    'try {',
    "  const raw = await fs.readFile(configPath, 'utf8');",
    '  config = JSON.parse(raw);',
    '} catch (error) {',
    "  console.error('[DevAssist Launcher] Unable to read config.json:', error.message);",
    '  process.exit(1);',
    '}',
    '',
    'const projectConfig = config.project || {};',
    'const resolvedProjectPath = projectConfig.path',
    '  ? path.resolve(projectConfig.path)',
    '  : projectRoot;',
    'const projectName = projectConfig.name || path.basename(resolvedProjectPath);',
    '',
    'process.env.PROJECT_ROOT = resolvedProjectPath;',
    'process.env.PROJECT_NAME = projectName;',
    'process.env.DEVASSIST_PROJECT = projectName;',
    'process.env.DEVASSIST_PROJECT_PATH = resolvedProjectPath;',
    "process.env.DEVASSIST_DATA_PATH = path.join(resolvedProjectPath, '.devassist', 'data');",
    '',
    'if (config.consentLogging?.enabled !== false) {',
    '  process.env.DEVASSIST_CONSENT_LOGS = config.consentLogging?.logDir',
    '    ? path.resolve(resolvedProjectPath, config.consentLogging.logDir)',
    "    : path.join(resolvedProjectPath, '.devassist', 'logs');",
    '}',
    '',
    'if (config.artifactStore?.path) {',
    '  process.env.DEVASSIST_ARTIFACT_PATH = path.resolve(resolvedProjectPath, config.artifactStore.path);',
    '}',
    '',
    'if (config.tools?.vizitrtr?.enabled) {',
    "  process.env.DEVASSIST_ENABLE_VIZITRTR = 'true';",
    '  if (config.tools.vizitrtr.defaultIterations != null) {',
    '    process.env.VIZITRTR_DEFAULT_ITERATIONS = String(config.tools.vizitrtr.defaultIterations);',
    '  }',
    '  if (config.tools.vizitrtr.backendEnv) {',
    '    process.env.VIZITRTR_BACKEND_ENV = config.tools.vizitrtr.backendEnv;',
    '  }',
    '}',
    '',
    `const sharedField = config.sharedServer || '${sharedFallback}';`,
    'const sharedPath = path.isAbsolute(sharedField)',
    '  ? sharedField',
    '  : path.resolve(resolvedProjectPath, sharedField);',
    '',
    'try {',
    '  await import(sharedPath);',
    '} catch (error) {',
    '  console.error(`[DevAssist Launcher] Failed to load shared server at ${sharedPath}:`, error);',
    '  process.exit(1);',
    '}',
    ''
  ];

  const launcherPath = path.join(configDir, 'devassist-launcher.mjs');
  await fs.writeFile(launcherPath, launcherLines.join('\n'));
  await fs.chmod(launcherPath, 0o755);
  console.log(`✔ Wrote ${path.relative(projectRoot, launcherPath)}`);

  const shimPath = path.join(projectRoot, 'devassist');
  const shimContents = [
    '#!/bin/sh',
    'SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"',
    'node "$SCRIPT_DIR/.devassist/devassist-launcher.mjs" "$@"',
    ''
  ].join('\n');
  await fs.writeFile(shimPath, shimContents);
  await fs.chmod(shimPath, 0o755);
  console.log(`✔ Wrote ${path.relative(projectRoot, shimPath)}`);

  const launcherAbs = path.join(projectRoot, '.devassist', 'devassist-launcher.mjs');
  const clientsManifest = {
    version: 1,
    generatedAt: new Date().toISOString(),
    clients: {
      codex: {
        displayName: 'Codex',
        entrypoint: {
          command: 'node',
          args: [launcherAbs]
        },
        scopes: ['tools', 'filesystem', 'network'],
        notes: 'Add to Codex MCP profile to expose the DevAssist tool palette.'
      },
      claude: {
        displayName: 'Claude',
        entrypoint: {
          command: 'node',
          args: [launcherAbs]
        },
        configPath: '~/Library/Application Support/Claude/claude_desktop_config.json',
        scopes: ['tools', 'filesystem', 'network'],
        notes: 'Matches Claude Desktop MCP expectations; keep command in sync with Codex.'
      },
      llm: {
        displayName: 'Dev-workflow LLM CLI',
        entrypoint: {
          command: 'node',
          args: [launcherAbs]
        },
        prerequisites: ['Dev-workflow proxy running', 'Docker compose stack up'],
        scopes: ['tools', 'filesystem', 'network'],
        notes: 'Alias exposed as `llm`; shares the shared DevAssist launcher.'
      }
    }
  };

  const clientsPath = path.join(configDir, 'clients.json');
  await fs.writeFile(clientsPath, JSON.stringify(clientsManifest, null, 2));
  console.log(`✔ Wrote ${path.relative(projectRoot, clientsPath)}`);

  console.log('\nAll set! Add the launcher to your MCP clients using the paths above.');
} catch (error) {
  console.error('Wizard failed:', error);
  process.exitCode = 1;
} finally {
  await rl.close();
}
