#!/usr/bin/python3

from primary import create_app  # Adjust the import according to your project structure

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

