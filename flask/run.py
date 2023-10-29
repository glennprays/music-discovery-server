from app import create_app

app = create_app()

if __name__ == "__main__":
    print('masuk')
    app.run(debug=True)