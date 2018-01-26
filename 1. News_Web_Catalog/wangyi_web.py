import os, sys, urllib2, requests, re
from lxml import etree

class wangyi_web:

    def __init__(self, url):
        self.url = url

    def Get_Info(self, page):
        """
        use regex
        :param page:
        :return: page url
        """
        mypage = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>', page, re.S)
        print mypage
        return mypage

    def New_Get_Info(self, page):
        """
        Use regex will be slow, use XPath will be fase
        :param page:
        :return:
        """
        dom = etree.HTML(page)
        new_item = dom.xpath('//tr/td/a/text()')
        new_page = dom.xpath('//tr/td/a/@href')
        assert(len(new_item)==len(new_page))
        return zip(new_item, new_page)

    def PageResultsSave(self, page, filename, PageInfo):
        if not os.path.exists(page):
            os.makedirs(page)
        path = page + "/" + filename + ".txt"
        with open(path, "w+") as fp:
            for s in PageInfo:
                fp.write("%s\t\t%s\n" % (s[0].encode("utf8"), s[1].encode("utf8")))

    def Spider(self):
        i = 0
        print "downloading", self.url
        mypage = requests.get(self.url).content.decode("gbk")
        # mypage = urllib2.urlopen(url).read().decode("gbk")
        myPageInfo = self.Get_Info(mypage)
        save_page = u"scratching wangyi web"
        filename = str(i) + "_" + u"News List"
        self.PageResultsSave(save_page, filename, myPageInfo)
        i += 1
        for item, url in myPageInfo:
            print "downloading", url
            newpage = requests.get(url).content.decode("gbk")
            newPageInfo = self.New_Get_Info(newpage)
            filename = str(i) + "_" + item
            self.PageResultsSave(save_page, filename, newPageInfo)
            i += 1

if __name__ == "__main__":
    print "start"
    start_url = "http://news.163.com/rank/"
    test = wangyi_web(start_url)
    test.Spider()
    print "end"
