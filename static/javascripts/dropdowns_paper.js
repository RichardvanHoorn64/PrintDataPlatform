// Dropdown paper choices----------------------------------------------------------------------------------->


// get paperscategory selected -------------------------------------------------------------------------------->
const paperCategoryInput = document.getElementById('papercategory')

// select paperbrands
paperCategoryInput.addEventListener('change', e => {
    const selectedPaperCategoryId = e.target.value
    console.log("selectedPaperCategoryId: ", selectedPaperCategoryId);


    $.ajax({
        type: 'GET', url: `/paperbrand_json/${selectedPaperCategoryId}`,

        success: function (response) {
            console.log(response.data);
            data = response.data

            let html_data = '<option value="">Kies papiermerk</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.paperbrand_id}">${data.paperbrand}</option>`

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
    const selectedPaperBrandId = e.target.value
    console.log("selectedBrandId: ", selectedPaperBrandId);


    $.ajax({
        type: 'GET', url: `/paperweight_json/${selectedPaperBrandId}`,

        success: function (response) {
            console.log(response.data)
            data = response.data

            let html_data = '<option value="">Kies papiergewicht m2</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.paperweight_id}">${data.paperweight_m2}</option>`

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
    const selectedPaperWeightId = e.target.value
    console.log("selectedPaperWeightId : ", selectedPaperWeightId);

// select papercolors

    $.ajax({
        type: 'GET', url: `/papercolor_json/${selectedPaperWeightId}`,

        success: function (response) {
            console.log(response.data)
            data = response.data

            let html_data = '<option value="">Kies kleur</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.paperspec_id}">${data.papercolor}</option>`

            })
            $("#papercolor").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
});

// End dropdown paper general---------------------------------------------------------------------------------->


// paper brand weight and color for covers:

// get paperategory cover selected -------------------------------------------------------------------------------->

const paperCategoryInputCover = document.getElementById('papercategory_cover')

// select paperbrands
paperCategoryInputCover.addEventListener('change', e => {
    const selectedPaperCategoryCoverId = e.target.value
    console.log("selectedPaperCategoryCoverId: ", selectedPaperCategoryCoverId);


    $.ajax({
        type: 'GET', url: `/paperbrand_cover_json/${selectedPaperCategoryCoverId}`,

        success: function (response) {
            console.log(response.data)
            data = response.data

            let html_data = '<option value="">Geen merkvoorkeur</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.paperbrand_id}">${data.paperbrand}</option>`

            })
            $("#paperbrand_cover").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
})


// get paperbrand cover selected -------------------------------------------------------------------------------->
const paperBrandCoverInput = document.getElementById('paperbrand_cover')

// select paperweight
paperBrandCoverInput.addEventListener('change', e => {
    const selectedPaperBrandCoverId = e.target.value
    console.log("selectedBrandCoverId: ", selectedPaperBrandCoverId);


    $.ajax({
        type: 'GET', url: `/paperweight_cover_json/${selectedPaperBrandCoverId}`,

        success: function (response) {
            console.log(response.data)
            data = response.data

            let html_data = '<option value="">Kies papiergewicht m2</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.paperweight_id}">${data.paperweight_m2}</option>`

            })
            $("#paperweight_cover").html(html_data)

        }, error: function (error) {
            console.log("cover weight error: ", error)
        }
    })
})

// get papierweight cover selected -------------------------------------------------------------------------------->
const paperWeightCoverInput = document.getElementById('paperweight_cover')


paperWeightCoverInput.addEventListener('change', e => {
    const selectedPaperWeightCoverId = e.target.value
    console.log("selectedPaperWeightCoverId : ", selectedPaperWeightCoverId);

// select papercolors

    $.ajax({
        type: 'GET', url: `/papercolor_cover_json/${selectedPaperWeightCoverId}`,

        success: function (response) {
            console.log(response.data)
            data = response.data

            let html_data = '<option value="">Kies kleur</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.paperspec_id}">${data.papercolor}</option>`

            })
            $("#papercolor_cover").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
})



