#!/usr/bin/env python3
"""
Complete MachDatum RAG Chatbot Setup and Runner
Includes both Simple RAG (working) and Gemini API (experimental) versions
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        packages = [
            "python-docx",
            "sentence-transformers", 
            "scikit-learn",
            "numpy",
            "flask",
            "flask-cors",
            "python-dotenv",
            "google-generativeai"
        ]
        
        for package in packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                capture_output=True, text=True)
        
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def create_database():
    """Create the RAG database"""
    print("\n📄 Creating RAG database from document...")
    try:
        if os.path.exists("machdatum_rag_db.json"):
            print("Database already exists!")
            recreate = input("Recreate database? (y/n): ").strip().lower()
            if recreate != 'y':
                print("✅ Using existing RAG database")
                return True
        
        subprocess.check_call([sys.executable, "create_database.py"])
        print("✅ RAG database created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating database: {e}")
        return False
    return True

def test_chatbot():
    """Test the chatbot functionality"""
    print("\n🧪 Testing chatbot functionality...")
    try:
        from simple_rag_chatbot import SimpleRAGChatbot
        chatbot = SimpleRAGChatbot('machdatum_rag_db.json')
        
        test_query = "What services does MachDatum provide?"
        result = chatbot.chat(test_query)
        
        if result['response'] and len(result['context_used']) > 0:
            print("✅ Chatbot test successful!")
            print(f"   - Found {len(result['context_used'])} relevant context entries")
            print(f"   - Similarity scores: {[f'{score:.3f}' for score in result['similarity_scores']]}")
            return True
        else:
            print("❌ Chatbot test failed - no relevant context found")
            return False
    except Exception as e:
        print(f"❌ Chatbot test failed: {e}")
        return False

def run_chatbot():
    """Run the chatbot application"""
    print("\n🚀 Choose how to run the MachDatum RAG Chatbot:")
    print("1. 🌐 Web Interface (Recommended)")
    print("2. 💻 Command Line Interface (Simple RAG)")
    print("3. 🧪 Test Gemini API Integration")
    print("4. 📊 Show Database Statistics")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🌐 Starting web interface...")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 60)
        try:
            subprocess.check_call([sys.executable, "simple_web_app.py"])
        except KeyboardInterrupt:
            print("\n👋 Web server stopped!")
    
    elif choice == "2":
        print("\n💻 Starting command line chatbot...")
        print("🛑 Type 'quit' to exit")
        print("-" * 60)
        try:
            subprocess.check_call([sys.executable, "simple_rag_chatbot.py"])
        except KeyboardInterrupt:
            print("\n👋 Chatbot stopped!")
    
    elif choice == "3":
        print("\n🧪 Testing Gemini API integration...")
        try:
            subprocess.check_call([sys.executable, "test_gemini.py"])
        except Exception as e:
            print(f"Gemini API test failed: {e}")
    
    elif choice == "4":
        print("\n📊 Database Statistics...")
        try:
            import json
            with open('machdatum_rag_db.json', 'r', encoding='utf-8') as f:
                db = json.load(f)
            
            print(f"Company: {db['company_name']}")
            print(f"Website: {db['website']}")
            print(f"Total knowledge entries: {len(db['knowledge_base'])}")
            
            # Count by category
            categories = {}
            for entry in db['knowledge_base']:
                cat = entry.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
            
            print("\nEntries by category:")
            for cat, count in categories.items():
                print(f"  - {cat}: {count}")
                
        except Exception as e:
            print(f"Error reading database: {e}")
    
    else:
        print("❌ Invalid choice. Please run again and select 1-4.")

def main():
    """Main setup and run function"""
    print("=" * 70)
    print("🏢 MachDatum RAG Chatbot - Complete Setup & Runner")
    print("=" * 70)
    print()
    
    # Check if document exists
    if not os.path.exists("MachDatum Details.docx"):
        print("❌ Error: 'MachDatum Details.docx' not found!")
        print("📁 Please make sure the document is in the same folder as this script.")
        return
    
    print("✅ Found MachDatum Details.docx")
    
    # Step 1: Install dependencies
    if not install_dependencies():
        return
    
    # Step 2: Create database
    if not create_database():
        return
    
    # Step 3: Test functionality
    if not test_chatbot():
        print("⚠️  Warning: Basic test failed, but continuing...")
    
    # Step 4: Show system info
    print(f"\n📋 System Information:")
    print(f"   - Python: {sys.version.split()[0]}")
    print(f"   - Workspace: {os.getcwd()}")
    print(f"   - Database: {'✅ Ready' if os.path.exists('machdatum_rag_db.json') else '❌ Missing'}")
    
    # Step 5: Run chatbot
    print("\n" + "=" * 70)
    run_chatbot()

if __name__ == "__main__":
    main()