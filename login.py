# -*- coding=utf-8 -*-
# @Time:2024/12/26 14:47
# @Author:席灏铖
# @File:login.PY
# @Software:PyCharm‘


import streamlit as st
from user_data_storage import credentials, write_credentials, storage_file, Credentials
from webui import main

# 初始化会话状态
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'admin' not in st.session_state:
    st.session_state.admin = False
if 'usname' not in st.session_state:
    st.session_state.usname = ""


# 登录页面
def login_page():
    with st.container():
        # 添加自定义字体和精致的标题
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');
            .login-title {
                font-family: 'Poppins', sans-serif;
                text-align: center;
                color: #4C9B97;
                font-size: 36px;
                margin-bottom: 20px;
                letter-spacing: 1.2px;
            }
            .input-box {
                font-family: 'Poppins', sans-serif;
                background-color: #f4f4f9;
                border: 1px solid #ddd;
                padding: 12px;
                border-radius: 8px;
                font-size: 16px;
            }
            .submit-btn {
                background-color: #4C9B97;
                color: white;
                border-radius: 8px;
                padding: 12px;
                width: 100%;
                font-size: 16px;
                cursor: pointer;
            }
            .submit-btn:hover {
                background-color: #3e8e7e;
            }
        </style>
        """, unsafe_allow_html=True)

        # 标题使用自定义字体
        st.markdown("<h1 class='login-title'>🔐 欢迎回来！请登录</h1>", unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("👤 用户名", value="", placeholder="请输入用户名", max_chars=30, key="username",
                                     label_visibility="collapsed", help="用户名应为英文或数字")
            password = st.text_input("🔑 密码", value="", type="password", placeholder="请输入密码", max_chars=30,
                                     key="password", label_visibility="collapsed", help="请输入您的密码")
            submit = st.form_submit_button("登录", use_container_width=True, help="点击登录")

            if submit:
                user_cred = credentials.get(username)
                if user_cred and user_cred.password == password:
                    st.success("🎉 登录成功！")
                    st.session_state.logged_in = True
                    st.session_state.admin = user_cred.is_admin
                    st.session_state.usname = username
                    st.experimental_rerun()
                else:
                    st.error("❌ 用户名或密码错误，请重新输入。")


# 注册页面
def register_page():
    with st.container():
        # 添加自定义字体和精致的标题
        st.markdown("""
        <style>
            .register-title {
                font-family: 'Poppins', sans-serif;
                text-align: center;
                color: #4C9B97;
                font-size: 36px;
                margin-bottom: 20px;
                letter-spacing: 1.2px;
            }
        </style>
        """, unsafe_allow_html=True)

        # 标题使用自定义字体
        st.markdown("<h1 class='register-title'>📝 创建新账户</h1>", unsafe_allow_html=True)

        with st.form("register_form"):
            new_username = st.text_input("👤 设置用户名", value="", placeholder="请输入用户名", max_chars=30,
                                         key="new_username", label_visibility="collapsed")
            new_password = st.text_input("🔑 设置密码", value="", type="password", placeholder="请输入密码",
                                         max_chars=30, key="new_password", label_visibility="collapsed")
            register_submit = st.form_submit_button("注册", use_container_width=True)

            if register_submit:
                if new_username in credentials:
                    st.error("❌ 用户名已存在，请使用其他用户名。")
                else:
                    new_user = Credentials(new_username, new_password, is_admin=False)
                    credentials[new_username] = new_user
                    write_credentials(storage_file, credentials)
                    st.success(f"🎉 用户 {new_username} 注册成功！请登录。")
                    st.experimental_rerun()


# 侧边栏导航
def sidebar():
    st.sidebar.markdown("""
    <style>
        .sidebar-title {
            font-family: 'Poppins', sans-serif;
            color: #4C9B97;
            font-size: 30px;
            text-align: center;
            letter-spacing: 1px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<h2 class='sidebar-title'>导航栏</h2>", unsafe_allow_html=True)
    app_mode = st.sidebar.radio(
        "选择操作",
        options=["登录", "注册"],
        index=0,
        format_func=lambda x: "🔑 登录" if x == "登录" else "📝 注册",
        key="nav_radio",
        label_visibility="collapsed"
    )
    return app_mode


# 主界面布局
if __name__ == "__main__":
    # 还未登录，展示登录或注册页面
    if not st.session_state.logged_in:
        app_mode = sidebar()
        if app_mode == "登录":
            login_page()
        elif app_mode == "注册":
            register_page()
    else:
        # 登录后显示欢迎信息和角色信息
        st.sidebar.success(f"欢迎回来, {st.session_state.usname}!")
        st.sidebar.markdown(
            f"<p style='font-size: 16px; color: #777;'>您已登录为{'管理员' if st.session_state.admin else '普通用户'}。</p>",
            unsafe_allow_html=True,
        )
        # 显示主界面
        main(st.session_state.admin, st.session_state.usname)

