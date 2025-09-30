#!/usr/bin/env python3
"""
Agent Orchestrator for Household Meal Planning System
This script coordinates the 6 specialized agents and manages the development workflow.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from agents_config import (
    ALL_AGENTS,
    create_phase1_crew,
    create_phase2_crew,
    create_phase3_crew
)

# Load environment variables
load_dotenv()

class AgentOrchestrator:
    """Coordinates multi-agent workflow for the project"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.agents = ALL_AGENTS
        self.current_phase = None

    def initialize_project(self):
        """Phase 0b: Initialize project structure and Git repository"""
        print("=" * 80)
        print("PHASE 0b: Project Foundation & Git Setup")
        print("=" * 80)

        # Create directory structure
        directories = [
            ".github/workflows",
            "backend/src/api/recipes",
            "backend/src/api/inventory",
            "backend/src/api/users",
            "backend/src/api/menu",
            "backend/src/models",
            "backend/src/services",
            "backend/src/utils",
            "backend/src/scrapers",
            "backend/tests",
            "backend/migrations",
            "frontend/src/components",
            "frontend/src/pages",
            "frontend/src/hooks",
            "frontend/src/services",
            "frontend/src/styles",
            "frontend/src/utils",
            "frontend/public",
            "frontend/tests",
            "database/schemas",
            "database/migrations",
            "database/seeds",
            "docs",
            "infrastructure",
            "tests/e2e"
        ]

        print("\n📁 Creating project directory structure...")
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {directory}")

        print("\n✅ Project structure created successfully")
        return True

    def run_phase1(self):
        """Execute Phase 1: Database & Infrastructure Foundation"""
        print("\n" + "=" * 80)
        print("PHASE 1: Database & Infrastructure Foundation")
        print("=" * 80)

        self.current_phase = 1

        # Create and run Phase 1 crew
        crew = create_phase1_crew()

        print("\n🚀 Starting Phase 1 crew...")
        print(f"   Agents: Database Architect, DevOps Engineer")
        print(f"   Tasks: Database schema, API contracts, Docker setup\n")

        try:
            result = crew.kickoff()
            print("\n✅ Phase 1 completed successfully!")
            print(f"\nResults:\n{result}")
            return True
        except Exception as e:
            print(f"\n❌ Phase 1 failed: {e}")
            return False

    def run_phase2(self):
        """Execute Phase 2: Backend Development"""
        print("\n" + "=" * 80)
        print("PHASE 2: Backend API Development")
        print("=" * 80)

        self.current_phase = 2

        print("\n🚀 Starting Phase 2...")
        print(f"   Agent: Backend Developer")
        print(f"   Tasks: Authentication, Recipe APIs, Inventory, Ratings, Menu Planning\n")

        # Phase 2 implementation would go here
        print("\n⚠️  Phase 2 crew implementation pending...")
        return False

    def run_phase3(self):
        """Execute Phase 3: Frontend Development"""
        print("\n" + "=" * 80)
        print("PHASE 3: Frontend UI Development")
        print("=" * 80)

        self.current_phase = 3

        print("\n🚀 Starting Phase 3...")
        print(f"   Agent: Frontend Developer")
        print(f"   Tasks: Authentication UI, Recipe Management, Inventory UI, Menu Planning\n")

        # Phase 3 implementation would go here
        print("\n⚠️  Phase 3 crew implementation pending...")
        return False

    def run_all_phases(self):
        """Execute all development phases in sequence"""
        phases = [
            ("Initialization", self.initialize_project),
            ("Phase 1", self.run_phase1),
            ("Phase 2", self.run_phase2),
            ("Phase 3", self.run_phase3)
        ]

        for phase_name, phase_func in phases:
            success = phase_func()
            if not success:
                print(f"\n❌ {phase_name} failed. Stopping execution.")
                return False

        print("\n" + "=" * 80)
        print("🎉 All phases completed successfully!")
        print("=" * 80)
        return True

    def status_report(self):
        """Generate status report of current project state"""
        print("\n" + "=" * 80)
        print("PROJECT STATUS REPORT")
        print("=" * 80)

        # Check which components exist
        components = {
            "Database Schema": (self.project_root / "database" / "schemas").exists(),
            "API Spec": (self.project_root / "docs" / "API_SPEC.yaml").exists(),
            "Docker Compose": (self.project_root / "infrastructure" / "docker-compose.yml").exists(),
            "Backend": (self.project_root / "backend" / "src").exists(),
            "Frontend": (self.project_root / "frontend" / "src").exists(),
            "Documentation": (self.project_root / "docs").exists()
        }

        print("\n📊 Component Status:")
        for component, exists in components.items():
            status = "✅" if exists else "❌"
            print(f"  {status} {component}")

        print("\n👥 Available Agents:")
        for name, agent in self.agents.items():
            print(f"  • {name.capitalize()}: {agent.role}")

        print()

def main():
    """Main entry point for orchestrator"""
    orchestrator = AgentOrchestrator()

    # Check for API keys
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: No API keys found in .env file")
        print("   Please copy .env.example to .env and add your API keys")
        print()

    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py [command]")
        print("\nCommands:")
        print("  init      - Initialize project structure")
        print("  phase1    - Run Phase 1 (Database & Infrastructure)")
        print("  phase2    - Run Phase 2 (Backend Development)")
        print("  phase3    - Run Phase 3 (Frontend Development)")
        print("  all       - Run all phases")
        print("  status    - Show project status")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        orchestrator.initialize_project()
    elif command == "phase1":
        orchestrator.run_phase1()
    elif command == "phase2":
        orchestrator.run_phase2()
    elif command == "phase3":
        orchestrator.run_phase3()
    elif command == "all":
        orchestrator.run_all_phases()
    elif command == "status":
        orchestrator.status_report()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
