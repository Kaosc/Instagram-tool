# Instagram Tool

Console based tool with useful features that can be used for Instagram.

![console look](./assets/preview.png)

> [!WARNING]
> Please be aware of the risk of being restricted or blocked by Instagram when using this tool. The likelihood of this occurring may depend on how frequently the tool is used. We do not take any responsibility for any consequences, and users should proceed at their own risk.

# Installing dependencies

## 1. Python dependencies

```bash
pip install selenium colored pillow python-dotenv requests
```

or run the `dep-installer.py` file.

## 2. Setting Up Chrome Driver

The current version of Chrome Driver in this repository is **131**. To ensure compatibility, please check for the latest ChromeDriver version [here](https://googlechromelabs.github.io/chrome-for-testing/).

If a newer version is available:
1. Download the latest ChromeDriver.
2. Replace the existing file in the `driver` folder with the newly downloaded version.

**Note**: If you don't have Chrome installed on your system, make sure to install it before proceeding.

ChromeDriver version must be the same chrome version installed on your system. You can check your installed chrome version via Settings > About Chrome.

### Installation

1. Add latest ChromeDriver to in "driver" folder.
2. Set image and driver path.

# Usage

After setting up the driver, run the **instagramTool.py** file, enter the number corresponding to the action you want to perform, and press Enter.

# Fill login information

if you don't want to pass your login information every time you run the tool, please fill the `_loginInfo` file or create a `.env` file with the following variables:

```bash
IG_USERNAME="your_username"
IG_PASSWORD="your_password"
```

# Removing pending follow requests

Order to remove pending follow requests:

1. Download your data from Instagram.
   - Your Activity > [Download Your Information](https://www.instagram.com/download/request)
   - Click continue.
   - Click "Download or transfter information".
   - Find "Connections" tab and tick the "Followers and following" check box.
   - Click Next.
   - Tick the "Download to device" check box & click next.
   - Select a "Date range" & Select "Format" as JSON then click "Create files".
2. Wait for the Instagram notifies you with e-mail that the process is complete.
3. After downloading the data that Instagram sends you, find `pending_follow_requests.json` file under `connections/followers_and_following` folder.
4. Move the file to `data` folder in the tool.

> [!WARNING]
> Do not rename or edit the file content.

# Additional Notes

- The headless option may lead to certian action blocks (follow/unfollow) from Instagram if used too often. You might want to disable it in your use case.

   Order to disable it comment out or remove the below line from **InstagramTool.py** file.

   ```py
    self.chrome_options.add_argument("--headless=old")
   ```

   > [!WARNING]
      > Be cautious about storing your account credentials, such as your username and password, on your local machine (e.g., in an .env file). If your computer is compromised, this information could be leaked. Additionally, consider enabling two-factor authentication (2FA) for your Instagram account to enhance security.

- If you choose not to use headless, please make sure not to minimize the Chrome window, as it may disrupt some actions when minimized.

## Links to the repositories of the libraries used in this tool

- [Selenium](https://github.com/SeleniumHQ/Selenium)
- [Colored](https://gitlab.com/dslackw/colored)
- [Pillow](https://github.com/python-pillow/Pillow)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [Instaloader](https://github.com/instaloader/instaloader)
