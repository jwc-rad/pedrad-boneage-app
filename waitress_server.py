import argparse
from waitress import serve
from boneage import create_app
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Bone Age Server.")
    parser.add_argument('--host', type=str, default='0.0.0.0', help='DONT TOUCH')
    parser.add_argument('--port', type=int, default=19001, help='server port')
    args = parser.parse_args()
    
    host = args.host
    port = args.port
    
    app = create_app()
    serve(app, host=host, port=port)