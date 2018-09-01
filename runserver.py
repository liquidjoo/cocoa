from photolog import create_app

application = create_app()

if __name__ == '__main__':
    print("starting test server...")


    application.run(debug=True)
