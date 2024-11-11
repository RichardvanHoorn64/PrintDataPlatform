// Dropdown paper choices----------------------------------------------------------------------------------->


// get paperscategory selected -------------------------------------------------------------------------------->
const paperCategoryInput = document.getElementById('papercategory')

// select paperbrands
paperCategoryInput.addEventListener('change', e => {
    const selectedPaperCategory = e.target.value
    console.log("selectedPaperCategory: ", selectedPaperCategory);


    $.ajax({
        type: 'GET', url: `/paperbrand_json/${selectedPaperCategory}`,

        success: function (response) {
            console.log(response.data);
            data = response.data

            let html_data = '<option value="">Kies papiermerk</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.paperbrand}">${data.paperbrand}</option>`

            })
            $("#paperbrand").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
});


// get paperbrand selected -------------------------------------------------------------------------------->
const paperBrandInput = document.getElementById('paperbrand')

// select paperweight
paperBrandInput.addEventListener('change', e => {
    const selectedPaperBrand = e.target.value
    console.log("selectedBrand: ",selectedPaperBrand);


    $.ajax({
        type: 'GET', url: `/paperweight_json/${selectedPaperBrand}`,

        success: function (response) {
            console.log(response.data)
            data = response.data

            let html_data = '<option value="">Kies papiergewicht m2</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.paperweight_m2}">${data.paperweight_m2}</option>`

            })
            $("#paperweight").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
});

// get papierweight selected -------------------------------------------------------------------------------->
const paperWeightInput = document.getElementById('paperweight')


paperWeightInput.addEventListener('change', e => {
    const selectedPaperWeight = e.target.value
    console.log("selectedPaperWeightId : ", selectedPaperWeight);

    const selectedPaperBrand = document.getElementById('paperbrand').value;
    console.log("selectedPaperBrand : ", selectedPaperBrand);
// select papercolors

    $.ajax({
        type: 'GET', url: `/papercolor_json/${selectedPaperBrand}/${selectedPaperWeight}`,

        success: function (response) {
            console.log(response.data)
            data = response.data

            let html_data = null
                 // '<option value="">Kies kleur</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.papercolor}">${data.papercolor}</option>`

            })
            $("#papercolor").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
});

// End dropdown paper general---------------------------------------------------------------------------------->


// COVER:
// get paperategory cover selected -------------------------------------------------------------------------------->

const paperCategoryInputCover = document.getElementById('papercategory_cover')

// select paperbrands
paperCategoryInputCover.addEventListener('change', e => {
    const selectedPaperCategoryCover = e.target.value
    console.log("selectedPaperCategoryCover: ", selectedPaperCategoryCover);


    $.ajax({
        type: 'GET', url: `/paperbrand_cover_json/${selectedPaperCategoryCover}`,

        success: function (response) {
            console.log(response.data)
            data = response.data

            let html_data = '<option value="">Geen merkvoorkeur</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.paperbrand}">${data.paperbrand}</option>`

            })
            $("#paperbrand_cover").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
})


// get paperbrand selected -------------------------------------------------------------------------------->
const paperBrandInputCover = document.getElementById('paperbrand_cover')

// select paperweight
paperBrandInputCover.addEventListener('change', e => {
    const selectedPaperBrandCover = e.target.value
    console.log("selectedPaperBrandCover: ",selectedPaperBrandCover);


    $.ajax({
        type: 'GET', url: `/paperweight_cover_json/${selectedPaperBrandCover}`,

        success: function (response) {
            console.log(response.data)
            data = response.data

            let html_data = '<option value="">Kies papiergewicht m2</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.paperweight_m2}">${data.paperweight_m2}</option>`

            })
            $("#paperweight_cover").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
});

// get cover papercolor selected -------------------------------------------------------------------------------->
const paperWeightCoverInput = document.getElementById('paperweight_cover')


paperWeightCoverInput.addEventListener('change', e => {
    const selectedPaperWeightCover = e.target.value
    console.log("selectedPaperWeightCover : ", selectedPaperWeightCover);

// select papercolors cover
    const selectedPaperBrandCover = document.getElementById('paperbrand_cover').value;
    console.log("selectedPaperBrandCover 2 : ", selectedPaperBrandCover);

// select papercolors

    $.ajax({
        type: 'GET', url: `/papercolor_cover_json/${selectedPaperBrandCover}/${selectedPaperWeightCover}`,

        success: function (response) {
            console.log(response.data)
            data = response.data

            let html_data = null
                // '<option value="">Kies kleur</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.papercolor}">${data.papercolor}</option>`
            })
            $("#papercolor_cover").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
})



