[app]
title = GWaken Sleep Monitor
package.name = g_waken
package.domain = com.anomalyai

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json

version = 1.0.0
requirements = python3, kivy==2.1.0, flask, requests, pybluez

# 包含sleep_monitor模块
source.exclude_dirs = .git, .svn, .hg

[buildozer]
log_level = 2

# Android特定设置
android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, ACCESS_FINE_LOCATION, WAKE_LOCK, RECEIVE_BOOT_COMPLETED, INTERNET
android.api = 27
android.minapi = 21
android.ndk = 23b
android.sdk = 30

# 图标和启动画面
android.application.name = GWaken
android.icon.filename = %(source.dir)s/assets/icons/icon.png
android.presplash.filename = %(source.dir)s/assets/icons/splash.png
android.presplash.color = 0xffffff

# 使用SDL2引导
android.bootstrap = sdl2

# 允许访问外部存储
android.add_compile_options = --add-opens=java.base/java.lang=ALL-UNNAMED