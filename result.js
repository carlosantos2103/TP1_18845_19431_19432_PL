function onClick() {
    document.getElementById("label").style.display = "initial";
    if (document.getElementById("label").innerHTML !== "ATIVO") {
        document.getElementById("label").innerHTML = "ATIVO";
        document.getElementById("label").style.color = "green";
    } else {
        document.getElementById("label").innerHTML = "INATIVO";
        document.getElementById("label").style.color = "red";
    }
}

function openMenu(){
    if (document.getElementById("texto").style.display === "none") {
        document.getElementById("texto").style.display = "block";
    } else {
        document.getElementById("texto").style.display= "none";
    }
}

function viewDesc(){
    document.getElementById("desc").style.display = "inline";
}

function closeDesc(){
    document.getElementById("desc").style.display = "none";
}