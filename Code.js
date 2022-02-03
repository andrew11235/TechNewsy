function myFunction() {
var list = ["1", "2"];
var rand = Math.floor(Math.random() * list.length);

document.getElementById("newsnum").innerHTML = "Newsy " + rand + ": ";

document.getElementById("text").innerHTML = list[rand].toString();
}
