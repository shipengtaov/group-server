group-server
==============

#### ssh操作一组服务器

#### todo

* 插件扩展


#### 使用

* 帮助信息

		$ python run_cmd.py -h

* 对 group 里的每一个 server 批量执行命令

		$ python run_cmd.py -i

* -i 进入交互模式, 选择 group 后

	group 下的所有 server 执行 pwd 命令:

		pwd

	第 0 台 server 执行 pwd 命令:

		(0)pwd

	ip 为 1.2.3.4 的 server 执行 pwd 命令:

		(1.2.3.4)pwd

* 任意指定几台 server 并进入交互模式

		$ python run_cmd.py -s

* -s 进入交互模式后, 以 "," 作为分隔符选择需要操作的 server
