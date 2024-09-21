// get client_id selected -------------------------------------------------------------------------------->
const clientIdInput = document.getElementById('client_id')

// select clientcontacts
clientIdInput.addEventListener('change', e => {
    const selectedClientId = e.target.value
    console.log("selectedClientId: ", selectedClientId);


    $.ajax({
        type: 'GET', url: `/select_clientcontact_json/${selectedClientId}`,

        success: function (response) {
            console.log('client_ids', response.data);
            data = response.data

            let html_data =
            data.forEach(function (data) {
                html_data += `<option value="${data.clientcontact_id}">${data.first_name} ${data.last_name}</option>`

            })
            $("#clientcontact_id").html(html_data)

         }, error: function (error) {
            console.log(error)
        }
    })
})



