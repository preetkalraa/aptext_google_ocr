document.getElementById("upload-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("file-input");
    const resultDiv = document.getElementById("extracted-text");

    if (fileInput.files.length === 0) {
        alert("Please select an image file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Failed to upload image.");
        }

        const data = await response.json();
        resultDiv.textContent = data.text;
    } catch (error) {
        console.error(error);
        resultDiv.textContent = "An error occurred. Please try again.";
    }
});