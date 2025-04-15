# Mobile App Conversion Plan for 'You or Me?' Game

## Overview
This document outlines the plan to convert the existing Python-based 'You or Me?' game into a cross-platform mobile application using Flutter.

## Current Application Analysis

The current application is a Python-based game with the following features:
- OpenRouter API integration for generating 'You or Me?' questions
- Text-to-speech functionality using gTTS
- Speech-to-text functionality using SpeechRecognition
- Score tracking for 'You' and 'Me' responses
- Favorites system to save preferred questions
- Configuration management for API keys

## Mobile App Technology Stack

### Framework
- **Flutter**: Cross-platform framework for building native mobile applications for iOS and Android from a single codebase

### Key Packages
- **http**: For API requests to OpenRouter (replacing Python's requests)
- **flutter_tts**: For text-to-speech functionality (replacing gTTS)
- **speech_to_text**: For speech recognition (replacing SpeechRecognition)
- **shared_preferences**: For storing API keys and configuration (replacing JSON file storage)
- **sqflite**: For local database to store favorites and game history
- **flutter_dotenv**: For environment variable management (API keys)
- **provider** or **flutter_bloc**: For state management

## Implementation Plan

### 1. Project Setup
- Create a new Flutter project
- Set up the project structure following Flutter best practices
- Configure environment variables for API keys

### 2. Core Functionality Implementation
- Create API service for OpenRouter integration
- Implement text-to-speech functionality
- Implement speech-to-text functionality
- Create data models for questions, scores, and favorites
- Implement local storage for favorites and configuration

### 3. UI Implementation
- Design mobile-friendly UI with Material Design or Cupertino widgets
- Create screens for:
  - Game play
  - Score display
  - Favorites management
  - Settings (API key configuration)
- Implement responsive design for different screen sizes

### 4. Testing
- Unit tests for core functionality
- Widget tests for UI components
- Integration tests for full app flow
- Manual testing on iOS and Android devices

### 5. Deployment
- Configure app signing for both platforms
- Prepare app store assets (icons, screenshots, descriptions)
- Submit to Apple App Store and Google Play Store

## Migration Considerations

### API Integration
- The OpenRouter API integration will remain largely the same, but implemented using Flutter's http package
- API key storage will use secure storage methods appropriate for mobile platforms

### Speech Features
- Mobile platforms have native speech recognition capabilities that may offer better performance than the current Python implementation
- Text-to-speech will use platform-specific implementations through Flutter packages

### Data Storage
- Favorites will be stored in a local SQLite database using sqflite instead of JSON files
- Configuration will use SharedPreferences for simple key-value storage

### User Interface
- The current command-line interface will be replaced with a touch-friendly GUI
- Voice commands will be supplemented with touch controls for accessibility

## Timeline Estimate
- Project setup and core functionality: 2 weeks
- UI implementation: 2 weeks
- Testing and refinement: 1 week
- Deployment preparation: 1 week

Total estimated time: 6 weeks for initial release