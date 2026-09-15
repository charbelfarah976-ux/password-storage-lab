"""Development entry point for the Password Storage Lab."""

import os

from password_lab import create_app

app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5050")),
        debug=False,
    )
