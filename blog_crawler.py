from bs4 import BeautifulSoup
from datetime import datetime
from git import Repo
import requests

def get_blog_url(user):
    return f"https://blog.naver.com/{user}"

def get_blog(user):
    return requests.get(get_blog_url(user))

def get_xml_url(user):
     return f"https://rss.blog.naver.com/{user}.xml"

def get_xml(user):
     return requests.get(get_xml_url(user))
    
def get_soup(html):
    return  BeautifulSoup(html.text, 'html.parser')

def IsVaildBlog(soup):
    try:
        return False, soup.find('h2').find('img').get('alt')
    except AttributeError:
        return True, "블로그 주소가 확인되었습니다."

def get_logNo(url):
    return url.split('/')[-1]

def get_PostView_url(log):
    return f"https://blog.naver.com/PostView.nhn?blogId={user}&logNo={log}"

def get_html_tag(log):
    return f"""\t<a href="{get_PostView_url(log)}">\n\n</body>\n</html>"""

def print_url_txt(log):
    with open("logs.txt", "a") as f_url:
        f_url.write(f"{log}\n")

def print_url_html(log):
    with open("urls.html", "rb+") as f_index:
        f_index.seek(-16, 2)
        f_index.write(get_html_tag(log).encode())

def get_logs():
    with open('logs.txt', 'r') as f_log:
        return [log[:-1] for log in f_log.readlines()]

def get_datetime_now():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+09:00')

def get_html_lastmod():
    now = get_datetime_now()
    return now, f"<lastmod>{now}</lastmod>\r\n\t</url>\r\n</urlset>"

def update_sitemap():
    now, datetime_now = get_html_lastmod()
    
    with open("sitemap.xml", "rb+") as f_sitemap:
    	f_sitemap.seek(-64, 2)
    	f_sitemap.write(datetime_now.encode())

    repo.index.add(['sitemap.xml'])
    repo.index.commit(f"{now}")

def git_add(msg):
    repo.index.add(['urls.html', 'logs.txt'])
    repo.index.commit(f"add {msg}")
    
    print(f"add {msg}")

def git_push():
    repo.remote().push()

if __name__ == '__main__':
    user = ""

    repo = Repo('')
    logs = get_logs()

    html = get_xml(user)
    soup = get_soup(html)
    items = soup.find_all('item')

    for item in items:
        title = item.find('title').text
        url = item.find('guid').text
        logNo = get_logNo(url)

        if logNo not in logs[::-1]:
            print_url_txt(logNo)
            print_url_html(logNo)

            git_add(title)
        else:
            break
    
    update_sitemap()
    git_push()