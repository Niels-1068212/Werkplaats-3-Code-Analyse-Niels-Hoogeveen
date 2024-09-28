function goedkeuren(onderzoeksId) {
    updateStatus(onderzoeksId, 2);
}

function afkeuren(onderzoeksId) {
    updateStatus(onderzoeksId, 3);
}
function updateStatus(onderzoeksId, nieuweStatus) {
    fetch(`/beheerder/update_status/${onderzoeksId}/${nieuweStatus}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            location.reload();
        })
        .catch(error => console.error('Error:', error));
}

function goedkeurenOrganisatie(organisatieId) {
    updateStatusOrganisatie(organisatieId, 2);
}
function afkeurenOrganisatie(organisatieId) {
    updateStatusOrganisatie(organisatieId, 3);
}
function updateStatusOrganisatie(organisatieId, nieuweStatus) {
    fetch(`/beheerder/update_organisatie_status/${organisatieId}/${nieuweStatus}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            location.reload();
        })
        .catch(error => console.error('Error:', error));
}


function goedkeurenErvaringsdeskundige(Id) {
    updateStatusErvaringsdeskundige(Id, 2);
}
function afkeurenErvaringsdeskundige(Id) {
    updateStatusErvaringsdeskundige(Id, 3);
}
function updateStatusErvaringsdeskundige(Id, nieuweStatus) {
    fetch(`/beheerder/update_ervaringsdeskundige_status/${Id}/${nieuweStatus}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            location.reload();
        })
        .catch(error => console.error('Error:', error));
}

function goedkeurenDeelnames(Id) {
    updateStatusDeelnames(Id, 2);
}
function afkeurenDeelnames(Id) {
    updateStatusDeelnames(Id, 3);
}
function updateStatusDeelnames(Id, nieuweStatus) {
    fetch(`/beheerder/update_deelnames_status/${Id}/${nieuweStatus}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            location.reload();
        })
        .catch(error => console.error('Error:', error));
}

async function getDashboardData() {
    const response_promise = await fetch("/beheerder/dashboard/all");
    const anwser = await response_promise.json();
    document.getElementById('research').innerHTML = anwser['research'];
    document.getElementById('experience_expert').innerHTML = anwser['experience_expert'];
    document.getElementById('organization').innerHTML = anwser['organization'];
    document.getElementById('attendance_request').innerHTML = anwser['attendance_request'];
    console.log(anwser)
}

window.addEventListener('load', function() {
    if (document.getElementById('research')) {
        getDashboardData();
        setInterval(getDashboardData, 1000)
    }
});