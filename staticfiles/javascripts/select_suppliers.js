// uitleg: https://stackoverflow.com/questions/16712941/display-div-if-a-specific-select-option-value-is-selected
// demo: http://jsfiddle.net/CaVBZ/1/

/*jshint esversion: 6 */
/* jshint browser: true */


function SupplierSelectCheck(matchId) {
    // row level
    console.log('matchId: ', matchId);
    const suplierSwitch = document.getElementById("matchprintproject_switch");
    const suplierSwitchInput = suplierSwitch.checked;
    console.log('suplierSwitchInput: ', suplierSwitchInput);

    $.ajax({
        type: 'GET', url: `/select_supplier_switch_json/${matchId}`,

        success: function (response) {
            console.log('new_status: ', response.data);

        }, error: function (error) {
            console.log('error: ', error);
        }
    });
    location.reload();
}


