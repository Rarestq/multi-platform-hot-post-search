# Multi-Platform Hot Post Search

This repository provides a tool for searching hot posts across multiple platforms, for now it supports reddit and hackernews.

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
input your keyword: ComfyUI

hottest results of Reddit and HackerNews:
```markdown
Platform: Reddit
Author: Illustrious-Yard-871
Title: I couldn't find an intuitive GUI for GLIGEN so I made one myself. It uses ComfyUI in the backend
Metrics: 2437
Link: https://www.reddit.com/r/StableDiffusion/comments/1asmn6d/i_couldnt_find_an_intuitive_gui_for_gligen_so_i/
Post: 2024-02-16 23:12:58
---
Platform: Reddit
Author: Choidonhyeon
Title: ComfyUI - Creating Game Icons base on realtime drawing
Metrics: 1542
Link: https://www.reddit.com/r/StableDiffusion/comments/1b9vqdz/comfyui_creating_game_icons_base_on_realtime/
Post: 2024-03-08 18:44:52
---
Platform: Reddit
Author: ThroughForests
Title: Hank Hill tries ComfyUI
Metrics: 1252
Link: https://www.reddit.com/r/StableDiffusion/comments/15ilqso/hank_hill_tries_comfyui/
Post: 2023-08-05 04:22:22
---
Platform: Reddit
Author: comfyanonymous
Title: Real time prompting with SDXL Turbo and ComfyUI running locally
Metrics: 1181
Link: https://www.reddit.com/r/StableDiffusion/comments/1869cnk/real_time_prompting_with_sdxl_turbo_and_comfyui/
Post: 2023-11-28 22:48:52
---
Platform: Reddit
Author: AtreveteTeTe
Title: Roll your own Motion Brush with AnimateDiff and in-painting in ComfyUI
Metrics: 930
Link: https://www.reddit.com/r/StableDiffusion/comments/17xnqn7/roll_your_own_motion_brush_with_animatediff_and/
Post: 2023-11-17 20:05:15
---
Platform: HackerNews
Author: gslin
Title: Windows 9x and Word 9x at 800x600 resolution. Spacious. Comfy
Metrics: 338
Link: https://oldbytes.space/@48kRAM/110695813509755748
Post: 2023-07-11 15:31:17
---
Platform: HackerNews
Author: belladoreai
Title: Keylogger discovered in image generator extension
Metrics: 302
Link: https://old.reddit.com/r/comfyui/comments/1dbls5n/psa_if_youve_used_the_comfyui_llmvision_node_from/
Post: 2024-06-09 17:29:00
---
Platform: HackerNews
Author: vmoore
Title: Comfy Software: A software aesthetic for hackers with depression
Metrics: 193
Link: https://catgirl.ai/log/comfy-software/
Post: 2022-10-02 05:31:36
---
Platform: HackerNews
Author: godDLL
Title: A Comfy Helvetica frontpage for Hacker News
Metrics: 176
Link: http://comfy-helvetica.jottit.com/
Post: 2011-01-13 00:45:39
---
Platform: HackerNews
Author: kettunen
Title: Creating Comfy FreeBSD Jails Using Standard Tools
Metrics: 123
Link: https://kettunen.io/post/standard-freebsd-jails/
Post: 2021-01-17 19:07:30
---
```

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature`)
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`)
5. Push to the branch (`git push origin feature`)
6. Create a new Pull Request.

## Contact
- Email: rarestzhou@gmail.com
- Wechat:zjc111369
![](https://mmbiz.qpic.cn/mmbiz_jpg/KhD0fibB4GCDFlkCNLH5B7xiaIlGSWFSbXEtCYRJQ7fzsvb447XhJm35pkgjN75e0IfAbIBp5hdfl15ke3VJkdog/640?wx_fmt=jpeg)

---

Feel free to customize this template further based on your specific project details and requirements!
