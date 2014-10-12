# coding=utf-8
import ConfigParser,urllib2,cookielib,lxml
from lxml import etree
def httpCrawlerMirror(url):
    '''
    @summary: 网页抓取
    '''
    content = httpRequest(url)
    title = parseMirrorHtml(content)
    if title:
        '''
        获取成功，保存镜像地址
        '''
        saveMirrorData(title);
    else:
        raise Exception("fail");

def httpRequest(url):
    '''
    @summary: 网络请求
    '''  
    try:
        ret = None
        SockFile = None
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322)')
        request.add_header('Pragma', 'no-cache')
        opener = urllib2.build_opener()
        SockFile = opener.open(request);
        '''encoding = SockFile.headers['content-type'].split('charset=')[-1];
        ret = unicode(SockFile.read(), encoding);
        '''
        ret = SockFile.read();

    finally:
        if SockFile:
            SockFile.close()

    return ret

def parseMirrorHtml(html):
    '''
    @summary: 抓取结构化数据
    '''
    content = None
    htmltree = lxml.etree.HTML(html);
    content = htmltree.xpath("//span[@style='font-size: medium']/a/@href");

    return content
def parseVPNHtml(html):
    '''
    @summary: 抓取结构化数据
    '''
    content = None
    htmltree = lxml.etree.HTML(html);
    vpntable = htmltree.xpath("//table[@id='vg_hosts_table_id']")[2];
    i = 0;
    for tr in vpntable:
        for item in tr:
            print item.xpath('string()') + "\t";
        print "\n----------------------------------\n";
        i = i + 1;
        if i > 20:
            break;
    return vpntable
def saveMirrorData(data):
    '''
    @summary: 数据存储
    '''
    i = 1;
    config = ConfigParser.RawConfigParser();
    config.add_section('mirrors');
    for mirror in data:
        config.set("mirrors", "siteurl" + str(i), mirror);
        print mirror;
        i = i + 1;
    with open(mirrorFile, 'wb') as configfile:
        config.write(configfile);

def tryMirrorSite():
    mirrorConfig = ConfigParser.ConfigParser();
    mirrorConfig.read(mirrorFile);
    for item in mirrorConfig.items("mirrors"):
        try:
            print "try mirror site:" + item[1];
            httpCrawlerMirror(item[1] + siteAppend);
            '''成功一次，break掉'''
            break;
        except Exception, e:
            '''
            fail
            '''
            print e;
            continue;
        finally:
            pass;

def httpCrawlerVPN(url):
    '''
    @summary: 网页抓取
    '''
    content = httpRequest(url)
    title = parseVPNHtml(content)
    if title:
        pass;
    else:
        raise Exception("fail");

def tryMirrorSiteVPN():
    mirrorConfig = ConfigParser.ConfigParser();
    mirrorConfig.read(mirrorFile);
    for item in mirrorConfig.items("mirrors"):
        try:
            print "try to get VPN with mirror site:" + item[1];
            httpCrawlerVPN(item[1]);
            '''成功一次，break掉'''
            break;
        except Exception, e:
            '''
            fail
            '''
            print e;
            continue;
        finally:
            pass;

if __name__ == '__main__':
    cf = ConfigParser.ConfigParser();
    cf.read("config.ini");
    mainUrl = cf.get("main", "mainurl");
    siteAppend = cf.get("main", "sitePath");
    mirrorFile = cf.get("main", "mirrorFile");
    try:
        httpCrawlerMirror(mainUrl + siteAppend);
    except Exception:
        tryMirrorSite();
    finally:
        pass
    '''
    使用mirrorsite去打印vpn信息
    '''
    tryMirrorSiteVPN();

