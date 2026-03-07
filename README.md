# MagicEdit AI: Professional Creative Suite

MagicEdit AI is a cutting-edge web application providing professional-grade AI tools for creators. Built with a focus on speed, precision, and aesthetics, it offers advanced generative features and surgical background removal.

## ✨ Features

- **Latent Emoji Forge**: Generate unique, high-fidelity emojis using customized latent diffusion models.
- **Neural Background Removal**: Segment subjects from complex backgrounds with neural accuracy in seconds.
- **Premium Interface**: A modern, glassmorphic dark-theme UI with fluid animations and responsive design.
- **Session History**: Track and manage your creative output throughout your session.

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **AI/ML**: PyTorch, TorchVision
- **Frontend**: Vanilla JS, CSS3, HTML5 (Jinja2 Templates)
- **Data/Storage**: AWS S3 integration
- **Packaging**: astral-sh/uv

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) installed

### Installation

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd PhotoShop
   ```

2. Sync dependencies:

   ```bash
   uv sync
   ```

3. Run the application:
   ```bash
   uv run main.py
   ```
   The app will be available at `http://localhost:8000`.

## 🐳 Docker Deployment

You can run the entire suite using Docker:

```bash
docker build -t magicedit-ai .
docker run -p 8000:8000 magicedit-ai
```

## 📂 Project Structure

- `src/`: Core logic, models, and API routes.
- `static/`: Premium CSS, JS, and global styles.
- `templates/`: Jinja2 HTML templates for the frontend.
- `models/`: Local storage for transient model weights.
