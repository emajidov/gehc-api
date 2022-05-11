from gehc_api import initialize_api


if __name__ == "__main__":
    application = initialize_api()
    application.run(port=8080)
