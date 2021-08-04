alfred-workflow-in-python-tutorial
==============================================================================

.. contents::
    :depth: 1
    :local:


MacOS 上的神软 Alfred
------------------------------------------------------------------------------

`Alfred <https://www.alfredapp.com/>`_ 是 MacOS 平台上的一款生产力软件. 有些人称之为快速启动器.


Alfred Workflow 简介
------------------------------------------------------------------------------

- Trigger: 如何触发这个 workflow, 通常是以 keyword 的形式触发
- Input (重要): workflow 的输入, 通常是 keyword 之后的 argument
- Output: 从前一个单元的输出, 可以选择对它做一些事情
- Action: 对输出的 item 的 argument 所进行的操作, 例如打开文件, 在浏览器中打开


Script Filter 介绍
------------------------------------------------------------------------------

Script Filter 是 Alfred Workflow 中的一种 Input, 可以接受 argument 为输入, 作为参数传给任意编程语言的 script 作为参数, 然后返回输出.

这种输入输出模型使得 Alfred Workflow 几乎可以做任何事.

根据这篇文档 https://www.alfredapp.com/help/workflows/inputs/script-filter/json/, 输出需要以 JSON 的形式 被发送到 sys.stdout 中, 然后 Alfred 会根据这个 JSON 渲染 dropdown menu, 以及定义你按下 Tab / Enter / Alt / Cmd 等键的行为.


Alfred Workflow 的核心原理
------------------------------------------------------------------------------

首先我们来理解 Alfred 是如何与用户交互的. 我们以下图为例:

.. image:: https://user-images.githubusercontent.com/6800411/126883941-e0f9e64a-b80b-43f4-85bf-a61d38623c20.png

1. 匹配 Alfred Keyword: 首先用户输入关键字, 在本例中关键字是 fts movie. 在输入关键字时, Alfred 会将用全文搜索搜索所有软件内定义过的关键字, 提示用户可能的命令, 并提供 Tab 自动补全功能.
2. 匹配到关键字后, 你可以直接输入回车, 或是输入一些 参数 (Query). 然后 Alfred 会对 Query 进行处理, 返回一些 Item. 你可以对 Item 进行选择, 或者进行下一步的操作. 而这些操作背后对应的行为, 你可以在 Alfred Workflow 中进行定义, 比如打开文件, 打开浏览器.

**重点**

对于开发而言, 最重要的是理解 编程模型中的 输入 和 输出. 在这个例子里可以很清晰的看到.

输入:

- 关键字 Keyword: fts movie
- 参数 Query: Drama

输出:

一些 Item, 每个 Itenm 都有这些元素:

- 标题 Title: 也就是大写的部分
- 副标题 Subtitle: 也就是小字的部分
- 自动补全 Auto Complete: 这部分是看不到的, 是你按下 Tab 键自动补全出来的字符串
- 参数 Arg: 这部分也是看不到的, 是你按下 Enter 回车确定后传递给下一个操作的参数, 也是一个字符串
- 图标 Icon: 本例中没有, 也就是左边的图标.

理解了这个编程模型, 我们编程的重点则是编写一个函数, 能够根据输出, 返回正确的输出, 并且包括这种错误情况的处理.


用 Python2 开发 Alfred Workflow
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

我们来试着用 Python2 编写一个用于生成随机密码的工具.

用 Python 开发 Alfred Workflow 的难点
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 苹果电脑上自带的 Python 是 Python2. 虽然 Alfred 可以用 Python3 作为 Workflow 的运行时, 但是对于用户而言为了使用 Workflow 来配置 Python 环境是不现实的. 你的 Workflow 的使用者不一定会正确的在 Mac 上配置 Python 环境. **所以你只能用 Mac 上自带的 Python 开发**, 而为系统自带的 Python 安装第三方库的行为本身是很危险的. **这也会使得使用在 Alfred Workflow 中使用第三方库变得非常麻烦**.
2. 功能测试困难.
3. 集成测试困难. 就算你确定你的功能测试 100% 没问题, 但是你最终还是希望能够在 Alfred 中实际使用你的 Workflow.


创建 Python2.7 虚拟环境
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

为了开发调试方便, 我们还是要使用 python2.7 创建一个 virtualenv 用来开发, 并使用我们习惯的 IDE 来开发和测试.

