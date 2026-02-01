import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from graph import create_stable_scout_graph

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize the graph
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("WARNING: GROQ_API_KEY not found in .env file")
    scout = None
else:
    scout = create_stable_scout_graph(api_key)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'groq_api_configured': bool(api_key),
        'graph_initialized': scout is not None
    })

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Main analysis endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        
        if not scout:
            return jsonify({'error': 'System not initialized. Check GROQ_API_KEY in .env'}), 500
        
        # Create input for the graph
        inputs = {"messages": [HumanMessage(content=query)]}
        
        # Collect all messages from the graph execution
        messages = []
        
        for event in scout.stream(inputs, stream_mode="values"):
            if "messages" in event:
                # Get the latest message
                latest_message = event["messages"][-1]
                
                # Convert message to dict
                message_dict = {
                    'type': latest_message.type if hasattr(latest_message, 'type') else 'unknown',
                    'content': latest_message.content if hasattr(latest_message, 'content') else str(latest_message)
                }
                
                # Add additional fields if available
                if hasattr(latest_message, 'name'):
                    message_dict['name'] = latest_message.name
                
                if hasattr(latest_message, 'tool_calls') and latest_message.tool_calls:
                    message_dict['tool_calls'] = [
                        {
                            'name': tc.get('name', ''),
                            'args': tc.get('args', {}),
                            'id': tc.get('id', '')
                        }
                        for tc in latest_message.tool_calls
                    ]
                
                messages.append(message_dict)
        
        return jsonify({
            'query': query,
            'messages': messages,
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Analysis failed: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("🚀 StableScout Python API Server")
    print("=" * 60)
    print(f"Port: {port}")
    print(f"Debug Mode: {debug}")
    print(f"GROQ API Key: {'✓ Configured' if api_key else '✗ Missing'}")
    print(f"Graph Status: {'✓ Ready' if scout else '✗ Not Initialized'}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
