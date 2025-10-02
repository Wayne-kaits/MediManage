# MediManage Electron Shell

This Electron app wraps the existing Flask web app and provides a desktop-like experience.

## Prerequisites
- Node.js 18+
- Python 3.11+
- Project Python deps installed: `pip install -r d:\Softwares\MediManage\requirements.txt`

## Development
1. Install Node deps:
   ```bash
   npm install
   ```
2. Start Electron (will attempt to start Flask backend if not already running):
   ```bash
   npm run start
   ```

If you want to run Flask yourself (for logs/hot reload), in another terminal:
```bash
python d:\Softwares\MediManage\main.py
set NO_FLASK=1
npm run start
```

## Packaging (Windows)
```bash
npm run dist
```
Artifacts will be in `ElectronApp/dist`.

## Config
- Set `FLASK_PORT` to change backend port (default 5000).
- Set `FLASK_URL` to point Electron to an already-running server.
- Set `PYTHON` to a specific Python executable if needed.