这里我们有一个脚本

.. code-block:: bash

    # 创建虚拟环境
    bash ./bin/venv-up.sh

    # 安装你的 workflow python library 本身为 editable 模式
    # 以及必备的 Alfred-Workflow
    bash ./bin/pip-dev-install

    # 进入虚拟环境
    source ./venv/bin/activate

    # 如果使用的是 Pycharm, 运行下面脚本, 找到 Virtualenv 的 Python 解释器的绝对路径
    # 在 Pycharm 中配置好 Python Interpreter
    bash ./bin/info.sh


进行本地开发, 编写测试
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**编写功能单元**:

跟 alfred 的主逻辑相关的功能性单元, 建议放在其他模块中, 比如本例中我们把根据密码长度生成密码的逻辑实现放在了 ``afwf_rand_pass/helpers.py`` 里.

这样做的目的是将 workflow 的主逻辑代码以及功能性单元代码分开. 方便测试功能性单元代码, 以及减少 workflow 主逻辑代码量, 方便维护.

最后在 ``tests/test_helpers.py`` 中进行功能单元测试.

**编写workflow主逻辑**:

请仔细阅读 ``afwf_rand_pass/handlers.py``

**测试workflow主逻辑**:

在 ``afwf_rand_pass.handlers.handler`` 的主函数中 有一个可选参数 ``args``, 是一个 字符串列表. 用户可以在 Python 测试框架中使用 args 来传递输入, 而用 ``Workflow3._items`` 来捕获输出. 从而对输入输出的各种排列组合进行测试.

**在 Alfred 中进行直接测试**:

在 Alfred 中创建一个 Workflow, 并创建一个 Script Filter Input, 然后按照下图的设置配置. 注意! 这里我们使用的是 virtualenv 中的 Python 以及项目中的 main.py 文件运行的 workflow. 而最终发布时我们需要对其重新打包, 并且依赖库所放置的文件夹方式也不相同. 打包部分我们交给后面的 shell script 完成.

.. image:: ./alfred-script-filter-config-1.png

.. image:: ./alfred-script-filter-config-2.png

值得注意的是, 在 main.py 文件中我们用把输出的 argument 和 输出的 json 都写入到项目目录下的 wf-input.json 和 wf-output.json 文件中了. 这样使得开发者在用 alfred 输入命令后, 能在这两个文件中看到 Python 获得的输入和输出数据, 便于调试.


在本地构建 Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

首先在 Alfred Workflow 的界面的左边选择你的 Workflow, 并右键点击 -> Open in Finder 在文件夹中打开. 然后将该文件夹路径拷贝, 这是你实际的 Alfred Workflow 所在的目录, 路径类似于 ``/path-to/Alfred.alfredpreferences/workflows/user.workflow.A123B456-C123-4567-8910-ABCDEFGHIJKL``

然后打开 ``./bin/build-wf.sh`` 将该路径粘贴到 ``dir_workflow`` 变量中, 然后运行. 其原理是在指定路径下, 清楚并构建 ``./lib``, ``./workflow``, ``./main.py``.

最后在 Alfred Workflow 中的界面中打开 Script Filter, 将命令行命令替换为如下, 使用系统的 Python 而不是 Virtualenv 中的 Python 即可. (你的用户可不会用 Virtualenv)

.. code-block:: bash

    /usr/bin/python main.py {query}


发布你的 Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 创建一个跟你的版本号一致的 Branch
2. 在本地的 Alfred Workflow 中, 右键点击你的 Workflow, 选择 Export
3. 在 Github 上创建一个 Release, 从 Branch 发布, 然后手动上传刚才 Export 的 ``your-workflow-name.alfredworkflow`` 文件即可.


项目模板
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

本项目可以作为一个模板

1. 修改 ``afwf_rand_pass`` 文件夹名, 这是你的 workflow 的 python library 的名称, 你可以改成你的 library 的名字
2. 修改 ``setup.py`` 里的 ``import afwf_rand_pass as package``, 改成你的 library 的名字
3. 修改 ``requirements.txt`` 里你所需要的依赖包
4. 修改所有包含 ``import afwf_rand_pass ...`` 相关的代码. 包括 main 以及 tests 里的.
