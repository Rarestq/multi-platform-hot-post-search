from app import create_app
    
app = create_app()

if __name__ == '__main__':
    # Run the application if this script is executed directly
    app.run(debug=app.config['DEBUG_MODE'])