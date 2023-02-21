## strawberryAPI 

a lightweight `MicroPython` web framework & server for `RaspberryPi Pico W`

### Features:

---
- async web server, can be used in 2 modes:
  - as client
  - as host (Wi-Fi hotspot)
- blueprints based routing (like `flask`)
- `GET` & `POST` request methods
- url parameters `/page_url_params/<arg_1>`
- simple templating engine supporting:
  - templates inheritance
  - variables injection
- routing errors handling
- generator based file responses
- files hosting
- debug logging

### How to use:

---
get production ready package from `prod` branch, use it in your project as shown in `Examples` section

### Examples:

---
- basic server & app setup - `main.py`
- API (POST/GET) - `routes/api/routes.py`
- pages (redirects, forms etc.) with templates parsing - `routes/home/routes.py`


### Requirements

---
packages in `requirements.txt` used for `MicroPython` development with `PyCharm`
