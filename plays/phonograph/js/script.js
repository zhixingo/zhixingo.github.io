let b = document.body;
let a = document.querySelector("#audio");


let radio = document.querySelector("#radio")
let playert = document.querySelector("#playert")
let disc = document.querySelector("#disc")
let control = document.querySelector("#control")
let needle = document.querySelector("#needle")
let shadows = document.querySelector("#shadows")
let shadowsb = document.querySelector("#shadowsb")
let shadowsc = document.querySelector("#shadowsc")

let sca = document.querySelectorAll(".speaker-ca");
let scb = document.querySelectorAll(".speaker-cb");


let sfa = document.querySelectorAll(".speaker__front");
let sta = document.querySelectorAll(".speaker__top");
let sba = document.querySelectorAll(".speaker__back");
let sla = document.querySelectorAll(".speaker__left");
let sra = document.querySelectorAll(".speaker__right");

var source = a.getElementsByTagName("source")[0]
/*******************/

let tf = () => {
    radio.classList.toggle('is-radio-active')
    playert.classList.toggle('is-playert-active')
    disc.classList.toggle('is-disc-active')
    control.classList.toggle('is-control-active')
    needle.classList.toggle('is-needle-active')
    shadows.classList.toggle('is-shadows-active')
    shadowsb.classList.toggle('is-shadowsb-active')
    shadowsc.classList.toggle('is-shadowsc-active')

    sca.forEach( f => f.classList.toggle("is-sca-active") );
    scb.forEach( f => f.classList.toggle("is-scb-active") );


    sfa.forEach( f => f.classList.toggle("sfa") );
    sta.forEach( f => f.classList.toggle("sta") );
    sba.forEach( f => f.classList.toggle("sba") );
    sla.forEach( f => f.classList.toggle("sla") );
    sra.forEach( f => f.classList.toggle("sra") );
}

let af = () => {
    a.loop = true;

    if (a.paused) a.play();
    else {
        a.pause();
        a.currentTime = 0;
    }

}


let radioPlaying = () => {
    tf()
    af()
}

/*******************/
b.addEventListener("click", radioPlaying)

function initial_audio() {
    var url = location.search
    if (url.indexOf("?") != -1) {
        var r = new Object()
        var para = url.split("?")[1]
        para = para.split("&")
        for(var i = 0; i < para.length; i++) {
            r[para[i].split("=")[0]]=unescape(para[i].split("=")[1])
        }
        source.setAttribute("src", r['url'])
        a.load()
    }
}
initial_audio()