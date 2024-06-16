```markdown
# Multi-Platform Hot Post Search

This repository provides a tool for searching hot posts across multiple platforms.

## How to Use

To use this tool, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Rarestq/multi-platform-hot-post-search.git
   ```

2. Navigate to the project directory:

   ```bash
   cd multi-platform-hot-post-search
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. create .env.local file, and setup your own Reddit Client ID and Client Secret, refer to [Reddit Apps](https://www.reddit.com/prefs/apps/):
  
  ```markdown
   REDDIT_CLIENT_ID=""
   REDDIT_CLIENT_SECRET=""
   REDDIT_USER_AGENT="YourAppName/0.1 by username"
   ```

## Usage

Run the script:

   ```bash
   python3 main.py
   ```
then you get results from reddit and hackernews by your keyword.

### Example

```bash
python3 main.py
```
input your keyword: Gemini Nano

results:
```markdown
Platform: Reddit
Author: lostlifon
Description: GPT-4 Week 5. Open Source is coming + Music industry in shambles - Nofil's Weekly Breakdown
Metrics: 3353
Link: https://www.reddit.com/r/ChatGPT/comments/12v8oly/gpt4_week_5_open_source_is_coming_music_industry/
Created_at: 2023-04-22 15:05:55
---
Platform: Reddit
Author: PhanThomBjork
Description: SDXL + SVD + Suno AI
Metrics: 1090
Link: https://www.reddit.com/r/StableDiffusion/comments/18f80gg/sdxl_svd_suno_ai/
Created_at: 2023-12-10 17:03:41
---
Platform: Reddit
(venv) (base) rarestzhoudeMacBook-Pro:multi-platform-hot-post-search rarestzhou$ python3 main.py 
Please enter the keyword you want to search for: suno ai
Searching HackerNews for keyword: suno ai
Platform: Reddit
Author: lostlifon
Description: GPT-4 Week 5. Open Source is coming + Music industry in shambles - Nofil's Weekly Breakdown
Metrics: 3358
Link: https://www.reddit.com/r/ChatGPT/comments/12v8oly/gpt4_week_5_open_source_is_coming_music_industry/
Created_at: 2023-04-22 15:05:55
---
Platform: Reddit
Author: PhanThomBjork
Description: SDXL + SVD + Suno AI
Metrics: 1094
Link: https://www.reddit.com/r/StableDiffusion/comments/18f80gg/sdxl_svd_suno_ai/
Created_at: 2023-12-10 17:03:41
---
Platform: Reddit
Author: Galadnir
Description: i'm trying to marry Isolla of Suno, but I didn't know that incest is popular in calradia.
Metrics: 584
Link: https://www.reddit.com/r/mountandblade/comments/6to5mo/im_trying_to_marry_isolla_of_suno_but_i_didnt/
Created_at: 2017-08-14 17:55:03
---
Platform: Reddit
Author: Shynaya
Description: Lil update on my collection ! Bought a lot of since my last post …. 🥹 I need to finish my Claynore c...
Metrics: 508
Link: https://www.reddit.com/r/MangaCollectors/comments/xihhy3/lil_update_on_my_collection_bought_a_lot_of_since/
Created_at: 2022-09-19 16:38:42
---
Platform: Reddit
Author: Infamous_AI_1568
Description: The best AI for music creation
Metrics: 478
Link: https://www.reddit.com/r/AI_Tools_News/comments/18zaqhm/the_best_ai_for_music_creation/
Created_at: 2024-01-05 16:21:48
---
Platform: HackerNews
Author: elsewhen
Description: Suno AI
Metrics: 336
Link: https://www.suno.ai/
Created_at: 2023-12-23 12:24:14
---
Platform: HackerNews
Author: herbertl
Description: Suno, an AI music generator
Metrics: 139
Link: https://www.rollingstone.com/music/music-features/suno-ai-chatgpt-for-music-1234982307/
Created_at: 2024-03-18 15:52:02
---
```

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature`)
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature`)
6. Create a new Pull Request.

## Contact
Email: rarestzhou@gmail.com
Wechat:zjc111369
![](https://mp.weixin.qq.com/cgi-bin/getimgdata?msgid=&mode=small&source=&fileId=100000588&ow=725340616&token=1048341528&lang=zh_CN)

---

Feel free to customize this template further based on your specific project details and requirements!
