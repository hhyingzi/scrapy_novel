

import re

alt = "                        · 13小时前                        · 今日更新1章                    "
search_result = re.search("· ([0-9]*.*前)", alt)
pretty_date_result = search_result.group(1).strip()
print(pretty_date_result)




