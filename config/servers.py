#!/usr/bin/env python
# -*- coding: utf-8 -*-


username1 = "username-1"
password1 = "password-1"

username2 = "username-2"
password2 = "password-2"

username3 = "username-3"
password3 = "password-3"

username4 = "username-4"
password4 = "password4"

servers = {
	"server-name-1": {
		"ip": "x.x.x.x", 
		"username": username1,
		"password": password1
	},

	"server-name-2": {
		"ip": "x.x.x.x",
		"username": username2,
		"password": password2
	},

	"server-name-3": {
		"ip": "x.x.x.x",
		"username": username3,
		"password": password3
	},

	"server-name-4": {
		"ip": "x.x.x.x",
		"username": username4,
		"password": password4
	},

}

__all__ = [servers]
