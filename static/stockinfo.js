function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
a = httpGet("http://127.0.0.1:5000/")

a = JSON.parse(a)
document.getElementById("demo").innerHTML = "代號: " + a[0]["id"]
document.getElementById("demo1").innerHTML =  a[0]["price"]
document.getElementById("demo2").innerHTML =  a[0]["percent"]
document.getElementById("demo3").innerHTML =  a[0]["time"]
document.getElementById("demo4").innerHTML =  a[0]["name"]

document.getElementById("d").innerHTML = "代號: " + a[1]["id"]
document.getElementById("d1").innerHTML =  a[1]["price"]
document.getElementById("d2").innerHTML =  a[1]["percent"]
document.getElementById("d3").innerHTML =  a[1]["time"]
document.getElementById("d4").innerHTML =  a[1]["name"]

document.getElementById("de").innerHTML = "代號: " + a[2]["id"]
document.getElementById("de1").innerHTML =  a[2]["price"]
document.getElementById("de2").innerHTML =  a[2]["percent"]
document.getElementById("de3").innerHTML =  a[2]["time"]
document.getElementById("de4").innerHTML =  a[2]["name"]

document.getElementById("dem").innerHTML = "代號: " + a[3]["id"]
document.getElementById("dem1").innerHTML =  a[3]["price"]
document.getElementById("dem2").innerHTML =  a[3]["percent"]
document.getElementById("dem3").innerHTML =  a[3]["time"]
document.getElementById("dem4").innerHTML =  a[3]["name"]

document.getElementById("e").innerHTML = "代號: " + a[4]["id"]
document.getElementById("e1").innerHTML =  a[4]["price"]
document.getElementById("e2").innerHTML =  a[4]["percent"]
document.getElementById("e3").innerHTML =  a[4]["time"]
document.getElementById("e4").innerHTML =  a[4]["name"]

document.getElementById("f").innerHTML = "代號: " + a[5]["id"]
document.getElementById("f1").innerHTML =  a[5]["price"]
document.getElementById("f2").innerHTML =  a[5]["percent"]
document.getElementById("f3").innerHTML =  a[5]["time"]
document.getElementById("f4").innerHTML =  a[5]["name"]