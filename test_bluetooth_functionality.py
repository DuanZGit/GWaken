#!/usr/bin/env python3
"""
测试蓝牙功能可用性
"""
import bluetooth
import json
from datetime import datetime


def test_bluetooth_imports():
    """测试蓝牙库导入"""
    print("PyBluez imported successfully")
    print(f"Available socket types: RFCOMM={bluetooth.RFCOMM}, L2CAP={bluetooth.L2CAP}")
    print(f"Heart Rate Service UUID: {bluetooth.UUID_SERVICES['180d'] if '180d' in bluetooth.UUID_SERVICES else '0000180d-0000-1000-8000-00805f9b34fb'}")
    return True


def test_device_search():
    """测试设备搜索功能"""
    print("\n测试蓝牙设备搜索...")
    try:
        print("正在搜索蓝牙设备（2秒）...")
        nearby_devices = bluetooth.discover_devices(
            duration=2,
            lookup_names=True,
            flush_cache=True
        )
        
        print(f"找到 {len(nearby_devices)} 个设备:")
        for addr, name in nearby_devices:
            print(f"  - {name}: {addr}")
        
        return nearby_devices
        
    except bluetooth.btcommon.BluetoothError as e:
        print(f"蓝牙错误: {e}")
        print("这通常是由于没有物理蓝牙适配器或蓝牙服务未启动")
        return []
    except OSError as e:
        print(f"系统错误: {e}")
        print("容器环境通常没有物理蓝牙适配器")
        return []


def test_socket_creation():
    """测试蓝牙套接字创建"""
    print("\n测试蓝牙套接字创建...")
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print("蓝牙套接字创建成功")
        sock.close()
        return True
    except Exception as e:
        print(f"创建蓝牙套接字失败: {e}")
        return False


def simulate_redmi_band_connection():
    """模拟红米手环连接流程"""
    print("\n模拟红米手环2连接流程...")
    
    # 模拟设备搜索
    print("1. 搜索设备...")
    devices = test_device_search()
    
    # 检查是否有红米设备
    redmi_devices = []
    for addr, name in devices:
        if 'Redmi' in name or 'Mi Band' in name or 'Band' in name:
            redmi_devices.append((addr, name))
    
    if redmi_devices:
        print(f"找到 {len(redmi_devices)} 个红米手环设备:")
        for addr, name in redmi_devices:
            print(f"  - {name} ({addr})")
        
        # 模拟连接
        addr, name = redmi_devices[0]
        print(f"\n2. 连接到设备: {name} ({addr})")
        
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((addr, 1))  # 通道1是常用的
            print("3. 连接成功!")
            
            # 模拟数据读取
            print("4. 开始读取数据...")
            data = sock.recv(1024)
            print(f"接收到数据: {data}")
            
            sock.close()
            return True
            
        except Exception as e:
            print(f"连接失败: {e}")
            return False
    else:
        print("未找到红米手环设备")
        print("请确保:")
        print("  - 手环在蓝牙范围内")
        print("  - 手环蓝牙功能已开启")
        print("  - 手环未被其他设备连接")
        return False


def main():
    """主函数"""
    print("=== 红米手环2蓝牙连接功能测试 ===\n")
    
    # 测试基本导入
    test_bluetooth_imports()
    
    # 测试套接字创建
    test_socket_creation()
    
    # 测试设备搜索
    test_device_search()
    
    print("\n=== 测试完成 ===")
    print("注意: 如果在容器环境或无蓝牙适配器的系统中运行，")
    print("设备搜索会失败，这是正常现象。")


if __name__ == "__main__":
    main()