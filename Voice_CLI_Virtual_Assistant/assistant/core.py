"""The assistant object that wires configuration, speech and the router."""

from __future__ import annotations

import webbrowser

from .commands import CommandRouter, normalise
from .config import AssistantConfig, load_config
from .speech import SpeechEngine, greeting_for


class VirtualAssistant:
    """Multi-modal assistant driven by either typed or spoken commands."""

    def __init__(self, config: AssistantConfig | None = None,
                 speech: SpeechEngine | None = None,
                 router: CommandRouter | None = None,
                 opener=None, confirm=None) -> None:
        self.config = config or load_config()
        self.speech = speech or SpeechEngine(self.config)
        self.router = router or CommandRouter()
        # Injected so tests never open a browser and never touch power state.
        self.opener = opener or webbrowser.open
        self.confirm = confirm or self._confirm_interactively

    # ------------------------------------------------------------- helpers
    def _confirm_interactively(self, action: str) -> bool:
        """Ask the user to type the action name before a power command runs."""
        prompt = f"Type '{action}' to confirm, anything else cancels: "
        try:
            return input(prompt).strip().lower() == action
        except (EOFError, KeyboardInterrupt):
            return False

    def greeting(self) -> str:
        """Return the start-up greeting."""
        modes = "voice and text" if self.speech.stt_available else "text"
        return (
            f"{greeting_for()}! I am your ML-CaPsule assistant, listening in "
            f"{modes} mode. Say 'help' to see what I can do."
        )

    # -------------------------------------------------------------- driver
    def handle(self, utterance: str):
        """Normalise ``utterance``, dispatch it and return the response."""
        return self.router.dispatch(self, normalise(utterance, self.config.wake_word))

    def respond(self, utterance: str):
        """Handle ``utterance`` and speak the response aloud."""
        response = self.handle(utterance)
        if response.text:
            self.speech.speak(response.text)
        return response

    def run(self, voice: bool = False) -> int:
        """Run the interactive loop until the user exits."""
        self.speech.enable_stt = voice
        self.speech.speak(self.greeting())
        while True:
            try:
                utterance = self.speech.listen("you > ")
            except KeyboardInterrupt:
                print()
                self.speech.speak("Goodbye!")
                return 0
            if not utterance.strip():
                continue
            response = self.respond(utterance)
            if response.should_exit:
                return 0
