# Instagram Tool

### Console based tool with useful features that can be used for Instagram.

![console look](./assets/preview.png)

# Installing dependencies

## 1. Python dependencies

```bash
pip install selenium colored pillow python-dotenv requests
```

or run the `dep-installer.py` file.

## 2. ChromeDriver

** Please check [here](https://googlechromelabs.github.io/chrome-for-testing/) for the latest version. Current ChromeDriver version is 127 Stable (win64). **

ChromeDriver version must be the same chrome version installed on your system. You can check your installed chrome version via Settings > About Chrome.

#### Installation

1. Add latest ChromeDriver to in "driver" folder.
2. Set image and driver path.

# Removing pending follow requests

Order to remove pending follow requests:

1. Download your data from Instagram.
   - Your Activity > [Download Your Information](https://www.instagram.com/download/request)
   - Click continue.
   - Click "Download or transfter information".
   - Find "Connections" tab and tick the "Followers and following" check box.
   - Click Next.
   - Tick the "Dwonload to device" check box & click next.
   - Select a "Date range" & Select "Format" as JSON then click "Create files".
2. Wait for the Instagram notifies you with e-mail that the process is complete.
3. After downloading the data that Instagram sends you, find `pending_follow_requests.json` file under `connections/followers_and_following` folder.
4. Move the file to `data` folder in the tool.

> [!WARNING]
> Do not rename or edit the file content.

# Fill login information

if you don't want to pass your login information every time you run the tool, please fill the `_loginInfo` file or create a `.env` file with the following variables:

```bash
IG_USERNAME="your_username"
IG_PASSWORD="your_password"
```

# Additional Notes

The headless option may lead to certian action blocks (follow/unfollow) from Instagram if used too often. You might want to disable it in your use case.

Order to disable it comment out or remove the below line from **InstagramTool.py** file.

```py
 self.chrome_options.add_argument("--headless")
```

## Links to the repositories of the libraries used in this tool

- [Selenium](https://github.com/SeleniumHQ/Selenium)
- [Colored](https://gitlab.com/dslackw/colored)
- [Pillow](https://github.com/python-pillow/Pillow)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [Requests](https://github.com/psf/requests)
