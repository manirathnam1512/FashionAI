document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    
    let formData = new FormData();
    let fileInput = document.getElementById("fileInput");
    formData.append("file", fileInput.files[0]);

    let response = await fetch("http://127.0.0.1:5001/upload", {
        method: "POST",
        body: formData
    });

    let result = await response.json();
    
    if (result.error) {
        document.getElementById("output").innerText = "Error: " + result.error;
    } else {
        document.getElementById("output").innerText = "AI Suggestion: " + result.result.outfit_suggestion;
    }
});
