# Manga Web Editor

### Requirements:
- Python (Used 3.12 but 3.9+ should be fine)
- Tailwind (Use CLI tool [from here](https://tailwindcss.com/docs/installation))

### How to run
Download and run tailwind with the command
```shell
./tailwind -i src/templates/main.css -o static/index.css
```
Then create python virtualenv and install packages.
```shell
pip install -r requirements.txt
```

To run the webserver
```shell
fastapi dev  // For dev mode
fastapi run  // For prod
```
