# Dutch Learning Telegram Bot

A Telegram bot designed to help Egyptian learners master Dutch through interactive lessons, quizzes, and speech practice.

## Features

- Interactive lessons with CEFR levels (A1, A2, B1)
- Quiz system with multiple formats
- Speech recognition for pronunciation practice
- Progress tracking and gamification
- Arabic language support
- Admin panel for content management

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

4. Set up the database:
   ```bash
   alembic upgrade head
   ```

5. Run the bot:
   ```bash
   python bot.py
   ```

## Project Structure

- `bot.py`: Main bot logic and command handlers
- `models.py`: SQLAlchemy database models
- `database.py`: Database connection setup
- `config.py`: Configuration management
- `alembic/`: Database migrations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT