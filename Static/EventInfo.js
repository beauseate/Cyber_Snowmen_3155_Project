window.onload = function() {

    document.getElementById("5").onclick = rate5;
    document.getElementById("4").onclick = rate4;
    document.getElementById("3").onclick = rate3;
    document.getElementById("2").onclick = rate2;
    document.getElementById("1").onclick = rate1;


    function rate5(){ 
        document.getElementById("5").style.color = "orange"; 
        document.getElementById("4").style.color = "orange";
        document.getElementById("3").style.color = "orange";
        document.getElementById("2").style.color = "orange"; 
        document.getElementById("1").style.color = "orange";
        }
        
    function rate4(){
        document.getElementById("5").style.color = "#9e9e9e"; 
        document.getElementById("4").style.color = "orange";
        document.getElementById("3").style.color = "orange";
        document.getElementById("2").style.color = "orange"; 
        document.getElementById("1").style.color = "orange";
    }
    
    function rate3(){
        document.getElementById("5").style.color = "#9e9e9e"; 
        document.getElementById("4").style.color = "#9e9e9e";
        document.getElementById("3").style.color = "orange";
        document.getElementById("2").style.color = "orange";
        document.getElementById("1").style.color = "orange";
    }
    
    function rate2(){
        document.getElementById("5").style.color = "#9e9e9e"; 
        document.getElementById("4").style.color = "#9e9e9e";
        document.getElementById("3").style.color = "#9e9e9e";
        document.getElementById("2").style.color = "orange"; 
        document.getElementById("1").style.color = "orange";
    }
    
    function rate1(){
        document.getElementById("5").style.color = "#9e9e9e"; 
        document.getElementById("4").style.color = "#9e9e9e";
        document.getElementById("3").style.color = "#9e9e9e";
        document.getElementById("2").style.color = "#9e9e9e";
        document.getElementById("1").style.color = "orange";
    }
}