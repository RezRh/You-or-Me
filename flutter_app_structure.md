# Flutter App Structure for 'You or Me?' Game

This document outlines the proposed Flutter project structure and key implementation details for converting the Python-based 'You or Me?' game to a mobile application.

## Project Structure

```
you_or_me/
├── android/                 # Android-specific files
├── ios/                     # iOS-specific files
├── lib/
│   ├── main.dart            # Entry point of the application
│   ├── config/
│   │   ├── env.dart         # Environment configuration
│   │   └── theme.dart       # App theme configuration
│   ├── models/
│   │   ├── question.dart    # Question data model
│   │   └── score.dart       # Score data model
│   ├── screens/
│   │   ├── home_screen.dart # Main menu screen
│   │   ├── game_screen.dart # Game play screen
│   │   ├── favorites_screen.dart # Favorites management screen
│   │   └── settings_screen.dart  # Settings screen
│   ├── services/
│   │   ├── api_service.dart      # OpenRouter API integration
│   │   ├── speech_service.dart   # Text-to-speech and speech-to-text
│   │   └── storage_service.dart  # Local storage for favorites and settings
│   ├── providers/
│   │   ├── game_provider.dart    # Game state management
│   │   └── settings_provider.dart # App settings state management
│   └── widgets/
│       ├── question_card.dart    # Question display widget
│       ├── voice_button.dart     # Voice input button
│       └── score_display.dart    # Score display widget
├── assets/
│   ├── images/                   # App images and icons
│   └── sounds/                   # Sound effects
├── pubspec.yaml                  # Dependencies and app metadata
└── README.md                     # Project documentation
```

## Key Implementation Details

### 1. API Integration (api_service.dart)

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiService {
  final String baseUrl = 'https://openrouter.ai/api/v1/chat/completions';
  String? apiKey;
  
  Future<void> initialize() async {
    apiKey = dotenv.env['OPENROUTER_API_KEY'];
  }
  
  Future<String?> generateQuestion() async {
    if (apiKey == null) return null;
    
    try {
      final response = await http.post(
        Uri.parse(baseUrl),
        headers: {
          'Authorization': 'Bearer $apiKey',
          'Content-Type': 'application/json'
        },
        body: jsonEncode({
          'model': 'openai/gpt-3.5-turbo',
          'messages': [
            {
              'role': 'system',
              'content': 'You are a fun game assistant that generates \'You or Me?\' questions. These are questions that ask the player to choose between themselves or another person based on various scenarios, traits, or preferences. Generate a single, concise question in the format \'Who is more likely to...\' or \'Who would rather...\' Make it fun, creative, and appropriate for all ages.'
            },
            {
              'role': 'user',
              'content': 'Generate a \'You or Me?\' question.'
            }
          ],
          'max_tokens': 100
        }),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['choices'][0]['message']['content'].toString().trim();
      }
      return null;
    } catch (e) {
      print('Error generating question: $e');
      return null;
    }
  }
}
```

### 2. Speech Services (speech_service.dart)

```dart
import 'package:flutter_tts/flutter_tts.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

class SpeechService {
  final FlutterTts flutterTts = FlutterTts();
  final stt.SpeechToText speech = stt.SpeechToText();
  bool isListening = false;
  
  Future<void> initialize() async {
    await flutterTts.setLanguage('en-US');
    await speech.initialize();
  }
  
  Future<void> speak(String text) async {
    await flutterTts.speak(text);
  }
  
  Future<String?> listen() async {
    if (!isListening) {
      isListening = true;
      
      bool available = await speech.initialize();
      if (available) {
        await speech.listen(
          onResult: (result) {
            isListening = false;
            if (result.finalResult) {
              return result.recognizedWords.toLowerCase();
            }
          },
        );
        
        // Set a timeout
        await Future.delayed(Duration(seconds: 5));
        if (isListening) {
          speech.stop();
          isListening = false;
        }
      }
    }
    return null;
  }
}
```

### 3. Storage Service (storage_service.dart)

```dart
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/question.dart';

class StorageService {
  late Database database;
  late SharedPreferences prefs;
  
