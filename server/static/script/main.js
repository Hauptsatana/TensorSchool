const x = new XMLHttpRequest();
x.open("GET", "/goods/1", true);
x.onload = function (){
    alert( x.responseText);
}
x.send(null);