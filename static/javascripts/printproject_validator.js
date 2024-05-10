// uitleg: https://stackoverflow.com/questions/16712941/display-div-if-a-specific-select-option-value-is-selected
// demo: http://jsfiddle.net/CaVBZ/1/

/*jshint esversion: 6 */
/* jshint browser: true */


function validateFormPrintProjects() {
    const productCategoryID = document.getElementById('productcategory_id').value;

    console.log("PrintProject submit validator started");
    let inputform = document.forms.printproject_form;

    if (inputform.standard_size.value === "0" && inputform.width_mm_product.value==="") {
        alert("Geef bij vrij formaat de productbreedte (mm) in");
        event.preventDefault();
        return true;
    }

    if (inputform.standard_size.value === "0" && inputform.height_mm_product.value==="") {
        alert("Geef bij vrij formaat de producthoogte (mm) in");
        event.preventDefault();
        return true;
    }

    // for folders
    if (inputform.folding.value === "0" && productCategoryID==="2") {
        alert("Kies een vouwmethode");
        console.log("Vouwmethode alert started");
        event.preventDefault();
        return true;
    }

        // for brochures
   let page_remainder = inputform.number_of_pages.value % 4;
    if (page_remainder !== 0  &&  ["3", "4", "5"].includes(productCategoryID))
         {
        alert("Kies aantal pagina's als veelvoud van 4");
        console.log("Aantal pagina's alert started");
        event.preventDefault();
        return true;
    }


        if (inputform.finishing_brochures.value === ""  &&  ["3", "4", "5"].includes(productCategoryID))
         {
        alert("Kies nabewerking selfcovers");
        console.log("Nabewerking selfcovers alert started");
        event.preventDefault();
        return true;
    }
    return true;
}

function popUpEmpyProductCategory() {
     const productcategory = document.getElementById('productcategory_id').value;
     console.log("Papiercategorie alert started: ", productcategory);
     if (productcategory === "") {
         alert("Kies eerst een productcategorie: ", productcategory);
         }
}

// Paper general
function popUpEmpyPaperCategory() {
     const papercategory = document.getElementById('papercategory').value;
     console.log("Papiercategorie alert started: ", papercategory);
     if (papercategory === "") {
         alert("Kies eerst een papiercategorie.");
         }
}

function popUpEmpyPaperBrand() {
     const paperbrand = document.getElementById('paperbrand').value;
     console.log("Papierbrand alert started: ", paperbrand);
     if (paperbrand === "") {
         alert("Kies eerst een papiermerk.");
         }
}

function popUpEmpyPaperWeight() {
     const paperweight = document.getElementById('paperweight').value;
     console.log("papiergewicht cover alert started: ", paperweight);
     if ( paperweight === "") {
         alert("Kies eerst het papiergewicht.");
         }
}

// Paper general cover
function popUpEmpyPaperCategoryCover() {
     const papercategory_cover = document.getElementById('papercategory_cover').value;
     console.log("Papiercategorie omslag alert started: ", papercategory_cover);
     if (papercategory_cover === "") {
         alert("Kies eerst een omslag papiercategorie.");
         }
}


function popUpEmpyPaperBrandCover() {
     const paperbrand_cover = document.getElementById('paperbrand_cover').value;
     if (paperbrand_cover === "") {
         alert("Kies eerst een omslag papiermerk.");
         }
}

function popUpEmpyPaperWeightCover() {
     const paperweight_cover = document.getElementById('paperweight_cover').value;
     if ( paperweight_cover === "") {
         alert("Kies eerst het omslag papiergewicht.");
         }
}





