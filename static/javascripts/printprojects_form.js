// uitleg: https://stackoverflow.com/questions/16712941/display-div-if-a-specific-select-option-value-is-selected
// demo: http://jsfiddle.net/CaVBZ/1/

/*jshint esversion: 6 */
/* jshint browser: true */

// get categoryscategory selected -------------------------------------------------------------------------------->
const formDisplayInput = document.getElementById('productcategory_id');

// select papercategorie
formDisplayInput.addEventListener('change', e => {

    const productCategoryID = document.getElementById('productcategory_id').value;
    console.log(productCategoryID, " = Input");


    const paper_general = document.getElementById('paper_general');
    const printing_cover = document.getElementById('printing_cover');
    const paper_cover = document.getElementById('paper_cover');
    const folder_general = document.getElementById('folder_general');
    const brochures_finishing = document.getElementById('brochures_finishing');


    // Inner HTML field textoptions
    const finishing_brochures = document.getElementById('finishing_brochures');
    const paper_general_header = document.getElementById('paper_general_header');
    const print_general_header = document.getElementById('print_general_header');
    const printsided_plano_folders = document.getElementById('printsided_plano_folders');

    // required field options
    const folding = document.getElementById('folding');


    if (productCategoryID === "1") {
        console.log(productCategoryID, " = Plano");
        paper_general.style.display = "block";
        folder_general.style.display = "none";
        paper_cover.style.display = "none";
        printing_cover.style.display = "none";
        brochures_finishing.style.display = "none";
        // inner HTML
        paper_general_header.innerHTML = "Papier";
        print_general_header.innerHTML = "Bedrukking";
        // required
        folding.required = false;
        // field display
        printsided_plano_folders.style.display = "block";

    }
    if (productCategoryID === "2") {
        console.log(productCategoryID, " = Folders");
        paper_general.style.display = "block";
        folder_general.style.display = "block";
        paper_cover.style.display = "none";
        brochures_finishing.style.display = "none";
        printing_cover.style.display = "none";
        // inner HTML
        paper_general_header.innerHTML = "Papier";
        print_general_header.innerHTML = "Bedrukking";
        // required
        folding.required = true;
        // field display
        printsided_plano_folders.style.display = "block";
    }

    if (productCategoryID === "3") {
        console.log(productCategoryID, " = Selfcovers");
        paper_general.style.display = "block";
        folder_general.style.display = "none";
        paper_cover.style.display = "none";
        brochures_finishing.style.display = "block";
        printing_cover.style.display = "none";
        // inner HTML
        paper_general_header.innerHTML = "Papier selfcovers";
        print_general_header.innerHTML = "Bedrukking selfcover";
        finishing_brochures.innerHTML = "Nabewerking Selfcovers";
        // required
        folding.required = false;
        // field display
        printsided_plano_folders.style.display = "none";


    }

    if (productCategoryID === "4") {
        console.log(productCategoryID, " = Brochures gehecht");
        paper_general.style.display = "block";
        folder_general.style.display = "none";
        paper_cover.style.display = "block";
        brochures_finishing.style.display = "block";
        printing_cover.style.display = "block";
        // inner HTML
        paper_general_header.innerHTML = "Papier binnenwerk";
        print_general_header.innerHTML = "Bedrukking binnenwerk";
        finishing_brochures.innerHTML = "Nabewerking Gehecht";
        // required
        folding.required = false;
        // field display
        printsided_plano_folders.style.display = "none";


    }

    if (productCategoryID === "5") {
        console.log(productCategoryID, " = Brochures gebonden");
        paper_general.style.display = "block";
        folder_general.style.display = "none";
        paper_cover.style.display = "block";
        brochures_finishing.style.display = "block";
        printing_cover.style.display = "block";
        // inner HTML
        paper_general_header.innerHTML = "Papier binnenwerk";
        print_general_header.innerHTML = "Bedrukking binnenwerk";
        finishing_brochures.innerHTML = "Nabewerking Gebonden";
        // required
        folding.required = false;
        // field display
        printsided_plano_folders.style.display = "none";
    }

    return productCategoryID;
});


// New paper input
function new_paperSelectCheck() {
    const ProductCategoryID = returnProductCategoryID()
    console.log("selectedProductCategoryID 2:", ProductCategoryID)
    // NewPaperSwitch
    const NewPaperSwitch = document.getElementById("NewPaperSwitch");
    // Get the checkbox
    const checkBox = document.getElementById("NewPaperSwitch");
    // Get the default input
    const default_paper_input = document.getElementById("default_paper_input");
    const papercategory = document.getElementById("papercategory")
    const paperbrand = document.getElementById("paperbrand")
    const paperweight = document.getElementById("paperweight")
    const papercolor = document.getElementById("papercolor")


    if (default_paper_input.style.display === "none") {
        default_paper_input.style.display = "block";
        papercategory.required = true;
        paperbrand.required = true;
        paperweight.required = true;
        papercolor.required = true;
        NewPaperSwitch.innerHTML = "Papiersoort niet gevonden? Maak een nieuwe specificatie aan.";
    } else {
        default_paper_input.style.display = "none";
        papercategory.required = false;
        paperbrand.required = false;
        paperweight.required = false;
        papercolor.required = false;
        NewPaperSwitch.innerHTML = "Maak een nieuwe specificatie aan.";
    }
    console.log(default_paper_input.style.display)
}


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

