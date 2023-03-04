# hscr - Hentai Scroller

Free-to-use hentai scroller run locally from your laptop. Fetches all images associated with specific sauce id and creates long panel of images to autoscroll down. Pretty hacky thing I built in a few hours, so it's very barebones. Feel free to fork or clone and modify it. Also, Python 3.9 was used, so it might not work with other versions depending on the versions of libraries used.

## How to Use

1. Clone the repo `git clone https://github.com/3zhang4li/hentai-scroller.git`

2. Install dependencies `pip install -r requirements.txt`

3. Create your `.env` file. IT MUST MATCH THIS EXACTLY, OR WILL NOT WORK:

```
FERNET_KEY='WGaTGCKEhOQQu20KrYHpNhu3NXHAkPaImIrd2K3rkOI='
FIRST_SECRET='gAAAAABkAwrUJd_ctspOvRDb-Qb5jzYQWZZ8_k_l4zUXKIbuGdOAivKSjsWjPk_t8WBu0EaLlBlMCB-yqxUPND92TFWwGFTzK-TtB5tK5CUGPpJVcP6fuxI='
SECOND_SECRET='gAAAAABkAwykhAEdzqrtvxV5l4V-39HKnYPnXKdlPeRMQd1O7nU4JUTT47Iy7Hgbn3XUjxY9YtXgctucHqdElRYBX83TwL0gf4R5eCIm9XWbGmKaSxCO948='
THIRD_SECRET='gAAAAABkAw0-8PMf83pMAGNCC2tiQFTWFR6vqw_aKuhgRuCqQXU-SsZF10ggtCLrl7eJe2QAbGvc0-fsjrMPgZnYInI2RHEyew=='
APP_SECRET_1='gAAAAABkAw4nx16UIPZ4rxoYZAI-ISaSZ8iGY-8H9eO9W3FsKJipeoPoAkS4_FYUP8QzhBUOSC4meGk3_wg_WGeRFJqVKwvauw=='
```

NOTE: In the code previously, there were strings like "hentai" or "nhentai.net" when sending requests or accessing files so I decided to encrypt those strings first, then decrypt them when I need to use them. It's a bigger hassle, but at the cost of being extra discreet. 

4. After creating your `.env` file, source them: `source .env`. 

5. Run the app `python app.py`
