"""
This module provides the PhotoboothController class, which connects the Photobooth-style GUI with the backend functionality.

Classes in this module include:
- PhotoboothController: Handles the communication between the Photobooth-style GUI and the backend.

EVERYTHING BELOW IS TEMPORARY for now
"""

import controller.base_controller as base_controller
import view.photobooth_gui as photobooth_gui
class PhotoboothController(base_controller.BaseController):
    def __init__(self, view):
        super().__init__(view)
        # Bind buttons or events to controller methods

    # Implement methods to handle events

    def on_start_button_click(self):
        """
        Handles the start button click event in the Photobooth GUI.
        """
        pass

    def on_stop_button_click(self):
        """
        Handles the stop button click event in the Photobooth GUI.
        """
        pass

    def on_user_recognized(self, user):
        """
        Handles the event when a user is recognized in the Photobooth GUI.
        
        Args:
            user (str): The recognized user.
        """
        pass
    
    def on_exit(self):
        """
        Handles the exit event for the application.
        """
        photobooth_gui.video_capture.release()
