// Dropdown envelope choices----------------------------------------------------------------------------------->


// get envelopeCategory selected -------------------------------------------------------------------------------->
const envelopeCategoryInput = document.getElementById('env_category_id')

// select envelopebrands
envelopeCategoryInput.addEventListener('change', e => {
    const selected_envelopeCategoryID = e.target.value
    console.log("selected_env_CategoryID: ", selected_envelopeCategoryID);


    $.ajax({
        type: 'GET', url: `/env_size_close_cut_json/${selected_envelopeCategoryID}`,

        success: function (response) {
            console.log(response.data);
            data = response.data

            let html_data = '<option value="">Kies formaat en uitvoering</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.env_size_close_cut}">${data.env_size_close_cut}</option>`

            })
            $("#env_size_close_cut").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
});


// get envelope Size Closure and Cut selected -------------------------------------------------------------------------------->
const envelopeMaterialColorInput = document.getElementById('env_size_close_cut')

// select envelopeweight
envelopeMaterialColorInput.addEventListener('change', e => {
    const selected_env_size_close_cut = e.target.value
    console.log("selectedSizeCloseCut: ",selected_env_size_close_cut);

    const selected_envelopeCategoryID = document.getElementById('env_category_id').value;
    console.log("selected_envelopeCategoryID : ", selected_envelopeCategoryID);


    $.ajax({
        type: 'GET', url: `/env_material_color_json/${selected_envelopeCategoryID}/${selected_env_size_close_cut}`,

        success: function (response) {
            console.log('env_material_color_json data : ', response.data)
            data = response.data

            let html_data = '<option value="">Kies materiaal en kleur</option>'
            data.forEach(function (data) {
                html_data += `<option value="${data.env_material_color}">${data.env_material_color}</option>`

            })
            $("#env_material_color").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
});

// get envelopes Material and color selected -------------------------------------------------------------------------------->
const envelopeWindowInput = document.getElementById('env_material_color')


envelopeWindowInput.addEventListener('change', e => {
    const selected_env_material_color = e.target.value
    console.log("selected_env_material_color : ", selected_env_material_color);

    const selected_envelopeCategoryID = document.getElementById('env_category_id').value;
    console.log("selected_envelopeCategoryID : ", selected_envelopeCategoryID);

    const selected_env_size_close_cut = document.getElementById('env_size_close_cut').value;
    console.log("selected_env_size_close_cut : ", selected_env_size_close_cut);

// select envelopecolors
    console.log('url: ', `/env_window_json/${selected_envelopeCategoryID}/${selected_env_size_close_cut}/${selected_env_material_color}`)

    $.ajax({
        type: 'GET', url: `/env_window_json/${selected_envelopeCategoryID}/${selected_env_size_close_cut}/${selected_env_material_color}`,

        success: function (response) {
            console.log(response.data)
            console.log('env_window_json data : ', response.data)
            data = response.data
            let number_of_windows = data.length

            let html_data = null
            if (number_of_windows > 1)
                html_data += '<option value="">Kies venster</option>'

            data.forEach(function (data) {
                html_data += `<option value="${data.env_window}">${data.env_window}</option>`

            })
            $("#env_window").html(html_data)

        }, error: function (error) {
            console.log(error)
        }
    })
});

// End dropdowns envelopes ---------------------------------------------------------------------------------->

