//获取ip信息
//调用IP Geolocation API接口，官网：http://ip-api.com/
var ip_url = "http://ip-api.com/json/?callback=show_ip";
function show_ip(data){
    var hid7 = document.getElementById("hid7");
    var p = hid7.getElementsByTagName("p")[0];
    var ul = document.createElement("ul");
    ul.className = "ul";
    hid7.insertBefore(ul, p);
    hid7.removeChild(p);
    var items = ["query", "city", "timezone"];
    var names = ["IP地址", "所在城市", "时区"];
    for (var i = 0; i < items.length; ++i){
        var li = document.createElement("li");
        var info;
        if(items[i] == "city"){
            info = "<a href='https://www.google.com/search?q=" + data[items[i]] + "' target=\"_blank\">" + data[items[i]] +"</a>";
        }else{
            info = data[items[i]];
        }
        li.innerHTML = names[i] + ": " + info;
        ul.appendChild(li);
    }
}
var ip_script = document.createElement("script");
ip_script.setAttribute("src", ip_url);
document.getElementsByTagName("head")[0].appendChild(ip_script);