"""
Main entry point to run all dashboards simultaneously.
Note: Running all dashboards at once requires multiple processes.
For most use cases, run individual dashboards using their respective run scripts.
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Run all dashboard servers in separate processes."""
    print("="*60)
    print("Starting All Stack Overflow Dashboards")
    print("="*60)
    print("\nNote: This will start all four dashboards on different ports:")
    print("  • H1A: http://127.0.0.1:8050")
    print("  • H1B: http://127.0.0.1:8051")
    print("  • H2:  http://127.0.0.1:8052")
    print("  • H3:  http://127.0.0.1:8053")
    print("  • H4:  http://127.0.0.1:8054")
    print("  • H5:  http://127.0.0.1:8055")
    print("  • H6A: http://127.0.0.1:8056")
    print("  • H6B: http://127.0.0.1:8057")
    print("\nPress Ctrl+C to stop all servers\n")
    print("="*60 + "\n")
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Define the run scripts
    scripts = [
        project_root / "h1a" / "run_h1a.py",
        project_root / "h1b" / "run_h1b.py",
        project_root / "h2" / "run_h2.py",
        project_root / "h3" / "run_h3.py",
        project_root / "h4" / "run_h4.py",
        project_root / "h5" / "run_h5.py",
        project_root / "h6a" / "run_h6a.py",
        project_root / "h6b" / "run_h6b.py"
    ]
    
    processes = []
    
    try:
        # Start each dashboard in a separate process
        for script in scripts:
            print(f"Starting {script.parent.name}...")
            process = subprocess.Popen(
                [sys.executable, str(script)],
                cwd=str(project_root)
            )
            processes.append(process)
        
        print("\n All dashboards started successfully!")
        print("Press Ctrl+C to stop all servers\n")
        
        # Wait for all processes
        for process in processes:
            process.wait()
            
    except KeyboardInterrupt:
        print("\n\nStopping all dashboards...")
        for process in processes:
            process.terminate()
        print("All dashboards stopped")
    except Exception as e:
        print(f"\n Error: {e}")
        for process in processes:
            process.terminate()

if __name__ == "__main__":
    print("\nNote: For better control, consider running dashboards individually:")
    print("   python h1a/run_h1a.py")
    print("   python h1b/run_h1b.py")
    print("   python h2/run_h2.py")
    print("   python h3/run_h3.py")
    print("   python h4/run_h4.py")
    print("   python h5/run_h5.py")
    print("   python h6a/run_h6a.py")
    print("   python h6b/run_h6b.py\n")
    
    response = input("Do you want to run all dashboards now? (y/n): ")
    if response.lower() == 'y':
        main()
    else:
        print("Cancelled. Run individual dashboards as needed.")
