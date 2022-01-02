weather_url = "https://tianqiapi.com/api.php?style=tb&skin=pitaya&city=%E5%8D%97%E4%BA%AC";

const check_url = function (url) {
  const promise = new Promise(function (resolve, reject) {
    if (!url) reject('无效路径');
    $.ajax({
      url: url,
      type: 'GET',
      dataType: "jsonp", //跨域采用jsonp方式
      complete: (response)=> {
        if(response.status==200)
          resolve(true)
        else
          resolve(false)
      }
    });
  });
  return promise;
}

var hid1 = document.getElementById("hid1");
var hid1_p = hid1.getElementsByTagName("p")[0];
check_url(weather_url).then(res=>{
  if(res){
      hid1.innerHTML = '<iframe scrolling="no" src="'+ weather_url +'" frameborder="0" width="350" height="24" allowtransparency="true"></iframe>';
  }else {
      hid1_p.innerHTML = "天气获取失败，请检查网络！";
  }
});