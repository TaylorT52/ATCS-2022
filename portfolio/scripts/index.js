var nameElement = document.getElementById("nav-header"); 
var nameCounter = 0;
let nameTimer = setInterval(nameFunc, 300);
let nameStr = "aylor Tam"; 

function nameFunc() {
    var currStr = nameElement.innerHTML; 
    var add = nameStr.charAt(nameCounter); 
    nameElement.innerHTML = currStr + add; 
    nameCounter += 1;
    if(nameCounter > nameStr.length){
        clearInterval(nameTimer); 
    }
}

// Handle Bootstrap carousel slide event
$('.carousel').carousel({
    interval: 2
});