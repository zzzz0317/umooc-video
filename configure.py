click_wait_time = 1
video_load_wait_time = 3
video_check_time = 3
mainloop_wait_time = 5

resFolderViewList_wait_time = 0
colUrlStuView_wait_time = 0
thread_wait_time = 0
test_wait_time = 0
unknown_wait_time = 0

# umooc_link = "http://jpkc.bcu.edu.cn/meol/index.do"
umooc_link = "http://jpkc.bcu.edu.cn/meol/"
input_umooc = input("请输入学校优慕课链接\n"
                    "（如：http://jpkc.bcu.edu.cn/meol/\n"
                    "输入不正确会导致后续程序运行出现问题，留空默认为北京城市学院在线教育综合平台）：\n")
if (input_umooc == ""):
    print("已默认选择：北京城市学院在线教育综合平台")
else:
    umooc_link = input_umooc
umooc_username = input("优慕课用户名:\n")
umooc_password = input("优慕课密码:\n")
