import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from anthropic import Anthropic

class ClaudeUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def initUI(self):
        layout = QVBoxLayout()

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter your text here...")
        layout.addWidget(self.input_text)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)
        layout.addWidget(self.submit_button)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)
        self.setWindowTitle('Claude 3.5 Sonnet UI')
        self.setGeometry(300, 300, 500, 500)

    def on_submit(self):
        user_input = self.input_text.toPlainText()
        response = self.get_claude_response(user_input)
        self.output_text.setPlainText(response)

    def get_claude_response(self, prompt):
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == '__main__':
    app = QApplication([])
    ex = ClaudeUI()
    ex.show()
    app.exec()