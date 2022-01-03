//接口说明见https://github.com/muggledy/iper

var hid7 = document.getElementById("hid7");
var hid7_p = hid7.getElementsByTagName("p")[0];

fetch("https://iper.vercel.app/api/index").then(function(data){
        return data.text();
    }).then(function(data){
        data = eval("(" + data + ")");
        var ul = document.createElement("ul");
        ul.className = "ul";
        hid7.insertBefore(ul, hid7_p);
        hid7.removeChild(hid7_p);
        var items = ["query", "city", "timezone"];
        var names = ["IP地址", "所在城市", "时区"];
        for (var i = 0; i < items.length; ++i){
            var li = document.createElement("li");
            var info;
            if(items[i] == "city"){
                info = "<a href='https://www.google.com/search?q=" + data[items[i]] + "' target=\"_blank\">" +
                data[items[i]] +"</a>";
            }else{
                info = data[items[i]];
            }
            li.innerHTML = names[i] + ": " + info;
            ul.appendChild(li);
        }
}).catch(error => hid7_p.innerHTML = "IP获取失败，请检查网络！"); //https://juejin.cn/post/6844904193996619784