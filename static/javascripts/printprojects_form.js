
function standaard_sizeSelectCheck(nameSelect) {
    var keuze_s = "0";
    console.log(nameSelect);
    if (nameSelect) {
        formaattypeValue = keuze_s;
        if (formaattypeValue === nameSelect.value) {
            document.getElementById("width_mm_input").style.display = "block";
            document.getElementById("height_mm_input").style.display = "block"
        } else {
            document.getElementById("width_mm_input").style.display = "none";
            document.getElementById("height_mm_input").style.display = "none"
        }
    } else {
        document.getElementById("width_mm_input").style.display = "block";
        document.getElementById("height_mm_input").style.display = "block"
    }
}


function validateForm() {
    console.log("form validate test")

    let x = document.forms["printproject_form"]["folding"].value;
    console.log("form validate input: ", x)
    if (x == "0") {
        alert("Kies vouwmethode");
        return false;
    }
    if (x == null) {
        alert("Kies vouwmethode null");
        return false;
    }

}