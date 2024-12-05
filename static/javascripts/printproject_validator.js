// uitleg: https://stackoverflow.com/questions/16712941/display-div-if-a-specific-select-option-value-is-selected
// demo: http://jsfiddle.net/CaVBZ/1/

/*jshint esversion: 6 */
/* jshint browser: true */


function validateFormPrintProjects() {
    console.log("PrintProject submit validator started");
    let inputform = document.getElementById('printproject_form');


    const printproject = document.querySelector("#start_printproject");
    let categories_brochures = ["3", "4", "5"];
    let productCategoryID = printproject.dataset.productcategory_id;
    console.log("productCategoryID: ", productCategoryID);

    if (inputform.project_title.value==="") {
        alert("Geef een projectnaam op")
        return false;
    }

    if (inputform.volume.value==="") {
        alert("Geef de gewenste oplage op")
        return false;
    }

    if (inputform.standard_size.value === "0" && inputform.width_mm_product.value==="") {
        alert("Geef bij vrij formaat de productbreedte (mm) in");
        return false;
    }

    if (inputform.standard_size.value === "0" && inputform.height_mm_product.value==="") {
        alert("Geef bij vrij formaat de producthoogte (mm) in");
        return false;
    }

    // for folders
    if (productCategoryID==="2"){
            if (inputform.folding.value === "0") {
                alert("Kies een vouwmethode");
                console.log("Vouwmethode alert started");
                return false;
            }
    }

    // for brochures
   if (["3", "4", "5"].includes(productCategoryID)) {
        console.log("finishing brochures: ", inputform.finishing_brochures.value)
           if (inputform.finishing_brochures.value === "0") {
               alert("Kies nabewerking");
               console.log("Kies nabewerking alert started");
               return false;
           }
           let page_remainder = inputform.number_of_pages.value % 4;
        if (page_remainder !== 0 )
             {
            alert("Kies aantal pagina's als veelvoud van 4");
            console.log("Aantal pagina's alert started");
            return false;
           }
    }

    return true;
}


// Paper general
function popUpEmptyPaperCategory() {
     const papercategory = document.getElementById('papercategory').value;
     console.log("Papiercategorie alert started: ", papercategory);
     if (papercategory === "") {
         alert("Kies eerst een papiercategorie.");
         }
}

function popUpEmptyPaperBrand() {
     const paperbrand = document.getElementById('paperbrand').value;
     console.log("Papierbrand alert started: ", paperbrand);
     if (paperbrand === "") {
         alert("Kies eerst een papiermerk.");
         }
}

function popUpEmptyPaperWeight() {
     const paperweight = document.getElementById('paperweight').value;
     console.log("papiergewicht cover alert started: ", paperweight);
     if ( paperweight === "") {
         alert("Kies eerst het papiergewicht.");
         }
}

// Paper general cover
function popUpEmptyPaperCategoryCover() {
     const papercategory_cover = document.getElementById('papercategory_cover').value;
     console.log("Papiercategory cover alert started: ", papercategory_cover);
     if (papercategory_cover === "") {
         alert("Kies eerst een omslag papiercategorie.");
         }
}


function popUpEmptyPaperBrandCover() {
     const paperbrand_cover = document.getElementById('paperbrand_cover').value;
     console.log("Papierbrand cover alert started: ", paperbrand_cover);
     if (paperbrand_cover === "") {
         alert("Kies eerst een omslag papiermerk.");
         }
}

function popUpEmptyPaperWeightCover() {
     const paperweight_cover = document.getElementById('paperweight_cover').value;
     console.log("Papierweight cover alert started: ", paperweight_cover);
     if ( paperweight_cover === "") {
         alert("Kies eerst het omslag papiergewicht.");
         }
}


// Envelopes
function popUpEmptyEnvCategory() {
     const env_category_id = document.getElementById('env_category_id').value;
     console.log("Envelope category alert started: ", env_category_id);
     if (env_category_id === "") {
         alert("Kies eerst een enveloppen categorie.");
         }
}


function popUpEmptyEnvSizeCloseCut() {
     const env_size_close_cut = document.getElementById('env_size_close_cut').value;
     console.log("Envelope size closure cut alert started: ", env_size_close_cut);
     if (env_size_close_cut === "") {
         alert("Kies eerst de envelop uitvoering.");
         }
}

function popUpEmptyEnvMaterialColor() {
     const env_material_color = document.getElementById('env_material_color').value;
     console.log("Envelope  Material color alert started: ", env_material_color);
     if ( env_material_color === "") {
         alert("Kies eerst het envelop materiaal.");
         }
}