// Print rear checks -------------------------------------------------------------------------------->
function print_rearSelectCheck(nameSelect) {
    // row level
    const print_rear_row = document.getElementById("print_rear_row")
    // div level
    const pms_colors_front_label = document.getElementById("pms_colors_front_label")
    // field level
    const print_front_label = document.getElementById("print_front_label")
    const pressvarnish_front_label = document.getElementById("pressvarnish_front_label")


    console.log("print choiche: ", nameSelect.value);
    if (nameSelect.value === "Tweezijdig verschillend") {
        print_rear_row.style.display = "block";
        print_front_label.innerHTML = "BEDRUKKING VOORZIJDE";
        pms_colors_front_label.innerHTML = "AANTAL PMS KLEUREN VOORZIJDE";
        pressvarnish_front_label.innerHTML = "PERSVERNIS VOORZIJDE";
    } else {
        print_rear_row.style.display = "none";
        print_front_label.innerHTML = "BEDRUKKING";
        pms_colors_front_label.innerHTML = "AANTAL PMS KLEUREN";
        pressvarnish_front_label.innerHTML = "PERSVERNIS";
    }
}

function print_rearCoverSelectCheck(nameSelect) {
    // row level
    const print_rear_cover_row = document.getElementById("print_rear_cover_row")
    // div level
    const number_pms_colors_cover_label = document.getElementById("number_pms_colors_cover_label")
    // field level
    const print_front_label_cover = document.getElementById("print_front_label_cover")
    const pressvarnish_cover_label = document.getElementById("pressvarnish_cover_label")


    if (nameSelect.value === "Tweezijdig verschillend") {
        print_rear_cover_row.style.display = "block";
        print_front_label_cover.innerHTML = "BEDRUKKING VOORZIJDE OMSLAG";
        number_pms_colors_cover_label.innerHTML = "AANTAL PMS KLEUREN VOORZIJDE OMSLAG";
        pressvarnish_cover_label.innerHTML = "PERSVERNIS VOORZIJDE OMSLAG";
    } else {
        print_rear_cover_row.style.display = "none";
        print_front_label_cover.innerHTML = "BEDRUKKING OMSLAG";
        number_pms_colors_cover_label.innerHTML = "AANTAL PMS KLEUREN OMSLAG";
        pressvarnish_cover_label.innerHTML = "PERSVERNIS OMSLAG";
    }
}


// Calculate number of pages folder -------------------------------------------------------------------------------->
const foldermethodInput = document.getElementById('folding')

// select paperbrands
foldermethodInput.addEventListener('change', e => {
    const foldermethodInputId = e.target.value
    console.log("selectedfoldermethodInputId: ", foldermethodInputId);


    $.ajax({
        type: 'GET', url: `/folder_number_of_pages_json/${foldermethodInputId}`,

        success: function (response) {
            console.log(response.data)
            data = response.data
            console.log("data: ", data)
            let html_data = data + " pagina's"
            console.log(html_data)
            $("#number_of_folder_pages").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
})

// Display enhance options -------------------------------------------------------------------------------->

const enhanceDisplayInput = document.getElementById('enhance_sided');

// select papercategorie
enhanceDisplayInput.addEventListener('change', e => {
    const enhanceChoice = e.target.value
    // fields
    const field_enhance_front = document.getElementById('field_enhance_front');
    const field_enhance_rear = document.getElementById('field_enhance_rear');
    const field_enhance_front_label = document.getElementById('field_enhance_front_label');
    const field_enhance_rear_label = document.getElementById('field_enhance_rear_label');

    console.log(enhanceChoice, " = enhanceChoice");

    if (enhanceChoice === "Geen veredeling") {
        field_enhance_front.style.display = "none";
        field_enhance_rear.style.display = "none";
    }

    if (enhanceChoice === "Tweezijdig gelijk") {
        field_enhance_front.style.display = "block";
        field_enhance_rear.style.display = "none";
        field_enhance_front_label.innerHTML = "Veredeling";
    }

    if (enhanceChoice === "Alleen voorzijde") {
        field_enhance_front.style.display = "block";
        field_enhance_rear.style.display = "none";
        field_enhance_front_label.innerHTML = "Veredeling voorzijde";
    }

    if (enhanceChoice === "Alleen achterzijde") {
        field_enhance_front.style.display = "none";
        field_enhance_rear.style.display = "block";
        field_enhance_rear_label.innerHTML = "Veredeling achterzijde";
    }
    if (enhanceChoice === "Tweezijdig verschillend") {
        field_enhance_front.style.display = "block";
        field_enhance_rear.style.display = "block";
        field_enhance_front_label.innerHTML = "Veredeling voorzijde";
        field_enhance_rear_label.innerHTML = "Veredeling achterzijde";
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