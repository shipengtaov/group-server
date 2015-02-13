#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import paramiko

import logging
import argparse

from config import servers, groups


def group_interactive():
	print "所有可选的 group:"
	list_groups()
	while True:
		group = raw_input("选择一个group(q or quit:退出, l:列出所有group):")
		if not group:
			continue
		if group == 'q' or group == 'quit':
			break
		if group == 'l' or group == 'list':
			list_groups()
			continue
		if not groups.groups.has_key(group):
			print "{0} group 不存在".format(group)
			continue
		else:
			group_loop(group)

def list_groups():
	for group in groups.groups.keys():
		print ' '*4 + '→ ' + group

def group_loop(group):
	group_servers = [servers.servers[i['server']] for i in groups.groups[group]]
	operate_servers(group_servers)

def servers_interactive():
	print "所有可选的 server:"
	list_servers()
	while True:
		group = raw_input("选择需要操作的server, 多个server以','分割\n(q or quit:退出, l:列出所有server): ").strip(' ,')
		if not group:
			continue
		elif group == 'q' or group == 'quit':
			break
		elif group == 'l' or group == 'list':
			list_servers()
			continue
		server_names = group.split(",")
		not_exist_servers = set(server_names) - set(servers.servers.keys())
		if not_exist_servers:
			print "server 不存在: {}".format(", ".join(not_exist_servers))
			continue
		else:
			group_servers = [servers.servers[i] for i in server_names]
			operate_servers(group_servers)

def list_servers():
	for server_name,item in servers.servers.items():
		print "{}→ {} : {}@{}".format(' '*4, server_name, item['username'], item['ip'])

def operate_servers(servers):
	ssh_clients = []
	for i in servers:
		ssh_client = {}
		ssh_client['ip'] = i['ip']
		client = None
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		print "正在连接 {0}".format(i['ip'])
		client.connect(i['ip'], username=i['username'], password=i['password'])
		ssh_client['ssh'] = client
		ssh_clients.append(ssh_client)
	while True:
		cmd = raw_input("\n输入需要执行的命令:\nq or quit:退出; l:列出当前所有server; (0)pwd: 第0台server执行pwd; (1.2.3.4)pwd: server为指定ip的执行pwd\n> ")
		if not cmd:
			continue
		if cmd == 'l' or cmd == 'list':
			for server in ssh_clients:
				print ' '*4 + '→ ' + server['ip']
			continue
		if cmd == 'q' or cmd == 'quit':
			for ssh in ssh_clients:
				ssh['ssh'].close()
			break
		# 指定某一台 server 执行命令
		# 比如: > (1.2.3.4)pwd
		ip_pattern = re.compile("^\(([^\)]*?)\).*$")
		ip_match = ip_pattern.match(cmd)
		if ip_match:
			match_server = ip_match.groups()[0]
			if len(match_server) >= 7:
				ip = match_server
			else:
				server_index = int(match_server)
				if server_index >= len(ssh_clients):
					print "指定的 server 不存在"
					continue
				ip = ssh_clients[server_index]['ip']
			print "指定 server: {0}".format(ip)
			cmd = cmd[len(match_server)+2:]
		else:
			ip = None
		print
		for ssh in ssh_clients:
			if ip and ssh['ip'] != ip:
				continue
			print '-'*20
			print ssh['ip']
			print "正在执行: {0}".format(cmd)
			print "执行结果:"
			print "↓"*10
			stdin, stdout, stderr = ssh['ssh'].exec_command(cmd)
			print stdout.read()
			print
		print

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", 
						dest="interactive_group", 
						action="store_true", 
						help=u"对每一个 group server 以交互式运行")
	parser.add_argument("-s",
						dest="interactive_servers",
						action="store_true",
						help=u"指定某几台 server, 以交互式运行")
	return parser.parse_args(), parser

def main():
	logging.basicConfig(level=logging.WARN,
						format='%(asctime)s %(levelname)-8s %(message)s',
						datefmt='%Y-%m-%d %H:%M:%S')
	args, parser = parse_args()
	if args.interactive_group:
		group_interactive()
	elif args.interactive_servers:
		servers_interactive()
	else:
		parser.print_help()

if __name__ == '__main__':
	main()
