$.datetimepicker.setDateFormatter({
    parseDate: function (date, format) {
        var d = moment(date, format);
        return d.isValid() ? d.toDate() : false;
    },
    formatDate: function (date, format) {
        return moment(date).format(format);
    },
});

$('.datetime').datetimepicker({
    format:'DD-MM-YYYY hh:mm A',
    formatTime:'hh:mm A',
    formatDate:'DD-MM-YYYY',
    useCurrent: false,
});

// Initialise Pusher
const pusher = new Pusher('<d0d46422fb3e9456efd6>', {
    cluster: '<us2>',
    encrypted: true
});

var channel = pusher.subscribe('table');

channel.bind('new-record', (data) => {

    const start_time = moment(`${data.data.start_time}`, 'DD/MM/YYYY hh:mm a').format('YYYY-MM-DD hh:mm:ss a')
    const end_time = moment(`${data.data.end_time}`, 'DD/MM/YYYY hh:mm a').format('YYYY-MM-DD hh:mm:ss a')
    $('#reminders').append(`
        <tr id="${data.data.id}">
            <th scope="row"> ${data.data.title} </th>
            <td> ${data.data.description} </td>
            <td> ${start_time} </td>
            <td> ${end_time} </td>
        </tr>
   `)
});

channel.bind('update-record', (data) => {

    const start_time = moment(`${data.data.start_time}`, 'DD/MM/YYYY hh:mm a').format('YYYY-MM-DD hh:mm:ss a')
    const end_time = moment(`${data.data.end_time}`, 'DD/MM/YYYY hh:mm a').format('YYYY-MM-DD hh:mm:ss a')

    $(`#${data.data.id}`).html(`
        <th scope="row"> ${data.data.reminders} </th>
        <td> ${data.data.description} </td>
        <td> ${start_time} </td>
        <td> ${end_time} </td>
    `)

});