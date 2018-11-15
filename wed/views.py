# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import paramiko



def exec_command(comm):
    hostname = "xxxxx"    #ip
    username = "xxxxx"   #用户名
    password = "xxxxxxxxxx"   #密码

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(comm)
    result = stdout.read()
    ssh.close()
    return result


@accept_websocket
def index(request):

    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['input']
            return HttpResponse(message)
        except:
            return render(request, 'index.html')
    else:
        for message in request.websocket:
            # 通过页面的message传递参数
            cmd = message
            command = cmd #这里是要执行的命令或者脚本
            request.websocket.send(exec_command(command))  # 发送消息到客户端

