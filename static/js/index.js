const log = $("#log");
const file_input = $("#file_input");

// Whenever this form has a submit event,
$("form").submit(function (event) {
    // prevent form from redirecting/making a request and do this instead
    event.preventDefault();

    // Creates FormData object and sticks file in there
    let formData = new FormData();
    let fileData = file_input[0].files[0];
    formData.append("file", fileData);

    // Makes a POST request to the uploader endpoint
    // If successful, tell user file was uploaded successfully and clear #file_input
    // Else, tell user it failed
    $.ajax({
        url: 'uploader',
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(response){
            console.log(response);
            log.text(fileData.name + " was uploaded successfully.");
            file_input.val(null);
        },
        error: function(){
            log.text("The file upload failed.");
        }
    });
});