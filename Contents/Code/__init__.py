# PMS plugin framework

####################################################################################################

VIDEO_PREFIX = "/video/nickelodeon"

#NAMESPACES = {'media':'http://search.yahoo.com/mrss/', 'mediaad':'http://blip.tv/mediaad'}

NICK_ROOT            = "http://www.nick.com"
NICK_SHOWS_LIST      = "http://www.nick.com/shows/"
VIDEO_PLAYER         = "http://media.mtvnservices.com/mgid:cms:item:nick.com:"
RSS_FEED             = "http://www.nick.com/dynamo/video/data/mrssGen.jhtml?type=network&loc=default&hub=kids&mode=playlist&dartSite=nick.playtime.nol&mgid=mgid:cms:item:nick.com:%s&demo=null&block=true"
AJAX_FULL            = "http://www.nick.com/ajax/videos/all-videos/%s/?&sort=date+desc&start=0&page=1&viewType=collectionAll&type=fullEpisodeItem"
AJAX_CLIP            = "http://www.nick.com/ajax/videos/all-videos/%s/?&sort=date+desc&start=0&page=1&viewType=collectionAll&type=videoItem"

NAME = L('Title')
ART  = 'art-default.png'
ICON = 'icon-default.png'

####################################################################################################

def Start():
    Plugin.AddPrefixHandler(VIDEO_PREFIX, MainMenu, L('VideoTitle'), ICON, ART)
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

####################################################################################################
def MainMenu():
    dir = MediaContainer(mediaType='video', viewGroup='List')
    content = HTML.ElementFromURL(NICK_SHOWS_LIST).xpath('//ul[@class="all-shows-list"]//li/a')
    for item in content:
        link = item.get('href')
        link = link.split('/')[2]
        image = item[0].get('src')
        if image == '/nick-assets/404.gif':
            image = R(ICON)
        else:
            image = image.split('?', 1)[0]
        title = item.get('title')
        dir.Append(Function(DirectoryItem(ShowList, title, thumb=image), image = image, pageUrl = link))
    return dir

####################################################################################################
def ShowList(sender, image, pageUrl):
    dir = MediaContainer(title2=sender.itemTitle, viewGroup='List')
    dir.Append(Function(DirectoryItem(VideoList, title="Full Episodes", thumb=image), clip="full episodes", image=image, pageUrl=pageUrl))
    dir.Append(Function(DirectoryItem(VideoList, title="Clips", thumb=image), clip="clips", image=image, pageUrl=pageUrl))
    return dir

####################################################################################################
def VideoList(sender, clip, image, pageUrl):
    dir = MediaContainer(title2=sender.itemTitle, viewGroup='InfoList')
    if clip == 'clips':
        url = AJAX_CLIP % (pageUrl)
    else:
        url = AJAX_FULL % (pageUrl)
    content = HTML.ElementFromURL(url).xpath("//ul[@class='large-grid-list clearfix']//li/div")
    if not content:
        return MessageContainer("No " + clip + " available", ("Sorry, there are no " + clip + " available."))
    for item in content:
        title = item.xpath('.//div[2]/h4')[0].text
        if '"' in title:
            title = title.split('"')[1].replace('"', '')
        summary = item.xpath('.//div[@class="col2"]/p')[0].text
        link = VIDEO_PLAYER + item.xpath('.//div')[0].text
        thumb = item.xpath('./a/img')[0].get('src')
        thumb = thumb.split('?', 1)[0]
        dir.Append(WebVideoItem(url=link, title=title, thumb=thumb, summary=summary))
    return dir