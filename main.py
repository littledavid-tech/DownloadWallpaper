import requests
import bs4


def download_all_wallpapers(url: str, total_page: int):
    """
    下载所有的壁纸
    :param url:
    :param total_page:
    :return:
    """
    list = []
    # 根据页码下载获取缩略图地址
    for i in range(total_page):
        current_url = url + str(i)
        print(f"Get preview page:{i}")
        response = requests.get(current_url, headers={'User-Agent': 'Mozilla/5.0'})
        download_wallpaper(get_page_preview(response.text))
    return list


def get_page_preview(content):
    """
    根据分页数据，获取该页码上的所有缩略图的Link
    :param content:
    :return:
    """
    list = []
    bs = bs4.BeautifulSoup(content, 'html.parser')
    for e in bs.select(".preview"):
        list.append(e.get("href"))
    print(f"Get preview count:{len(list)}")
    return list


def download_wallpaper(url_list):
    """
    根据缩略图的Link下载原图
    :param url_list:
    :return:
    """
    for url in url_list:
        print(f"Downloading {url}")
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        bs = bs4.BeautifulSoup(response.text)
        img_link = bs.select("#wallpaper")[0].get("src")
        print(f"Downloading src:{img_link}")
        stream = requests.get(img_link, stream=True)
        with open(get_file_name_from_url(img_link), "wb") as writer:
            for chunk in stream.iter_content(chunk_size=1024):
                writer.write(chunk)
        print("Download complete")


def get_file_name_from_url(url: str):
    return url.split("/")[-1]


download_all_wallpapers("https://wallhaven.cc/toplist?page=", 70)
