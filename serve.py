#!/usr/bin/python3

from cfr import create_app

def main():
  app = create_app()
  app.run(
    debug=True,
    threaded=True,
    host='127.0.0.1',
    port=8000
  )

if __name__ == '__main__':
  main()
