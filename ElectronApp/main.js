// Main process for Electron shell
// - Starts Flask backend if not already running
// - Opens Electron BrowserWindow pointing to Flask URL
// - Handles Windows Squirrel installer events
// - Enforces single-instance behavior

const path = require('path');
const http = require('http');
const { app, BrowserWindow, dialog } = require('electron');
const { spawn } = require('child_process');

// Handle Squirrel events (Windows installer) early and quit
if (require('electron-squirrel-startup')) {
  app.quit();
}

const APP_ID = 'com.medimanage.app';
const FLASK_PORT = process.env.FLASK_PORT || 5000;
const FLASK_URL = process.env.FLASK_URL || `http://127.0.0.1:${FLASK_PORT}`;
let flaskProcess = null;

function waitForServer(url, timeoutMs = 20000, intervalMs = 500) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    const timer = setInterval(() => {
      http
        .get(url, () => {
          clearInterval(timer);
          resolve();
        })
        .on('error', () => {
          if (Date.now() - start > timeoutMs) {
            clearInterval(timer);
            reject(new Error('Server did not start in time'));
          }
        });
    }, intervalMs);
  });
}

function startFlask() {
  const projectRoot = path.resolve(__dirname, '..');
  const python = process.env.PYTHON || 'python';
  const scriptPath = path.join(projectRoot, 'main.py');

  const env = { ...process.env, FLASK_RUN_FROM_ELECTRON: '1' };

  const child = spawn(python, [scriptPath], {
    cwd: projectRoot,
    env,
    stdio: 'inherit',
  });

  child.on('exit', (code) => {
    console.log(`Flask process exited with code ${code}`);
  });

  return child;
}

async function createWindow() {
  // Start Flask only if not disabled and no custom URL is given
  if (!process.env.NO_FLASK && !process.env.FLASK_URL) {
    try {
      await waitForServer(FLASK_URL, 2000, 400);
      console.log('Flask already running.');
    } catch (_) {
      console.log('Starting Flask backend...');
      flaskProcess = startFlask();
      try {
        await waitForServer(FLASK_URL, 25000, 500);
      } catch (err) {
        dialog.showErrorBox('MediManage', 'Failed to start backend server.');
      }
    }
  }

  const iconPath = path.join(__dirname, 'icons', 'icon.ico');

  const mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
    },
    title: 'MediManage',
    icon: iconPath,
    show: true,
  });

  await mainWindow.loadURL(FLASK_URL);
}

// Ensure single instance
const gotLock = app.requestSingleInstanceLock();
if (!gotLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    const [win] = BrowserWindow.getAllWindows();
    if (win) {
      if (win.isMinimized()) win.restore();
      win.focus();
    }
  });
}

app.on('ready', () => {
  try { app.setAppUserModelId(APP_ID); } catch (_) {}
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  if (flaskProcess) {
    try {
      flaskProcess.kill();
    } catch (_) {}
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});