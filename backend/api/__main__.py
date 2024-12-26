import uvicorn


def main():
    uvicorn.run(app="api.app:create_app", host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
