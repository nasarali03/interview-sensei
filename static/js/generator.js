// Generator JavaScript for InterviewAI

document.addEventListener("DOMContentLoaded", function () {
  // File upload handlers
  const jdFile = document.getElementById("jdFile");
  const resumeFile = document.getElementById("resumeFile");
  const jdFileInfo = document.getElementById("jdFileInfo");
  const resumeFileInfo = document.getElementById("resumeFileInfo");

  if (jdFile) {
    jdFile.addEventListener("change", function (e) {
      handleFileUpload(e.target, jdFileInfo);
    });
  }

  if (resumeFile) {
    resumeFile.addEventListener("change", function (e) {
      handleFileUpload(e.target, resumeFileInfo);
    });
  }

  function handleFileUpload(fileInput, infoElement) {
    const file = fileInput.files[0];
    if (file) {
      // Validate file size (10MB limit)
      const maxSize = 10 * 1024 * 1024; // 10MB in bytes
      if (file.size > maxSize) {
        showError(`File "${file.name}" is too large. Maximum size is 10MB.`);
        fileInput.value = "";
        return;
      }

      // Validate file type
      const allowedTypes = [".pdf", ".docx", ".doc", ".txt"];
      const fileExtension = "." + file.name.split(".").pop().toLowerCase();

      if (!allowedTypes.includes(fileExtension)) {
        showError(
          `File type "${fileExtension}" is not supported. Please upload PDF, DOCX, DOC, or TXT files.`
        );
        fileInput.value = "";
        return;
      }

      // Show file info
      infoElement.style.display = "block";
      infoElement.innerHTML = `
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <i class="fas fa-file-alt" style="color: #667eea;"></i>
                    <span>${file.name}</span>
                    <span style="color: #718096; font-size: 0.875rem;">
                        (${(file.size / 1024 / 1024).toFixed(2)} MB)
                    </span>
                    <button type="button" onclick="removeFile('${
                      fileInput.id
                    }')" 
                            style="background: none; border: none; color: #e53e3e; cursor: pointer; margin-left: auto;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
    }
  }

  // Remove file function (global for onclick)
  window.removeFile = function (fileInputId) {
    const fileInput = document.getElementById(fileInputId);
    const infoElement = fileInputId === "jdFile" ? jdFileInfo : resumeFileInfo;

    fileInput.value = "";
    infoElement.style.display = "none";
  };

  // Form submission
  const uploadForm = document.getElementById("uploadForm");
  if (uploadForm) {
    uploadForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      const submitBtn = document.getElementById("submitBtn");
      const loading = document.getElementById("loading");
      const result = document.getElementById("result");
      const error = document.getElementById("error");

      // Hide previous results
      result.style.display = "none";
      error.style.display = "none";

      // Show loading
      submitBtn.disabled = true;
      loading.style.display = "block";

      try {
        const formData = new FormData();

        // Add text inputs
        const jdText = document.getElementById("jdText").value.trim();
        const resumeText = document.getElementById("resumeText").value.trim();

        if (jdText) formData.append("job_description_text", jdText);
        if (resumeText) formData.append("resume_text", resumeText);

        // Add file inputs
        const jdFile = document.getElementById("jdFile").files[0];
        const resumeFile = document.getElementById("resumeFile").files[0];

        if (jdFile) formData.append("job_description_file", jdFile);
        if (resumeFile) formData.append("resume_file", resumeFile);

        // Validate that at least one input is provided
        if (!jdText && !resumeText && !jdFile && !resumeFile) {
          throw new Error(
            "Please provide at least a job description or resume (as text or file)."
          );
        }

        const response = await fetch("/upload-and-generate", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Failed to generate questions");
        }

        const data = await response.json();

        // Display results
        document.getElementById("resultContent").innerHTML = formatQuestions(
          data.questions_and_answers
        );
        result.style.display = "block";

        // Scroll to results
        result.scrollIntoView({ behavior: "smooth", block: "start" });
      } catch (err) {
        showError(`Error: ${err.message}`);
      } finally {
        submitBtn.disabled = false;
        loading.style.display = "none";
      }
    });
  }

  // Format questions for better display using markdown
  function formatQuestions(text) {
    if (!text) return "<p>No questions generated. Please try again.</p>";

    try {
      // Configure marked options for better formatting
      marked.setOptions({
        breaks: true,
        gfm: true,
        headerIds: false,
        mangle: false,
      });

      // Convert markdown to HTML
      const html = marked.parse(text);

      // Add custom classes for better styling
      const formattedHtml = html
        .replace(/<h1>/g, '<h1 class="md-h1">')
        .replace(/<h2>/g, '<h2 class="md-h2">')
        .replace(/<h3>/g, '<h3 class="md-h3">')
        .replace(/<h4>/g, '<h4 class="md-h4">')
        .replace(/<h5>/g, '<h5 class="md-h5">')
        .replace(/<h6>/g, '<h6 class="md-h6">')
        .replace(/<p>/g, '<p class="md-p">')
        .replace(/<ul>/g, '<ul class="md-ul">')
        .replace(/<ol>/g, '<ol class="md-ol">')
        .replace(/<li>/g, '<li class="md-li">')
        .replace(/<blockquote>/g, '<blockquote class="md-blockquote">')
        .replace(/<code>/g, '<code class="md-code">')
        .replace(/<pre>/g, '<pre class="md-pre">')
        .replace(/<strong>/g, '<strong class="md-strong">')
        .replace(/<em>/g, '<em class="md-em">');

      // Wrap in markdown-content div
      const result = `<div class="markdown-content">${formattedHtml}</div>`;

      // Apply syntax highlighting after a short delay to ensure DOM is ready
      setTimeout(() => {
        if (typeof Prism !== "undefined") {
          Prism.highlightAll();
        }
      }, 100);

      return result;
    } catch (error) {
      console.error("Error parsing markdown:", error);
      // Fallback to basic formatting
      return `<div class="markdown-content"><p>${text}</p></div>`;
    }
  }

  // Show error function
  function showError(message) {
    const error = document.getElementById("error");
    error.style.display = "block";
    error.textContent = message;
    error.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // Copy to clipboard function
  window.copyToClipboard = function () {
    const resultContent = document.getElementById("resultContent");
    const text = resultContent.innerText || resultContent.textContent;

    if (navigator.clipboard) {
      navigator.clipboard
        .writeText(text)
        .then(() => {
          showCopyNotification("Questions copied to clipboard!");
        })
        .catch(() => {
          fallbackCopyTextToClipboard(text);
        });
    } else {
      fallbackCopyTextToClipboard(text);
    }
  };

  function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      document.execCommand("copy");
      showCopyNotification("Questions copied to clipboard!");
    } catch (err) {
      showCopyNotification("Failed to copy. Please select and copy manually.");
    }

    document.body.removeChild(textArea);
  }

  function showCopyNotification(message) {
    // Create a simple notification
    const notification = document.createElement("div");
    notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #48bb78;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.animation = "slideOut 0.3s ease";
      setTimeout(() => {
        if (document.body.contains(notification)) {
          document.body.removeChild(notification);
        }
      }, 300);
    }, 3000);
  }

  // Add CSS for question formatting
  const questionStyles = document.createElement("style");
  questionStyles.textContent = `
        .question-block {
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: #f7fafc;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .question-title {
            color: #2d3748;
            margin-bottom: 1rem;
            font-size: 1.125rem;
            font-weight: 600;
        }
        
        .answer-point {
            margin: 0.5rem 0;
            padding-left: 1rem;
            color: #4a5568;
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .copy-btn {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
        }
        
        .copy-btn:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
  document.head.appendChild(questionStyles);

  // Drag and drop functionality
  const dropZones = document.querySelectorAll(".form-section");

  dropZones.forEach((zone) => {
    zone.addEventListener("dragover", function (e) {
      e.preventDefault();
      this.style.borderColor = "#667eea";
      this.style.backgroundColor = "#f7fafc";
    });

    zone.addEventListener("dragleave", function (e) {
      e.preventDefault();
      this.style.borderColor = "#e2e8f0";
      this.style.backgroundColor = "#f7fafc";
    });

    zone.addEventListener("drop", function (e) {
      e.preventDefault();
      this.style.borderColor = "#e2e8f0";
      this.style.backgroundColor = "#f7fafc";

      const files = e.dataTransfer.files;
      if (files.length > 0) {
        const file = files[0];
        const fileInput = this.querySelector('input[type="file"]');
        if (fileInput) {
          fileInput.files = files;
          fileInput.dispatchEvent(new Event("change"));
        }
      }
    });
  });

  console.log("InterviewAI generator loaded successfully!");
});
