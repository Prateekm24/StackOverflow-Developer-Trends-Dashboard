"""Browser utilities for opening dashboards."""
import webbrowser
from threading import Timer


def open_browser(port, delay=1.5):
    """
    Open the web browser after a short delay.
    
    Args:
        port: Port number where the dashboard is running
        delay: Delay in seconds before opening browser (default: 1.5)
    """
    url = f'http://127.0.0.1:{port}/'
    webbrowser.open_new(url)


def schedule_browser_open(port, delay=1.5):
    """
    Schedule browser opening with a timer.
    
    Args:
        port: Port number where the dashboard is running
        delay: Delay in seconds before opening browser (default: 1.5)
        
    Returns:
        Timer object that can be cancelled if needed
    """
    timer = Timer(delay, lambda: open_browser(port, delay=0))
    timer.start()
    return timer
