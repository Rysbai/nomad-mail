


const API_URL = "https://nomad-mailing.herokuapp.com/api";
function loadEvents(){
    console.log("weeffsfsasdasda");
    $.ajax({
        type: "GET",
        url: API_URL + "/event/get_all",
        dataType: "json",
        success: function (data) {
            console.log(data);
            let i;
            let options = [];
            for (i=0; i<data.length; i++){
                options.push(`<option value="${ data[i].id }"> ${ data[i].name } </option>`)
            }
            $("#eventSelect").html(options)

        }

    });
}

function loadCountries(){
    console.log("weeffsfsasdasda");
    $.ajax({
        type: "GET",
        url: API_URL + "/event/get_all_participants_country",
        dataType: "json",
        success: function (data) {
            let i;
            let options = [];
            for (i=0; i<data.length; i++){
                options.push(`<option label="${ data[i].name }">${ data[i].name }</option>`)
            }
            $("#countrySelect").html(options)
        }
    });
}

function getRecipients() {
    const event_id = $("#eventSelect").val();
    const sex = $("#sexSelect").val();
    const countries = $("#countrySelect").val();
    $.ajax({
        type: "GET",
        url: API_URL + `/event/get_recipients?event_id=${event_id}&sex=${sex}&countries=${countries}`,
        dataType: "json",
        success: function (data) {
            let i;
            let rec_ids = '';
            let tableBodyItem = [];
            for (i=0; i< data.length; i++){
                rec_ids += data[i].id + ',';

                tableBodyItem.push(`<tr>
                                    <td>${data[i].name}</td>
                                    <td>${data[i].surname}</td>
                                    <td>${data[i].distance}</td>
                                    <td>${data[i].country}</td>
                                    <td>${data[i].email}</td>
                                    <td>${data[i].sex}</td>
                                </tr>`)
            }
            $('#id_rec_ids').val(rec_ids);
            $("#recipientTableBody").html(tableBodyItem)
        }
    })
}

$("#filter-recipients").click( function(){
    getRecipients()
}
);

loadEvents();
loadCountries();

