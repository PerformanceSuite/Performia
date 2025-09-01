#!/usr/bin/env python3
"""
Performia UI Session Manager
Manages development sessions for continuity across Claude Code sessions
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import subprocess
import shutil

class SessionManager:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.sessions_dir = self.base_dir / ".sessions"
        self.state_dir = self.base_dir / ".state"
        self.current_session_file = self.base_dir / ".current-session"
        
        # Create directories if they don't exist
        self.sessions_dir.mkdir(exist_ok=True)
        self.state_dir.mkdir(exist_ok=True)
        
        self.current_session = self.load_current_session()
    
    def load_current_session(self):
        """Load the current session ID"""
        if self.current_session_file.exists():
            return self.current_session_file.read_text().strip()
        return None
    
    def save_current_session(self, session_id):
        """Save the current session ID"""
        self.current_session_file.write_text(session_id)
        self.current_session = session_id
    
    def new_session(self, name=None):
        """Create a new session"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"session_{timestamp}"
        if name:
            session_id = f"{session_id}_{name.replace(' ', '_')}"
        
        session_data = {
            "id": session_id,
            "name": name or "Unnamed Session",
            "created": timestamp,
            "phase": self.get_current_phase(),
            "last_mode": None,
            "components_created": [],
            "tests_passed": [],
            "git_commits": [],
            "notes": []
        }
        
        session_file = self.sessions_dir / f"{session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        self.save_current_session(session_id)
        print(f"✅ Created new session: {session_id}")
        return session_id
    
    def continue_session(self):
        """Continue the last session"""
        if not self.current_session:
            sessions = sorted(self.sessions_dir.glob("*.json"))
            if sessions:
                last_session = sessions[-1].stem
                self.save_current_session(last_session)
                print(f"✅ Continuing session: {last_session}")
                self.show_session_status()
                return last_session
            else:
                return self.new_session("initial")
        
        print(f"✅ Continuing session: {self.current_session}")
        self.show_session_status()
        return self.current_session
    
    def list_sessions(self):
        """List all sessions"""
        sessions = sorted(self.sessions_dir.glob("*.json"))
        if not sessions:
            print("No sessions found")
            return
        
        print("\n📋 Available Sessions:")
        print("-" * 50)
        for session_file in sessions:
            with open(session_file) as f:
                data = json.load(f)
                current = "→" if session_file.stem == self.current_session else " "
                print(f"{current} {data['id']}")
                print(f"   Name: {data['name']}")
                print(f"   Created: {data['created']}")
                print(f"   Phase: {data.get('phase', 'Unknown')}")
                print()
    
    def load_session(self, session_id):
        """Load a specific session"""
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            print(f"❌ Session not found: {session_id}")
            return None
        
        self.save_current_session(session_id)
        print(f"✅ Loaded session: {session_id}")
        self.show_session_status()
        return session_id
    
    def save_session(self):
        """Save current session state"""
        if not self.current_session:
            print("❌ No active session")
            return
        
        session_file = self.sessions_dir / f"{self.current_session}.json"
        with open(session_file) as f:
            data = json.load(f)
        
        # Update session data
        data["last_updated"] = datetime.now().strftime("%Y%m%d_%H%M%S")
        data["phase"] = self.get_current_phase()
        
        # Save git status
        try:
            git_status = subprocess.check_output(["git", "status", "--short"], 
                                                text=True, stderr=subprocess.DEVNULL)
            data["git_status"] = git_status
        except:
            pass
        
        with open(session_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Session saved: {self.current_session}")
    
    def show_session_status(self):
        """Show current session status"""
        if not self.current_session:
            print("No active session")
            return
        
        session_file = self.sessions_dir / f"{self.current_session}.json"
        if not session_file.exists():
            print("Session file not found")
            return
        
        with open(session_file) as f:
            data = json.load(f)
        
        print("\n📊 Current Session Status:")
        print("-" * 50)
        print(f"ID: {data['id']}")
        print(f"Name: {data['name']}")
        print(f"Phase: {data.get('phase', 'Unknown')}")
        print(f"Last Mode: {data.get('last_mode', 'None')}")
        print(f"Components Created: {len(data.get('components_created', []))}")
        print(f"Tests Passed: {len(data.get('tests_passed', []))}")
        
        # Check Claude Flow status
        try:
            flow_status = subprocess.check_output(
                ["npx", "claude-flow@alpha", "hive-mind", "status"],
                text=True, stderr=subprocess.DEVNULL, timeout=5
            )
            if "Ready" in flow_status:
                print("Claude Flow: ✅ Ready")
            else:
                print("Claude Flow: ⚠️ Check status")
        except:
            print("Claude Flow: ❌ Not responding")
        
        print("-" * 50)
    
    def get_current_phase(self):
        """Determine current development phase"""
        # Check which components exist
        components_dir = self.base_dir / "src" / "components" / "basic"
        if not components_dir.exists() or not any(components_dir.glob("*.cpp")):
            return "Phase 1: Foundation"
        
        modes_dir = self.base_dir / "src" / "modes"
        studio_file = modes_dir / "StudioMode.cpp"
        if studio_file.exists():
            return "Phase 3: Studio Mode"
        
        if (components_dir / "PerformiaKnob.cpp").exists():
            return "Phase 2: Basic Components"
        
        return "Phase 1: Foundation"
    
    def add_note(self, note):
        """Add a note to the current session"""
        if not self.current_session:
            print("❌ No active session")
            return
        
        session_file = self.sessions_dir / f"{self.current_session}.json"
        with open(session_file) as f:
            data = json.load(f)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.setdefault("notes", []).append(f"[{timestamp}] {note}")
        
        with open(session_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Note added to session")
    
    def checkpoint(self, message):
        """Create a git checkpoint"""
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Checkpoint: {message}"], check=True)
            print(f"✅ Git checkpoint created: {message}")
            
            # Update session
            if self.current_session:
                session_file = self.sessions_dir / f"{self.current_session}.json"
                with open(session_file) as f:
                    data = json.load(f)
                data.setdefault("git_commits", []).append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "message": message
                })
                with open(session_file, 'w') as f:
                    json.dump(data, f, indent=2)
        except subprocess.CalledProcessError as e:
            print(f"❌ Git checkpoint failed: {e}")

def main():
    """Main entry point for command-line usage"""
    manager = SessionManager()
    
    if len(sys.argv) < 2:
        print("Usage: session.py [new|continue|list|load|save|status|note|checkpoint] [args...]")
        return
    
    command = sys.argv[1]
    
    if command == "new":
        name = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        manager.new_session(name)
    elif command == "continue":
        manager.continue_session()
    elif command == "list":
        manager.list_sessions()
    elif command == "load":
        if len(sys.argv) < 3:
            print("Usage: session.py load <session_id>")
        else:
            manager.load_session(sys.argv[2])
    elif command == "save":
        manager.save_session()
    elif command == "status":
        manager.show_session_status()
    elif command == "note":
        if len(sys.argv) < 3:
            print("Usage: session.py note <note text>")
        else:
            note = " ".join(sys.argv[2:])
            manager.add_note(note)
    elif command == "checkpoint":
        if len(sys.argv) < 3:
            print("Usage: session.py checkpoint <message>")
        else:
            message = " ".join(sys.argv[2:])
            manager.checkpoint(message)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()