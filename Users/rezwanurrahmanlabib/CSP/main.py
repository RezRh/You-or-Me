import os
import json
import random
import requests
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import time
import tempfile

class YouOrMeGame:
    def __init__(self):
        self.api_key = ""
        self.score_you = 0
        self.score_me = 0
        self.favorite_questions = []
        self.questions_asked = []
        self.config_file = "config.json"
        self.favorites_file = "favorites.json"
        self.recognizer = sr.Recognizer()
        self.load_config()
        self.load_favorites()
    
    def load_config(self):
        """Load configuration from file if it exists"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.api_key = config.get("api_key", "")
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({"api_key": self.api_key}, f)
            print("Configuration saved successfully!")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def load_favorites(self):
        """Load favorite questions from file if it exists"""
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, 'r') as f:
                    self.favorite_questions = json.load(f)
            except Exception as e:
                print(f"Error loading favorites: {e}")
    
    def save_favorites(self):
        """Save favorite questions to file"""
        try:
            with open(self.favorites_file, 'w') as f:
                json.dump(self.favorite_questions, f)
            print("Favorites saved successfully!")
        except Exception as e:
            print(f"Error saving favorites: {e}")
    
    def setup_api_key(self):
        """Set up the OpenRouter API key"""
        print("\n=== API Key Setup ===")
        print("You need an OpenRouter API key to play this game.")
        print("Get one at: https://openrouter.ai/")
        
        if self.api_key:
            print(f"Current API key: {self.api_key[:5]}...{self.api_key[-5:]}")
            change = input("Do you want to change it? (y/n): ").lower()
            if change != 'y':
                return True
        
        self.api_key = input("Enter your OpenRouter API key: ").strip()
        if not self.api_key:
            print("API key is required to play the game.")
            return False
        
        self.save_config()
        return True
    
    def generate_question(self):
        """Generate a 'You or Me?' question using OpenRouter API"""
        if not self.api_key:
            print("API key not set. Please set up your API key first.")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "openai/gpt-3.5-turbo",  # You can change this to other models
                "messages": [
                    {"role": "system", "content": "You are a fun game assistant that generates 'You or Me?' questions. These are questions that ask the player to choose between themselves or another person based on various scenarios, traits, or preferences. Generate a single, concise question in the format 'Who is more likely to...' or 'Who would rather...' Make it fun, creative, and appropriate for all ages."},
                    {"role": "user", "content": "Generate a 'You or Me?' question."}
                ],
                "max_tokens": 100
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                question = response.json()["choices"][0]["message"]["content"].strip()
                self.questions_asked.append(question)
                return question
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error generating question: {e}")
            return None
    
    def text_to_speech(self, text):
        """Convert text to speech and play it"""
        try:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_filename = temp_file.name
            temp_file.close()
            
            # Generate speech
            tts = gTTS(text=text, lang='en')
            tts.save(temp_filename)
            
            # Play the speech
            playsound(temp_filename)
            
            # Clean up the temporary file
            os.unlink(temp_filename)
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            print(text)  # Fallback to displaying text
    
    def speech_to_text(self):
        """Convert speech to text"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5)
                print("Processing...")
                
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None
    
    def process_answer(self, question, answer):
        """Process the player's answer"""
        if answer in ["you", "me"]:
            if answer == "you":
                self.score_you += 1
                return "You chose 'You'! One point for 'You'."
            else:  # answer == "me"
                self.score_me += 1
                return "You chose 'Me'! One point for 'Me'."
        else:
            return "Invalid answer. Please say 'You' or 'Me'."
    
    def add_to_favorites(self, question):
        """Add a question to favorites"""
        if question and question not in self.favorite_questions:
            self.favorite_questions.append(question)
            self.save_favorites()
            return f"Added to favorites: {question}"
        return "Question already in favorites or invalid question."
    
    def display_favorites(self):
        """Display all favorite questions"""
        if not self.favorite_questions:
            return "You don't have any favorite questions yet."
        
        print("\n=== Your Favorite Questions ===")
        for i, question in enumerate(self.favorite_questions, 1):
            print(f"{i}. {question}")
        return "End of favorites list."
    
    def display_score(self):
        """Display the current score"""
        return f"Current Score - You: {self.score_you}, Me: {self.score_me}"
    
    def reset_score(self):
        """Reset the score"""
        self.score_you = 0
        self.score_me = 0
        return "Score has been reset."
    
    def play_round(self):
        """Play a single round of the game"""
        question = self.generate_question()
        if not question:
            return False
        
        print("\n" + question)
        self.text_to_speech(question)
        
        # Get player's answer
        print("Say 'You' or 'Me'...")
        answer = self.speech_to_text()
        
        if answer:
            result = self.process_answer(question, answer)
            print(result)
            self.text_to_speech(result)
            
            # Ask if they want to add to favorites
            print("\nDo you want to add this question to favorites? (yes/no)")
            self.text_to_speech("Do you want to add this question to favorites? Say yes or no.")
            fav_response = self.speech_to_text()
            
            if fav_response and fav_response.lower() in ["yes", "yeah", "yep", "sure"]:
                feedback = self.add_to_favorites(question)
                print(feedback)
                self.text_to_speech("Added to favorites.")
        
        return True
    
    def display_menu(self):
        """Display the game menu"""
        print("\n===== You or Me? Game =====")
        print("1. Play a round")
        print("2. Display score")
        print("3. Reset score")
        print("4. View favorite questions")
        print("5. Setup API key")
        print("6. Exit game")
        print("===========================\n")
    
    def run(self):
        """Run the game"""
        print("Welcome to 'You or Me?' Game!")
        self.text_to_speech("Welcome to You or Me Game!")
        
        if not self.api_key and not self.setup_api_key():
            print("Cannot continue without an API key. Exiting...")
            return
        
        while True:
            self.display_menu()
            self.text_to_speech("Please choose an option from the menu.")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == "1":
                self.play_round()
            elif choice == "2":
                result = self.display_score()
                print(result)
                self.text_to_speech(result)
            elif choice == "3":
                result = self.reset_score()
                print(result)
                self.text_to_speech(result)
            elif choice == "4":
                result = self.display_favorites()
                self.text_to_speech("Here are your favorite questions.")
            elif choice == "5":
                self.setup_api_key()
            elif choice == "6":
                print("Thank you for playing 'You or Me?' Game!")
                self.text_to_speech("Thank you for playing You or Me Game! Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                self.text_to_speech("Invalid choice. Please try again.")

if __name__ == "__main__":
    game = YouOrMeGame()
    game.run()