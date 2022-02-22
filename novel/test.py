import re

alt = "'明克街13号 第两百三十八章 海神的陨落！ 首发时间：2022-02-22 00:34:52 章节字数：5303'"
search_result = re.search("首发时间：(.*)章节字数", alt)
date_result = search_result.group(1).strip()
print(date_result)