function ProductCategorySelectCheck(nameSelect) {
    var plano_choice = 'Plano';
    console.log(nameSelect);
    if (nameSelect) {
        formaattypeValue = plano_choice;
        if (formaattypeValue === nameSelect.value) {
            document.getElementById("paper_general").style.display = "block";
        } else {
            document.getElementById("paper_general").style.display = "none"
        }
    } else {
        document.getElementById("paper_general").style.display = "block";
    }
}