  Future<void> initialize() async {
    // Initialize shared preferences for settings
    prefs = await SharedPreferences.getInstance();
    
    // Initialize SQLite database for favorites
    final databasePath = await getDatabasesPath();
    final path = join(databasePath, 'you_or_me.db');
    
    database = await openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        await db.execute(
          'CREATE TABLE favorites(id INTEGER PRIMARY KEY, question TEXT)'
        );
      }
    );
  }
  
  // API Key methods
  Future<void> saveApiKey(String apiKey) async {
    await prefs.setString('api_key', apiKey);
  }
  
  String? getApiKey() {
    return prefs.getString('api_key');
  }
  
  // Score methods
  Future<void> saveScore(int youScore, int meScore) async {
    await prefs.setInt('you_score', youScore);
    await prefs.setInt('me_score', meScore);
  }
  
  int getYouScore() {
    return prefs.getInt('you_score') ?? 0;
  }
  
  int getMeScore() {
    return prefs.getInt('me_score') ?? 0;
  }
  
  // Favorites methods
  Future<void> addFavorite(String question) async {
    await database.insert(
      'favorites',
      {'question': question},
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }
  
  Future<List<Question>> getFavorites() async {
    final List<Map<String, dynamic>> maps = await database.query('favorites');
    
    return List.generate(maps.length, (i) {
      return Question(
        id: maps[i]['id'],
        text: maps[i]['question'],
      );
    });
  }
}
```

### 4. Main Game Screen (game_screen.dart)

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/game_provider.dart';
import '../widgets/question_card.dart';
import '../widgets/voice_button.dart';
import '../widgets/score_display.dart';

class GameScreen extends StatefulWidget {
  @override
  _GameScreenState createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  bool isLoading = false;
  String? currentQuestion;
  
  @override
  void initState() {
    super.initState();
    _generateQuestion();
  }
  
  Future<void> _generateQuestion() async {
    setState(() {
      isLoading = true;
    });
    
    final gameProvider = Provider.of<GameProvider>(context, listen: false);
    final question = await gameProvider.generateQuestion();
    
    setState(() {
      currentQuestion = question;
      isLoading = false;
    });
    
    if (question != null) {
      gameProvider.speakText(question);
    }
  }
  
  void _processAnswer(String answer) {
    if (currentQuestion == null) return;
    
    final gameProvider = Provider.of<GameProvider>(context, listen: false);
    gameProvider.processAnswer(answer);
    
    // Show dialog to add to favorites
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Add to Favorites?'),
        content: Text('Do you want to add this question to your favorites?'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              _generateQuestion();
            },
            child: Text('No'),
          ),
          TextButton(
            onPressed: () {
              gameProvider.addToFavorites(currentQuestion!);
              Navigator.of(context).pop();
              _generateQuestion();
            },
            child: Text('Yes'),
          ),
        ],
      ),
    );
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('You or Me?'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ScoreDisplay(),
            SizedBox(height: 40),
            if (isLoading)
              CircularProgressIndicator()
            else if (currentQuestion != null)
              QuestionCard(question: currentQuestion!),
            SizedBox(height: 40),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: () => _processAnswer('you'),
                  child: Text('YOU', style: TextStyle(fontSize: 20)),
                  style: ElevatedButton.styleFrom(
                    padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                  ),
                ),
                ElevatedButton(
                  onPressed: () => _processAnswer('me'),
                  child: Text('ME', style: TextStyle(fontSize: 20)),
                  style: ElevatedButton.styleFrom(
                    padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                  ),
                ),
              ],
            ),
            SizedBox(height: 20),
            VoiceButton(onResult: _processAnswer),
          ],
        ),
      ),
    );
  }
}
```

## Dependencies (pubspec.yaml)

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^0.13.5
  flutter_tts: ^3.6.3
  speech_to_text: ^6.1.1
  shared_preferences: ^2.1.0
  sqflite: ^2.2.6
  path: ^1.8.2
  provider: ^6.0.5
  flutter_dotenv: ^5.0.2
```

## Next Steps

1. Set up a Flutter development environment
2. Create the project structure as outlined above
3. Implement the core services (API, speech, storage)
4. Build the UI components and screens
5. Test on both Android and iOS devices
6. Prepare for app store submission