// uitleg: https://stackoverflow.com/questions/16712941/display-div-if-a-specific-select-option-value-is-selected
// demo: http://jsfiddle.net/CaVBZ/1/

/*jshint esversion: 6 */
/* jshint browser: true */

// New paper input
// function new_paperSelectCheck() {
//     const ProductCategoryID = returnProductCategoryID()
//     console.log("selectedProductCategoryID 2:", ProductCategoryID)
//     // NewPaperSwitch
//     const NewPaperSwitch = document.getElementById("NewPaperSwitch");
//     // Get the checkbox
//     const checkBox = document.getElementById("NewPaperSwitch");
//     // Get the default input
//     const default_paper_input = document.getElementById("default_paper_input");
//     const papercategory = document.getElementById("papercategory")
//     const paperbrand = document.getElementById("paperbrand")
//     const paperweight = document.getElementById("paperweight")
//     const papercolor = document.getElementById("papercolor")
//
//
//     if (default_paper_input.style.display === "none") {
//         default_paper_input.style.display = "block";
//         papercategory.required = true;
//         paperbrand.required = true;
//         paperweight.required = true;
//         papercolor.required = true;
//         NewPaperSwitch.innerHTML = "Papiersoort niet gevonden? Maak een nieuwe specificatie aan.";
//     } else {
//         default_paper_input.style.display = "none";
//         papercategory.required = false;
//         paperbrand.required = false;
//         paperweight.required = false;
//         papercolor.required = false;
//         NewPaperSwitch.innerHTML = "Maak een nieuwe specificatie aan.";
//     }
//     console.log(default_paper_input.style.display)
// }


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

// Print back checks -------------------------------------------------------------------------------->
function print_backSelectCheck(nameSelect) {
    // row level
    const print_back_row = document.getElementById("print_back_row")
    // div level
    const pms_colors_front_label = document.getElementById("pms_colors_front_label")
    // field level
    const print_front_label = document.getElementById("print_front_label")
    const pressvarnish_front_label = document.getElementById("pressvarnish_front_label")

    console.log("print back plano choice: ", nameSelect.value);
    if (nameSelect.value === "3") {
        print_back_row.style.display = "block";
        print_front_label.innerHTML = "BEDRUKKING VOORZIJDE";
        pms_colors_front_label.innerHTML = "AANTAL PMS KLEUREN VOORZIJDE";
        pressvarnish_front_label.innerHTML = "PERSVERNIS VOORZIJDE";
    } else {
        print_back_row.style.display = "none";
        print_front_label.innerHTML = "BEDRUKKING";
        pms_colors_front_label.innerHTML = "AANTAL PMS KLEUREN";
        pressvarnish_front_label.innerHTML = "PERSVERNIS";
    }
}

function print_backCoverSelectCheck(nameSelect) {
    // row level
    const print_back_cover_row = document.getElementById("print_back_cover_row")
    // div level
    const number_pms_colors_cover_label = document.getElementById("number_pms_colors_cover_label")
    // field level
    const print_front_label_cover = document.getElementById("print_front_label_cover")
    const pressvarnish_cover_label = document.getElementById("pressvarnish_cover_label")

     console.log("print cover choice: ", nameSelect.value);
    if (nameSelect.value === "3") {
        print_back_cover_row.style.display = "block";
        print_front_label_cover.innerHTML = "BEDRUKKING VOORZIJDE OMSLAG";
        number_pms_colors_cover_label.innerHTML = "AANTAL PMS KLEUREN VOORZIJDE OMSLAG";
        pressvarnish_cover_label.innerHTML = "PERSVERNIS VOORZIJDE OMSLAG";
    } else {
        print_back_cover_row.style.display = "none";
        print_front_label_cover.innerHTML = "BEDRUKKING OMSLAG";
        number_pms_colors_cover_label.innerHTML = "AANTAL PMS KLEUREN OMSLAG";
        pressvarnish_cover_label.innerHTML = "PERSVERNIS OMSLAG";
    }
}

// Display enhance options -------------------------------------------------------------------------------->

const enhanceDisplayInput = document.getElementById('enhance_sided');

// select papercategorie
enhanceDisplayInput.addEventListener('change', e => {
    const enhanceChoice = e.target.value
    // fields
    const field_enhance_front = document.getElementById('field_enhance_front');
    const field_enhance_back = document.getElementById('field_enhance_back');
    const field_enhance_front_label = document.getElementById('field_enhance_front_label');
    const field_enhance_back_label = document.getElementById('field_enhance_back_label');

    console.log("general enhanceChoice = ", enhanceChoice);

    if (enhanceChoice === "0") {
        console.log("no enhanceChoice = ", enhanceChoice);
        field_enhance_front.style.display = "none";
        field_enhance_back.style.display = "none";
    }

    if (enhanceChoice === "1") {
        field_enhance_front.style.display = "block";
        field_enhance_back.style.display = "none";
        field_enhance_front_label.innerHTML = "Veredeling voorzijde";
    }

    if (enhanceChoice === "2") {
        field_enhance_front.style.display = "block";
        field_enhance_back.style.display = "none";
        field_enhance_front_label.innerHTML = "Veredeling tweezijdig";
    }

    if (enhanceChoice === "3") {
        field_enhance_front.style.display = "none";
        field_enhance_back.style.display = "block";
        field_enhance_back_label.innerHTML = "Veredeling achterzijde";
    }
    if (enhanceChoice === "4") {
        field_enhance_front.style.display = "block";
        field_enhance_back.style.display = "block";
        field_enhance_front_label.innerHTML = "Veredeling voorzijde";
        field_enhance_back_label.innerHTML = "Veredeling achterzijde";
    }

});


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