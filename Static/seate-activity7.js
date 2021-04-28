//Global variables
var prevCalc = 0;
var calc = "";


window.onload = function() {
    document.getElementById("btn1").onclick = showNum;//1
    document.getElementById("btn2").onclick = showNum;//2
    document.getElementById("btn3").onclick = showNum;//2
    document.getElementById("btn4").onclick = showNum;//4
    document.getElementById("btn5").onclick = showNum;//5
    document.getElementById("btn6").onclick = showNum;//6
    document.getElementById("btn7").onclick = showNum;//7
    document.getElementById("btn8").onclick = showNum;//8
    document.getElementById("btn9").onclick = showNum;//9
    document.getElementById("btn0").onclick = showNum;//0
    document.getElementById("btnDecimal").onclick = showNum;//.

    document.getElementById("btnDivide").onclick = divide;///
    document.getElementById("btnTimes").onclick = multiply;//*
    document.getElementById("btnMinus").onclick = subtract;//-
    document.getElementById("btnPlus").onclick = add;//+

    document.getElementById("btnSqrt").onclick = sqrt;//sqrt()
    document.getElementById("btnRound").onclick = round;//Round
    document.getElementById("btnFloor").onclick = floor;//Floor
    document.getElementById("btnIncrement").onclick = increment;//++
    document.getElementById("btnDecrement").onclick = decrement;//--
    document.getElementById("btnPow").onclick = pow;//^
    document.getElementById("btnPow2").onclick = pow2;//^2

    document.getElementById("btnClear").onclick = clear;//clear
    document.getElementById("btnCalculate").onclick = calculate;//calculate
}

//The following function displays a number in the textfield when a number is clicked.
//Note that it keeps concatenating numbers which are clicked.
function showNum() {
    document.frmCalc.txtNumber.value += this.value;
}

//The following function decreases the value of displayed number by 1.
//isNaN method checks whether the value passed to the method is a number or not.     
function decrement() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
        if (!(isNaN(num))) {
            num--;
            document.frmCalc.txtNumber.value = num;
        }
}

function increment() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
    if (!(isNaN(num))) {
        num++;
        document.frmCalc.txtNumber.value = num;
    }
}

//The following function is called when "Add" button is clicked. 
//Note that it also changes the values of the global variables.       
function add() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
        if (!(isNaN(num))) {
            prevCalc = num;
            document.frmCalc.txtNumber.value = "";
            calc = "Add";
        }
}

function subtract() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
    if (!(isNaN(num))) {
        prevCalc = num;
        document.frmCalc.txtNumber.value = "";
        calc = "Subtract";
    }
}

function sqrt() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
    if (!(isNaN(num))) {
        prevCalc = num;
        document.frmCalc.txtNumber.value = Math.sqrt(prevCalc);

    }
}

function round() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
    if (!(isNaN(num))) {
        prevCalc = num;
        document.frmCalc.txtNumber.value = parseInt(prevCalc)+1;

    }
}

function floor() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
    if (!(isNaN(num))) {
        prevCalc = num;
            document.frmCalc.txtNumber.value = Math.floor(prevCalc);

    }
}

function multiply() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
    if (!(isNaN(num))) {
        prevCalc = num;
        document.frmCalc.txtNumber.value = "";
        calc = "Multiply";
    }
}

function divide() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
    if (!(isNaN(num))) {
        prevCalc = num;
        document.frmCalc.txtNumber.value = "";
        calc = "Divide";
    }
}

function pow2() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
    if (!(isNaN(num))) {
        prevCalc = num;
        document.frmCalc.txtNumber.value = Math.pow(prevCalc, 2);

    }
}

function pow() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
    if (!(isNaN(num))) {
        prevCalc = num;
        document.frmCalc.txtNumber.value = "";
        calc = "Pow";
    }
}

//The following function is called when "Calculate" button is clicked.
//Note that this function is dependent on the value of global variable.        
function calculate() {
    var num = parseFloat(document.frmCalc.txtNumber.value);
        if (!(isNaN(num))) {
            if (calc == "Add"){
                var total = prevCalc + num;
                document.frmCalc.txtNumber.value = total;
            }

            else if (calc == "Subtract"){
                var total = prevCalc - num;
                document.frmCalc.txtNumber.value = total;
            }

            else if (calc == "Multiply"){
                var total = prevCalc * num;
                document.frmCalc.txtNumber.value = total;
            }

            else if (calc == "Divide"){
                var total = prevCalc / num;
                document.frmCalc.txtNumber.value = total;
            }

            else if (calc == "Pow"){
                var total = Math.pow(prevCalc, num);
                document.frmCalc.txtNumber.value = total;
            }
        
}}

function clear() {
	document.frmCalc.txtNumber.value = "";
	prevCalc = 0;
	calc = "";
}