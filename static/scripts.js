// scripts.js
document.addEventListener("DOMContentLoaded", function () {
    // Tab Switching Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            // Update active states
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            if (tabId === 'encode') {
                document.getElementById('encoding-section').classList.add('active');
            } else {
                document.getElementById('decoding-section').classList.add('active');
            }
        });
    });

    // File Preview Logic
    function setupFilePreview(inputId, previewClass) {
        const input = document.getElementById(inputId);
        const preview = input.parentElement.querySelector('.file-preview');

        input.addEventListener('change', function(e) {
            preview.innerHTML = '';
            const file = e.target.files[0];
            
            if (file && file.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.src = URL.createObjectURL(file);
                preview.appendChild(img);
            }
        });
    }

    setupFilePreview('image', '.file-preview');
    setupFilePreview('decode-image', '.file-preview');

    // Character Counter
    const messageInput = document.getElementById('message');
    const charCount = document.getElementById('char-count');

    messageInput.addEventListener('input', function() {
        charCount.textContent = this.value.length;
    });

    // Encode Form Submission
    document.getElementById("encode-form").addEventListener("submit", async function (e) {
        e.preventDefault();
        const loader = document.getElementById("encoding-loader");
        const downloadSection = document.getElementById("download-link");

        try {
            loader.style.display = "block";
            downloadSection.style.display = "none";

            const formData = new FormData();
            formData.append("image", document.getElementById("image").files[0]);
            formData.append("message", document.getElementById("message").value);

            const response = await fetch("/encode", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                const downloadLink = document.getElementById("encoded-download");
                downloadLink.href = URL.createObjectURL(blob);
                downloadLink.download = "encoded_image.png";
                downloadSection.style.display = "block";
            } else {
                const error = await response.json();
                alert(error.error || "Encoding failed. Please try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred during encoding.");
        } finally {
            loader.style.display = "none";
        }
    });

    // Decode Form Submission
    document.getElementById("decode-form").addEventListener("submit", async function (e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append("image", document.getElementById("decode-image").files[0]);
    
        try {
            const response = await fetch("/decode", {
                method: "POST",
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                if (result.error) {
                    alert(result.error);
                } else {
                    document.getElementById("message-output").textContent = result.message;
                    document.getElementById("decoded-message").style.display = "block";
                }
            } else {
                alert("Decoding failed. Please check your inputs and try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred during decoding.");
        }
    });

    // Copy Decoded Message
    document.getElementById("copy-message").addEventListener("click", function() {
        const messageText = document.getElementById("message-output").textContent;
        navigator.clipboard.writeText(messageText).then(() => {
            this.textContent = "Copied!";
            setTimeout(() => {
                this.textContent = "Copy";
            }, 2000);
        });
    });
});