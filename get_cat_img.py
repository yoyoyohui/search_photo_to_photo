import requests
import os
import urllib
import numpy


'''
红色， 表示在工作区

绿色， 表示在暂存区

蓝色， 表示文件有修改，位于暂存区

文件名无颜色，表示位于本地仓库区或已经提交到远程仓库区
'''

'''
https://image.baidu.com/search/acjson?tn=resultjson_com&logid=10996907486721079359&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E7%8C%AB&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word=%E7%8C%AB&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&nojc=&pn=60&rn=30&gsm=3c&1625465189354=
'''
class Spider_baidu_image():
    def __init__(self):
        self.url = 'http://image.baidu.com/search/acjson?'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'}
        self.headers_image = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'Referer': 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1557124645631_R&pv=&ic=&nc=1&z=&hd=1&latest=0&copyright=0&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word=%E8%83%A1%E6%AD%8C'
        }

        self.keyword = input("请输入搜索图片关键字:")
        self.paginator = int(input("请输入搜索页数，每页30张图片："))
        # self.paginator = 50
        # print(type(self.keyword),self.paginator)
        # exit()

    def get_param(self):
        """
        获取url请求的参数，存入列表并返回
        :return:
        """
        keyword = urllib.parse.quote(self.keyword)
        params = []
        for i in range(1, self.paginator + 1):
            params.append(
                'tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=1&latest=0&copyright=0&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&cg=star&pn={}&rn=30&gsm=78&1557125391211='.format(
                    keyword, keyword, 30 * i))
        return params

    def get_urls(self, params):
        """
        由url参数返回各个url拼接后的响应，存入列表并返回
        :return:
        """
        # 每页的urls列表
        urls = []
        for i in params:
            urls.append(self.url + i)
        return urls


    def get_image_url(self, urls):
        image_url = []
        # 进入每一页，获取每一页的所有图片链接列表
        for url in urls:
            proxies = numpy.load('./Proxy_new.npy', allow_pickle=True)
            # print(proxies)
            ip = numpy.random.choice(proxies)
            print(ip)
            json_data = requests.get(url, headers=self.headers, proxies=ip).json()
            json_data = json_data.get('data')
            for i in json_data:
                if i:
                    image_url.append(i.get('thumbURL'))   # 加入图片链接列表
        return image_url

    def get_image(self, image_url):
        """
        根据图片url，在本地目录下新建一个以搜索关键字命名的文件夹，然后将每一个图片存入。
        :param image_url:
        :return:
        """
        cwd = os.getcwd()
        file_name = os.path.join(cwd, 'picture')
        if not os.path.exists('picture'):
            os.mkdir(file_name)
        for index, url in enumerate(image_url, start=1):
            proxies = numpy.load('./Proxy_new.npy', allow_pickle=True)
            # print(proxies)
            ip = numpy.random.choice(proxies)
            print(ip)
            with open(file_name + '\\cat{}.jpg'.format(index), 'wb') as f:
                f.write(requests.get(url, headers=self.headers_image, proxies=ip).content)
            if index != 0 and index % 30 == 0:
                print('{}第{}页下载完成'.format(self.keyword, index / 30))

    def __call__(self, *args, **kwargs):
        params = self.get_param()
        urls = self.get_urls(params)
        image_url = self.get_image_url(urls)
        self.get_image(image_url)


if __name__ == '__main__':
    spider = Spider_baidu_image()
    spider()
