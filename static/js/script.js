let y = new Date().getFullYear();
document.getElementById("date").max = 2017
document.getElementById("date").value = 2017
document.getElementById("date")
addEventListener("change",function(event){
    if (document.getElementById("date").value > document.getElementById("date").max){
        document.getElementById("date").value = 2017
    } else if (document.getElementById("date").value < 1901){
        document.getElementById("date").value = 1901
    }
})


function adv() {
    var x = document.getElementById('uas');
    if (x.style.display == 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}