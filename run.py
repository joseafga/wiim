#! /usr/bin/env python3

if __name__ == '__main__':
    from wiim import create_app

    app = create_app('settings')
    # Run a test server.
    app.run(port=8080)
