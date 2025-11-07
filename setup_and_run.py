#!/usr/bin/env python3
"""
MachDatum RAG Chatbot Setup and Runner
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def create_database():
    """Create the RAG database"""
    print("\nCreating RAG database from document...")
    try:
        subprocess.check_call([sys.executable, "create_database.py"])
        print("✓ RAG database created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating database: {e}")
        return False
    return True

def run_chatbot():
    """Run the chatbot application"""
    print("\nStarting RAG chatbot...")
    print("Choose how to run the chatbot:")
    print("1. Web Interface (Flask app)")
    print("2. Command Line Interface")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting web application...")
        print("Open your browser and go to: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        try:
            subprocess.check_call([sys.executable, "app.py"])
        except KeyboardInterrupt:
            print("\n👋 Web server stopped!")
    elif choice == "2":
        print("\n🚀 Starting command line chatbot...")
        try:
            subprocess.check_call([sys.executable, "rag_chatbot.py"])
        except KeyboardInterrupt:
            print("\n👋 Chatbot stopped!")
    else:
        print("❌ Invalid choice. Please run again and select 1 or 2.")

def main():
    """Main setup and run function"""
    print("=== MachDatum RAG Chatbot Setup ===")
    print()
    
    # Check if document exists
    if not os.path.exists("MachDatum Details.docx"):
        print("❌ Error: 'MachDatum Details.docx' not found in current directory!")
        print("Please make sure the document is in the same folder as this script.")
        return
    
    # Step 1: Install dependencies
    if not install_dependencies():
        return
    
    # Step 2: Create database (only if it doesn't exist or if user wants to recreate)
    if os.path.exists("machdatum_rag_db.json"):
        recreate = input("\nRAG database already exists. Recreate it? (y/n): ").strip().lower()
        if recreate == 'y':
            if not create_database():
                return
        else:
            print("✓ Using existing RAG database")
    else:
        if not create_database():
            return
    
    # Step 3: Run chatbot
    run_chatbot()

if __name__ == "__main__":
    main()