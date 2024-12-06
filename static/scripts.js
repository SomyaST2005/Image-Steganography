// static/scripts.js

document.addEventListener("DOMContentLoaded", function () {
    // Handle Encode Form Submission
    document.getElementById("encode-form").addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData();
        formData.append("image", document.getElementById("image").files[0]);
        formData.append("message", document.getElementById("message").value);

        try {
            const response = await fetch("/encode", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                const downloadLink = document.getElementById("encoded-download");
                downloadLink.href = URL.createObjectURL(blob);
                downloadLink.download = "encoded_image.png";
                document.getElementById("download-link").style.display = "block";
            } else {
                alert("Encoding failed. Please try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred during encoding.");
        }
    });

    // Handle Decode Form Submission
    document.getElementById("decode-form").addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData();
        formData.append("image", document.getElementById("decode-image").files[0]);
        formData.append("message_length", document.getElementById("message-length").value);

        try {
            const response = await fetch("/decode", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                document.getElementById("message-output").textContent = result.message;
                document.getElementById("decoded-message").style.display = "block";
            } else {
                alert("Decoding failed. Please check your inputs and try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred during decoding.");
        }
    });
});
