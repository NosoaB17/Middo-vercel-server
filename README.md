# Middo-vercel-server

This is a Flask-based translation server deployed on Vercel.

## Features

- Text translation
- Language detection
- Text-to-speech conversion

## Deployment

This server is configured to be deployed on Vercel. Follow these steps:

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the project directory
3. Follow the prompts to deploy

## API Endpoints

- `/translate` (POST): Translate text
- `/languages` (GET): Get list of supported languages
- `/tts` (GET): Convert text to speech
