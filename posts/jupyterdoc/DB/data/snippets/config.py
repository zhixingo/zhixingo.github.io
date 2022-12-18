execute=True

snippets_config={
  'update':[
    {
      "name" : "解决matplotlib中文乱码",
      "code" : [
          "plt.rcParams['font.sans-serif']=['SimHei']",
          'plt.rcParams["axes.unicode_minus"]=False'
      ]
    },
    {
      "name" : "重新加载模块",
      "code" : [
          "# 重新加载所有模块",
          "%load_ext autoreload",
          "%autoreload 2"
      ]
    }
  ],
}
'''
snippets_config={
  'delete':[
    '解决matplotlib中文乱码','重新加载模块',
  ]
}
'''