/*

function validateFormPrintProjectsDemo(e) {
    let inputform = document.forms["printproject_form"];

    if (inputform["folding"].value === "") {
        alert("Geen aanvraag verstuurd: Kies uit standaard of vrij productformaat");
        return true;
    }

    if (inputform["folding"].value === null) {
        alert("Geen aanvraag verstuurd: Kies uit standaard of vrij productformaat");
        return true;
    }

    if (inputform["formaatkeuze"].value === "vrij" && inputform["hoogte_mm_product"].value === "") {
        alert("Geen aanvraag verstuurd: Vul het vrij productformaat in");
        return true;

    }

    if (inputform["formaatkeuze"].value === "vrij" && inputform["breedte_mm_product"].value === "") {
        alert("Geen aanvraag verstuurd: Vul het vrij productformaat in");
        return true;

    }

    if (inputform["aantal_paginas"].value === "") {
        alert("Geen aanvraag verstuurd: Kies het aantal paginas");
        return true;

    }

    if (inputform["nabewerking_brochures"].value === "Kies nabewerking") {
        alert("Geen aanvraag verstuurd: Kies een nabewerking");
        return true;

    }

    if (inputform["papiersoort_bw"].value === 0) {
        alert("Geen aanvraag verstuurd: Kies een papiersoort");
        return true;
    }

    if (inputform["papiergewicht_m2_bw"].value === "") {
        alert("Geen aanvraag verstuurd: Papiersoort en gewicht moeten beide gekozen worden");
        return true;
    }

    if (inputform["papierkleur"].value === "Kies een kleur") {
        alert("Geen aanvraag verstuurd: Papierkleur niet gekozen");
        return true;
    }


    if (inputform["papiersoort_omslag"].value === 0) {
        alert("Geen aanvraag verstuurd: Omslag papiersoort moet gekozen worden");
        return true;
    }

    if (inputform["papiergewicht_m2_omslag"].value === "") {
        alert("Geen aanvraag verstuurd: Omslag papiersoort en gewicht moeten beide gekozen worden");
        return true;
    }
    if (inputform["papierkleur_omslag"].value === "Kies een kleur") {
        alert("Geen aanvraag verstuurd: Papierkleur omslag niet gekozen");
        return true;
    }

    return false;
}

function terugnaarinvoer_plano() {

    document.getElementById("inputform_plano");
    element.addEventListener("submit", function () {
        document.preventDefault()
        // window.history.back()
        return false;
    })
}

function validateFormPlano() {
    let inputform = document.forms["inputform_plano"];

    if (inputform["formaatkeuze"].value === "geen_keuze") {
        alert("Geen aanvraag verstuurd: Kies uit standaard of vrij productformaat");
        return true;
    }

    if (inputform["formaatkeuze"].value === "vrij" && inputform["hoogte_mm_product"].value === "") {
        alert("Geen aanvraag verstuurd: Vul het vrij productformaat in");
        return true;

    }

    if (inputform["formaatkeuze"].value === "vrij" && inputform["breedte_mm_product"].value === "") {
        alert("Geen aanvraag verstuurd: Vul het vrij productformaat in");
        return true;

    }


    if (inputform["papiersoort"].value === 0) {
        alert("Geen aanvraag verstuurd: Kies een papiersoort");
        return true;
    }

    if (inputform["papiergewicht_m2"].value === "") {
        alert("Geen aanvraag verstuurd: Papiersoort en gewicht moeten beide gekozen worden");
        return true;
    }
    if (inputform["papierkleur"].value === "") {
        alert("Geen aanvraag verstuurd: Papierkleur niet gekozen");
        return true;
    }

    return false;
}


function validateFormFolders() {
    let inputform = document.forms["inputform_folders"];

    if (inputform["formaatkeuze"].value === "geen_keuze") {
        alert("Geen aanvraag verstuurd: Kies uit standaard of vrij productformaat");
        return true;
    }

    if (inputform["formaatkeuze"].value === "vrij" && inputform["hoogte_mm_product"].value === "") {
        alert("Geen aanvraag verstuurd: Vul het vrij productformaat in");
        return true;

    }

    if (inputform["formaatkeuze"].value === "vrij" && inputform["breedte_mm_product"].value === "") {
        alert("Geen aanvraag verstuurd: Vul het vrij productformaat in");
        return true;

    }

    if (inputform["aantal_paginas"].value === "") {
        alert("Geen aanvraag verstuurd: Kies het aantal paginas");
        return true;

    }

    if (inputform["nabewerking_folders"].value === "Kies nabewerking") {
        alert("Geen aanvraag verstuurd: Kies een nabewerking");
        return true;

    }

    if (inputform["papiersoort"].value === 0) {
        alert("Geen aanvraag verstuurd: Kies een papiersoort");
        return true;
    }

    if (inputform["papiergewicht_m2"].value === "") {
        alert("Geen aanvraag verstuurd: Papiersoort en gewicht moeten beide gekozen worden");
        return true;
    }
    if (inputform["papierkleur"].value === "") {
        alert("Geen aanvraag verstuurd: Papierkleur niet gekozen");
        return true;
    }

    return true;

}
*/
