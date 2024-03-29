import sys
from time import sleep
from configure import *


def errExit(s):
    print(s)
    input("按回车退出")
    sys.exit(1)


def clickNav(browser, nav_name):
    nav = browser.find_element_by_class_name("nav").find_element_by_partial_link_text(nav_name)
    browser.execute_script("scrollTo(0,0);");
    nav.click()
    sleep(click_wait_time)


def hasElem(list, elem):
    for i in list:
        if i == elem:
            return True
    return False


def clickElemById(browser, id):
    browser.find_element_by_id(id).click()
    sleep(click_wait_time)


def clickElemByLinkText(browser, s):
    browser.find_element_by_partial_link_text(s).click()
    sleep(click_wait_time)


def inputElemById(browser, id, value):
    browser.find_element_by_id(id).send_keys(value)


def checkFrame(browser):
    browser.switch_to.frame(browser.find_element_by_id("mainFrame"))
    try:
        contentFrame = browser.find_element_by_id("main-content-two")
        addr = contentFrame.get_attribute("src")
        addrs = addr.split("/")
        addr = addrs[len(addrs) - 1].split("?")[0]
        if addr == "microLessonView.do":
            print("视频节点")
            browser.switch_to.frame(contentFrame)
            checkVideoFrame(browser)
        elif addr == "resFolderViewList.do":
            if (openAndWaitLink_wait_time == 0):
                print("文件或文件夹节点，跳过")
                sleep(unknown_wait_time)
            else:
                print("文件或文件夹节点，开始遍历")
                browser.switch_to.frame(contentFrame)
                checkFolderFrame(browser)
        elif addr == "colUrlStuView.do":
            print("疑似空节点，跳过")
            sleep(colUrlStuView_wait_time)
        elif addr == "thread.jsp":
            print("话题讨论，跳过")
            sleep(thread_wait_time)
        elif addr == "list.jsp" and addrs[len(addrs) - 3] == "test":
            print("在线测试，跳过")
            sleep(test_wait_time)
        else:
            print("未知节点(" + addr + ")，跳过")
            sleep(unknown_wait_time)
    except BaseException as e:
        browser.switch_to.default_content()
        print("该节点无内容")
        print(e)
    browser.switch_to.default_content()


def checkVideoFrame(browser):
    elemMenu = browser.find_element_by_id("content_min").find_element_by_id("descrip").find_elements_by_tag_name(
        "li")
    elemCount = len(elemMenu)
    print("共" + str(elemCount) + "个标签")
    videoMenu = []
    for i in elemMenu:
        videoMenuElemType = i.find_element_by_tag_name("a").get_attribute("class")
        if videoMenuElemType == "type_1":
            videoMenu.append(i)
    videoCount = len(videoMenu)
    print("共" + str(videoCount) + "个视频")
    for i in range(videoCount):
        print("打开第" + str(i + 1) + "个视频")
        videoMenuElem = videoMenu[i]
        videoMenuElem.click()
        sleep(video_load_wait_time)
        videoPlayer = browser.find_element_by_id("resAct_min").find_element_by_id("video") \
            .find_element_by_tag_name("video")
        videoDuration = browser.execute_script("return arguments[0].duration;", videoPlayer)
        print("当前视频时长: " + str(videoDuration))
        lastCurrentTime = 0
        while True:
            currentTime = browser.execute_script("return arguments[0].currentTime;", videoPlayer)
            print("\r已播放: " + str(currentTime), end="")
            if videoDuration == currentTime:
                break
            else:
                lastCurrentTime = currentTime
                sleep(video_check_time)
            if lastCurrentTime - currentTime == 0 and videoDuration - currentTime < 1:
                break
        print("\n第" + str(i + 1) + "个视频播放完成")
    print("当前节点视频全部播放完成")


def checkFolderFrame(browser):
    folderTable = browser.find_element_by_id("postform").find_element_by_tag_name("table")
    elems_tr = folderTable.find_elements_by_tag_name("tr")
    names = []
    links = []
    for i in range(1, len(elems_tr)):
        e = elems_tr[i]
        elem_a = e.find_element_by_tag_name("a")
        names.append(elem_a.get_attribute("innerText"))
        links.append(elem_a.get_attribute("href"))
    print("共 {} 个资源".format(len(links)))
    for i in range(len(links)):
        print("开始处理 {}".format(names[i]))
        openAndWaitLink(browser, links[i])


def openAndWaitLink(browser, link):
    sc = 'window.open("' + link + '")'
    browser.execute_script(sc)
    browser.switch_to_window(browser.window_handles[1])
    print("在新标签页中打开 {}".format(link))
    print("等待 {} 秒后继续".format(openAndWaitLink_wait_time))
    sleep(openAndWaitLink_wait_time)
    browser.close()
    print("新标签页关闭")
    browser.switch_to_window(browser.window_handles[0])


def removeUselessElem(browser):
    browser.execute_script("return document.getElementsByClassName('feamenu')[0].remove();")
    browser.execute_script("return document.getElementsByClassName('bdshare-slide-button-box')[0].remove();")
    browser.execute_script("return document.getElementById('xuboxer').remove();")
