import license

from selenium import webdriver
from pubfun import *

chrome_options = webdriver.chrome.options.Options()
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--window-size=1440,800")
print("是否显示浏览器窗口？")
if input("输入\"true\"显示, 其他值不显示\n") != "true":
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--mute-audio")
else:
    print("是否静音？")
    if input("输入\"false\"不静音, 其他值静音\n") != "false":
        chrome_options.add_argument("--mute-audio")

browser = None

print("初始化浏览器...")
try:
    browser = webdriver.Chrome(options=chrome_options)
except Exception as e:
    print("Error: " + str(e))
    errExit("初始化浏览器失败！请检查是否已安装Chrome浏览器和ChromeDriver！")

from configure import *

print("加载优慕课")
try:
    browser.get(umooc_link)
except Exception as e:
    print("Error: " + str(e))
    errExit("优慕课加载失败！请检查优慕课链接输入是否正确！")
print("发送登录请求...")
try:
    clickElemById(browser, "loginbtn")
    inputElemById(browser, "userName", umooc_username)
    inputElemById(browser, "passWord", umooc_password)
    browser.find_element_by_class_name("login-button").find_elements_by_class_name("submit")[0].click()
except Exception as e:
    print("Error: " + str(e))
    errExit("登录失败！请检查优慕课链接输入是否正确！")
sleep(1)

# 检查登陆是否成功
try:
    temp = browser.find_element_by_class_name("logoutbut")
except:
    errExit("登录失败")

print("登录成功")

print("获得课程列表...")
browser.get(umooc_link + "personal.do?menuId=0")
sleep(click_wait_time)
browser.find_element_by_class_name("courselist") \
    .find_element_by_class_name("courselistbody") \
    .find_element_by_class_name("courseborder") \
    .find_element_by_class_name("title") \
    .find_element_by_tag_name("span") \
    .find_element_by_tag_name("a").click()
browser.get(browser.find_element_by_id("main").get_attribute("src"))

courseList = []
for i in browser.find_element_by_tag_name("table").find_elements_by_tag_name("a"):
    iclass = i.get_attribute("class").split(" ")
    if hasElem(iclass, "moveup"):
        pass
    elif hasElem(iclass, "movedown"):
        pass
    else:
        courseList.append(i)

for i in range(len(courseList)):
    print(str(i) + "." + courseList[i].text)

courseNum = -1

while True:
    inp = input("请输入课程序号: ")
    if inp == "exit":
        sys.exit(0)
    try:
        courseNum = int(inp)
    except:
        pass
    if courseNum in range(len(courseList)):
        break
    else:
        print("输入错误，请重试")

# http://jpkc.bcu.edu.cn/meol/
browser.get(umooc_link +
            courseList[courseNum].get_attribute("onclick").split("window.open('")[1].split("','")[0].split("../")[1])
sleep(click_wait_time)

removeUselessElem(browser)

nav_name = ""
navs = browser.find_element_by_class_name("nav").find_elements_by_tag_name("li")
print("模块列表")

for i in range(len(navs)):
    print(str(i) + "." + navs[i].text)

while True:
    moduleNum = -1
    inp = input("请输入模块序号: ")
    if inp == "exit":
        sys.exit(0)
    try:
        moduleNum = int(inp)
    except:
        pass
    if moduleNum in range(len(navs)):
        nav_name = navs[moduleNum].text
        break
    else:
        print("输入错误，请重试")

clickNav(browser, nav_name)
sleep(click_wait_time)
left_menu = browser.find_elements_by_xpath(
    "//*[@id=\"menu\"]/ul[not(contains(@style,'display:none;')) and not(contains(@style,'display: none;'))]/li")
left_menu_sel = []
print("单元列表:")

for i in range(len(left_menu)):
    print(str(i) + "." + left_menu[i].text)

while True:
    moduleNum = -1
    inp = input("请输入单元序号:\n多个单元请用英文\",\"隔开，全部请输入\"all\"\n")
    if inp == "exit":
        sys.exit(0)
    elif inp == "break":
        break
    elif inp == "all":
        left_menu_sel = left_menu
        break
    else:
        try:
            inputList = inp.split(",")
            for i in inputList:
                left_menu_sel.append(left_menu[int(i)])
            break
        except:
            print("输入错误，请重试")

loopNum = -1
while True:
    inp = input("请输入循环次数(1-9999)：")
    if inp == "exit":
        sys.exit(0)
    try:
        loopNum = int(inp)
    except:
        pass
    if loopNum in range(10000):
        break
    else:
        print("输入错误，请重试")

print("#" * 20)
print("准备就绪，请在继续前确认配置\n")
print("选择的模块:", nav_name)
print("选择的单元:")

for i in range(len(left_menu_sel)):
    print(str(i + 1) + "." + left_menu_sel[i].text)

print("循环次数:", loopNum)
print("#" * 20)
input("按回车继续, 按Ctrl+C终止")
print("进入主循环")

count = 0
problem = 0
for i in range(loopNum):
    count = count + 1
    print(("=" * 10) + "开始第" + str(count) + "次循环")
    try:
        print("进入: " + nav_name)
        clickNav(browser, nav_name)
        # /html/body/div[3]/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/ul[1]
        # //*[@id="menu"]/ul[2]
        for i in left_menu_sel:
            iname = i.text
            print("\n" + ("=" * 10) + "\n节点: " + iname)
            browser.execute_script("arguments[0].scrollIntoView(true);", i)
            i.click()
            sleep(click_wait_time)
            checkFrame(browser)
            childLe3 = []
            try:
                childLe3 = i.find_element_by_tag_name("ul").find_elements_by_tag_name("li")
            except:
                print("节点\"" + iname + "\"无子节点")
            for j in childLe3:
                if hasElem(j.find_element_by_tag_name("a").get_attribute("class").split(" "), "le3"):
                    jname = j.text
                    print("\n" + ("=" * 10) + "\n节点: " + iname + " > " + jname)
                    browser.execute_script("arguments[0].scrollIntoView(true);", j)
                    browser.execute_script(
                        "scrollTop=document.documentElement.scrollTop||document.body.scrollTop;scrollTo(0,scrollTop-50);")
                    j.click()
                    sleep(click_wait_time)
                    print("当前主循环次数: ", count)
                    checkFrame(browser)
                    childLe4 = []
                    try:
                        childLe4 = j.find_element_by_tag_name("ul").find_elements_by_tag_name("li")
                    except:
                        print("节点\"" + jname + "\"无子节点")
                    for k in childLe4:
                        kname = k.text
                        print("\n" + ("=" * 10) + "\n节点: " + iname + " > " + jname + " > " + kname)
                        browser.execute_script("arguments[0].scrollIntoView(true);", k)
                        k.click()
                        sleep(click_wait_time)
                        print("当前主循环次数: ", count)
                        checkFrame(browser)
            sleep(click_wait_time)
            clickNav(browser, nav_name)
    except Exception as e:
        print("第" + str(count) + "次循环出现问题")
        print("异常原因", e)
        problem = problem + 1
    print("问题计数:", problem)
    sleep(3)

print("程序完成运行")
browser.close()
input("按回车退出。。。")
