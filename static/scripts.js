// scripts.js — StegShield Client
(function () {
    'use strict';

    // ============================================
    // State
    // ============================================
    const state = {
        encodeSubmitting: false,
        decodeSubmitting: false,
        objectURLs: [],
        encodeFile: null,
        decodeFile: null,
    };

    // ============================================
    // DOM References
    // ============================================
    const $ = (id) => document.getElementById(id);
    const dom = {
        themeToggle: $('theme-toggle'),
        tabBtns: document.querySelectorAll('.tab-btn'),
        tabIndicator: document.querySelector('.tab-indicator'),
        panels: document.querySelectorAll('.panel'),

        // Encode
        encodeForm: $('encode-form'),
        encodeDropzone: $('encode-dropzone'),
        encodeInput: $('encode-image-input'),
        encodePreview: $('encode-preview'),
        encodePreviewImg: $('encode-preview-img'),
        encodeFileInfo: $('encode-file-info'),
        encodeRemoveFile: $('encode-remove-file'),
        encodeCapacity: $('encode-capacity'),
        encodeCapacityFill: $('encode-capacity-fill'),
        encodeCapacityText: $('encode-capacity-text'),
        messageInput: $('message'),
        charCount: $('char-count'),
        encodeBtn: $('encode-btn'),
        encodeError: $('encode-error'),
        encodeSuccess: $('encode-success'),
        encodeDownload: $('encode-download'),

        // Decode
        decodeForm: $('decode-form'),
        decodeDropzone: $('decode-dropzone'),
        decodeInput: $('decode-image-input'),
        decodePreview: $('decode-preview'),
        decodePreviewImg: $('decode-preview-img'),
        decodeFileInfo: $('decode-file-info'),
        decodeRemoveFile: $('decode-remove-file'),
        decodeBtn: $('decode-btn'),
        decodeError: $('decode-error'),
        decodeSuccess: $('decode-success'),
        decodedMessageText: $('decoded-message-text'),
        copyBtn: $('copy-btn'),

        toastContainer: $('toast-container'),
    };

    // ============================================
    // Theme
    // ============================================
    function initTheme() {
        const saved = localStorage.getItem('stegshield-theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = saved || (prefersDark ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', theme);
    }

    function toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('stegshield-theme', next);
    }

    // ============================================
    // Tabs
    // ============================================
    function initTabs() {
        dom.tabBtns.forEach((btn) => {
            btn.addEventListener('click', () => switchTab(btn.dataset.tab));
        });

        // Keyboard: arrow keys
        const bar = document.querySelector('.tab-bar');
        bar.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                e.preventDefault();
                const current = document.querySelector('.tab-btn.active');
                const tabs = Array.from(dom.tabBtns);
                const idx = tabs.indexOf(current);
                const next = e.key === 'ArrowRight'
                    ? tabs[(idx + 1) % tabs.length]
                    : tabs[(idx - 1 + tabs.length) % tabs.length];
                switchTab(next.dataset.tab);
                next.focus();
            }
        });
    }

    function switchTab(tab) {
        dom.tabBtns.forEach((btn) => {
            const isActive = btn.dataset.tab === tab;
            btn.classList.toggle('active', isActive);
            btn.setAttribute('aria-selected', isActive);
        });

        dom.panels.forEach((panel) => {
            const isTarget = panel.id === `panel-${tab}`;
            panel.classList.toggle('active', isTarget);
            panel.hidden = !isTarget;
        });

        dom.tabIndicator.classList.toggle('decode', tab === 'decode');
    }

    // ============================================
    // Drop Zones
    // ============================================
    function initDropZone(dropzone, input, onFile) {
        ['dragenter', 'dragover'].forEach((evt) => {
            dropzone.addEventListener(evt, (e) => {
                e.preventDefault();
                dropzone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach((evt) => {
            dropzone.addEventListener(evt, (e) => {
                e.preventDefault();
                dropzone.classList.remove('dragover');
            });
        });

        dropzone.addEventListener('drop', (e) => {
            const file = e.dataTransfer.files[0];
            if (file) onFile(file);
        });

        dropzone.addEventListener('click', () => input.click());
        dropzone.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                input.click();
            }
        });

        input.addEventListener('change', () => {
            if (input.files[0]) onFile(input.files[0]);
        });
    }

    // ============================================
    // File Validation
    // ============================================
    function validateFile(file, mode) {
        const maxSize = 16 * 1024 * 1024;
        if (file.size > maxSize) {
            return { valid: false, error: 'File is too large (max 16 MB).' };
        }

        if (mode === 'encode') {
            const ok = ['image/png', 'image/jpeg'].includes(file.type);
            if (!ok) return { valid: false, error: 'Only PNG and JPEG images are supported.' };
        }

        if (mode === 'decode') {
            if (file.type !== 'image/png') {
                return { valid: false, error: 'Only PNG images can be decoded.' };
            }
        }

        return { valid: true };
    }

    function formatSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }

    // ============================================
    // Preview
    // ============================================
    function revokeURLs() {
        state.objectURLs.forEach((u) => URL.revokeObjectURL(u));
        state.objectURLs = [];
    }

    function showPreview(file, mode) {
        revokeURLs();
        const url = URL.createObjectURL(file);
        state.objectURLs.push(url);

        if (mode === 'encode') {
            dom.encodeDropzone.hidden = true;
            dom.encodePreview.hidden = false;
            dom.encodePreviewImg.src = url;
            dom.encodeFileInfo.innerHTML =
                `<strong>${file.name}</strong><br>${formatSize(file.size)} — ${file.type.split('/')[1].toUpperCase()}`;
            state.encodeFile = file;

            // Capacity calculation
            const img = new Image();
            img.onload = () => {
                const totalBits = img.width * img.height * 3 - 32;
                const maxChars = Math.floor(totalBits / 8);
                dom.encodeCapacity.hidden = false;
                dom.encodeCapacityText.textContent = `~${maxChars.toLocaleString()} characters max for this image (${img.width}×${img.height})`;
                updateCapacityBar(maxChars);
            };
            img.src = url;
        } else {
            dom.decodeDropzone.hidden = true;
            dom.decodePreview.hidden = false;
            dom.decodePreviewImg.src = url;
            dom.decodeFileInfo.innerHTML =
                `<strong>${file.name}</strong><br>${formatSize(file.size)}`;
            state.decodeFile = file;
        }
    }

    function removeFile(mode) {
        if (mode === 'encode') {
            dom.encodeDropzone.hidden = false;
            dom.encodePreview.hidden = true;
            dom.encodePreviewImg.src = '';
            dom.encodeInput.value = '';
            dom.encodeCapacity.hidden = true;
            state.encodeFile = null;
        } else {
            dom.decodeDropzone.hidden = false;
            dom.decodePreview.hidden = true;
            dom.decodePreviewImg.src = '';
            dom.decodeInput.value = '';
            state.decodeFile = null;
        }
        revokeURLs();
    }

    // ============================================
    // Capacity Bar
    // ============================================
    function updateCapacityBar(maxChars) {
        const msgLen = dom.messageInput.value.length;
        if (maxChars <= 0) {
            dom.encodeCapacityFill.style.width = '100%';
            dom.encodeCapacityFill.className = 'capacity-fill danger';
            return;
        }
        const pct = Math.min((msgLen / maxChars) * 100, 100);
        dom.encodeCapacityFill.style.width = pct + '%';
        dom.encodeCapacityFill.className = 'capacity-fill' +
            (pct > 80 ? ' danger' : pct > 50 ? ' warning' : '');
    }

    // ============================================
    // Character Counter
    // ============================================
    function initCharCounter() {
        dom.messageInput.addEventListener('input', () => {
            const len = dom.messageInput.value.length;
            dom.charCount.textContent = len;
            dom.charCount.parentElement.className = 'char-counter' +
                (len > 950 ? ' danger' : len > 800 ? ' warning' : '');
        });
    }

    // ============================================
    // Toast
    // ============================================
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        dom.toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('fade-out');
            toast.addEventListener('animationend', () => toast.remove());
        }, 4000);
    }

    // ============================================
    // Error Display
    // ============================================
    function showError(el, message) {
        el.textContent = message;
        el.hidden = false;
    }

    function hideError(el) {
        el.hidden = true;
    }

    // ============================================
    // Button Loading
    // ============================================
    function setLoading(btn, loading) {
        btn.disabled = loading;
        btn.classList.toggle('loading', loading);
    }

    // ============================================
    // Encode
    // ============================================
    async function handleEncode(e) {
        e.preventDefault();
        if (state.encodeSubmitting) return;

        hideError(dom.encodeError);
        dom.encodeSuccess.hidden = true;

        if (!state.encodeFile) {
            showError(dom.encodeError, 'Please select a cover image.');
            return;
        }

        const message = dom.messageInput.value.trim();
        if (!message) {
            showError(dom.encodeError, 'Please enter a message to encode.');
            return;
        }

        if (message.length > 1000) {
            showError(dom.encodeError, 'Message is too long (max 1000 characters).');
            return;
        }

        state.encodeSubmitting = true;
        setLoading(dom.encodeBtn, true);

        try {
            const formData = new FormData();
            formData.append('image', state.encodeFile);
            formData.append('message', message);

            const response = await fetch('/encode', { method: 'POST', body: formData });

            if (response.ok) {
                const blob = await response.blob();
                revokeURLs();
                const url = URL.createObjectURL(blob);
                state.objectURLs.push(url);
                dom.encodeDownload.href = url;
                dom.encodeSuccess.hidden = false;
                showToast('Message encoded successfully!', 'success');
            } else {
                const data = await response.json().catch(() => ({}));
                showError(dom.encodeError, data.error || 'Encoding failed. Please try again.');
                showToast('Encoding failed', 'error');
            }
        } catch (err) {
            showError(dom.encodeError, 'Network error. Please check your connection.');
            showToast('Network error', 'error');
        } finally {
            state.encodeSubmitting = false;
            setLoading(dom.encodeBtn, false);
        }
    }

    // ============================================
    // Decode
    // ============================================
    async function handleDecode(e) {
        e.preventDefault();
        if (state.decodeSubmitting) return;

        hideError(dom.decodeError);
        dom.decodeSuccess.hidden = true;

        if (!state.decodeFile) {
            showError(dom.decodeError, 'Please select an encoded image.');
            return;
        }

        state.decodeSubmitting = true;
        setLoading(dom.decodeBtn, true);

        try {
            const formData = new FormData();
            formData.append('image', state.decodeFile);

            const response = await fetch('/decode', { method: 'POST', body: formData });

            if (response.ok) {
                const data = await response.json();
                if (data.error) {
                    showError(dom.decodeError, data.error);
                    showToast('Decoding failed', 'error');
                } else {
                    dom.decodedMessageText.textContent = data.message;
                    dom.decodeSuccess.hidden = false;
                    showToast('Message decoded!', 'success');
                }
            } else {
                const data = await response.json().catch(() => ({}));
                showError(dom.decodeError, data.error || 'Decoding failed. Please try again.');
                showToast('Decoding failed', 'error');
            }
        } catch (err) {
            showError(dom.decodeError, 'Network error. Please check your connection.');
            showToast('Network error', 'error');
        } finally {
            state.decodeSubmitting = false;
            setLoading(dom.decodeBtn, false);
        }
    }

    // ============================================
    // Copy
    // ============================================
    function handleCopy() {
        const text = dom.decodedMessageText.textContent;
        navigator.clipboard.writeText(text).then(() => {
            const span = dom.copyBtn.querySelector('span');
            span.textContent = 'Copied!';
            setTimeout(() => { span.textContent = 'Copy'; }, 2000);
        }).catch(() => {
            showToast('Failed to copy to clipboard', 'error');
        });
    }

    // ============================================
    // Init
    // ============================================
    function init() {
        initTheme();
        initTabs();
        initCharCounter();

        dom.themeToggle.addEventListener('click', toggleTheme);

        // Encode dropzone
        initDropZone(dom.encodeDropzone, dom.encodeInput, (file) => {
            const v = validateFile(file, 'encode');
            if (!v.valid) {
                showToast(v.error, 'error');
                return;
            }
            showPreview(file, 'encode');
        });
        dom.encodeRemoveFile.addEventListener('click', () => removeFile('encode'));

        // Decode dropzone
        initDropZone(dom.decodeDropzone, dom.decodeInput, (file) => {
            const v = validateFile(file, 'decode');
            if (!v.valid) {
                showToast(v.error, 'error');
                return;
            }
            showPreview(file, 'decode');
        });
        dom.decodeRemoveFile.addEventListener('click', () => removeFile('decode'));

        // Forms
        dom.encodeForm.addEventListener('submit', handleEncode);
        dom.decodeForm.addEventListener('submit', handleDecode);

        // Copy
        dom.copyBtn.addEventListener('click', handleCopy);

        // Capacity bar updates with message input
        dom.messageInput.addEventListener('input', () => {
            const img = dom.encodePreviewImg;
            if (img.src && img.naturalWidth) {
                const totalBits = img.naturalWidth * img.naturalHeight * 3 - 32;
                const maxChars = Math.floor(totalBits / 8);
                updateCapacityBar(maxChars);
            }
        });

        // Cleanup on unload
        window.addEventListener('beforeunload', revokeURLs);
    }

    document.addEventListener('DOMContentLoaded', init);
})();
