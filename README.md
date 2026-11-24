# Image De-raining Web Application

A three-service application that removes rain streaks from uploaded images using directional discrete Fourier transform (DFT) filtering and edge sharpening.

## Architecture

- React client: port 3000
- Express API: port 5000
- FastAPI image processor: port 8000
- Optional MongoDB database for persistent processing history. Without it, the Express API stores the latest 50 entries locally in `server/history.json`.

## Run locally

Prerequisites: Python 3.8+ and Node.js 16+.

Open three terminals from the project root:

```bash
cd backend/api
python -m venv venv
# Windows: venv\\Scripts\\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python main.py
```

```bash
cd server
npm install
npm start
```

```bash
cd client
npm install
npm start
```

Then visit `http://localhost:3000`.

## Configuration

The Express server works with no configuration. To use MongoDB or point it at a non-default FastAPI instance, create `server/.env`:

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/derain_app
FASTAPI_URL=http://localhost:8000
```

For a separately deployed Express API, set `REACT_APP_API_URL` before starting or building the client.

## Project layout

```text
backend/api/       FastAPI DFT processor
server/            Express upload, history, and proxy API
client/            React interface
Reports/           Project report and original research code
```

## Notes

- Supported uploads are PNG, JPEG, and WebP up to 10 MB.
- The application is DFT-based and does not require model weights or TensorFlow.
- The `start-*.bat` files are optional Windows launch helpers.
