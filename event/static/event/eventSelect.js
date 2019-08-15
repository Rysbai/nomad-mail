

const localAPI = "http://127.0.0.1:8000/api";
const herokuAPI = "https://nomad-mailing.herokuapp.com/api";
const doAPI = "http://167.71.86.184/api";

const API_URL = localAPI;
function loadEvents(recEventId){
    $.ajax({
        type: "GET",
        url: API_URL + "/event/get_all",
        dataType: "json",
        success: function (data) {
            console.log(data);
            let i;
            for (i=0; i<data.length; i++){
                if (recEventId === data[i].id) {
                    $("#eventSelect").append($('<option>', {value: data[i].id, text: data[i].name, selected: true}))
                } else {
                    $("#eventSelect").append($('<option>', {value: data[i].id, text: data[i].name}))
                }
            }
        }

    });
}

function loadCountries(recCountries){
    $.ajax({
        type: "GET",
        url: API_URL + "/event/get_all_participants_country",
        dataType: "json",
        success: function (data) {
            console.log(recCountries);
            let i;
            for (i=0; i<data.length; i++){
                if (recCountries && data[i].name in recCountries) {
                    $("#countrySelect").append($('<option>', {value: data[i].name, text: data[i].name, selected: true}))
                } else {
                    $("#countrySelect").append($('<option>', {value: data[i].name, text: data[i].name}))
                }

            }

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
            $("#rec_counts").html("Количество получателей: " + data.length);
            $("#recipientTableBody").html(tableBodyItem)
        }
    })
}

$("#filter-recipients").click( function(){
    getRecipients()
});

const willGetRecipientsByIds = () => new Promise(
    function (resolve, reject) {
        const rec_ids = $('#id_rec_ids').val()
        $.ajax({
            type: "GET",
            url: API_URL + `/event/get_recipients_by_ids?rec_ids=${rec_ids}`,
            dataType: "json",
            success: function (data) {
                let i;
                let rec_ids = '';
                let tableBodyItem = [];
                for (i=0; i< data.recipients.length; i++){
                    rec_ids += data.recipients[i].id + ',';

                    tableBodyItem.push(`<tr>
                                        <td>${data.recipients[i].name}</td>
                                        <td>${data.recipients[i].surname}</td>
                                        <td>${data.recipients[i].distance}</td>
                                        <td>${data.recipients[i].country}</td>
                                        <td>${data.recipients[i].email}</td>
                                        <td>${data.recipients[i].sex}</td>
                                    </tr>`)
                }
                $("#rec_counts").html("Количество получателей: " + data.recipients.length);
                $("#recipientTableBody").html(tableBodyItem);
                resolve({
                    eventId: data.event_id,
                    countries: data.countries,
                    sex: data.sex
                })
            }
        })
    }
);

function loadPage() {
    if ($('#id_rec_ids').val()){
        willGetRecipientsByIds().then(res=> {
            console.log(res.countries);
            $(`#sexSelect option[value="${res.sex}"]`).prop('selected', true);
            loadEvents(res.eventId);
            loadCountries(res.countries);
        })
    } else {
        loadEvents();
        loadCountries();
    }
}

loadPage();