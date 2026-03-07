// static/emoji.js
let history = [];

async function generateEmoji() {
    const btn = document.getElementById('generate-btn');
    const display = document.getElementById('emoji-display');
    const resultImg = document.getElementById('emoji-result');
    const placeholder = document.getElementById('placeholder');
    const downloadBtn = document.getElementById('download-btn');

    try {
        btn.disabled = true;
        btn.innerText = '✨ Creating Magic...';
        display.classList.add('loading');
        placeholder.style.display = 'none';
        resultImg.style.display = 'none';

        // Add a timestamp to bypass any caching
        const response = await fetch(`/api/emoji/generate-emoji?t=${Date.now()}`);
        if (!response.ok) throw new Error('Generation failed');

        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);

        resultImg.src = imageUrl;
        resultImg.style.display = 'block';
        downloadBtn.style.display = 'inline-block';
        
        // Add to history
        addToHistory(imageUrl);

    } catch (error) {
        console.error(error);
        placeholder.style.display = 'block';
        placeholder.innerText = '❌ Error generating emoji. Try again.';
    } finally {
        btn.disabled = false;
        btn.innerText = '✨ Generate Magic Emoji';
        display.classList.remove('loading');
    }
}

function addToHistory(url) {
    const historyContainer = document.getElementById('history');
    const item = document.createElement('div');
    item.className = 'history-item';
    item.onclick = () => {
        document.getElementById('emoji-result').src = url;
    };
    
    const img = document.createElement('img');
    img.src = url;
    item.appendChild(img);
    
    historyContainer.prepend(item);
    
    // Keep only last 12
    if (historyContainer.children.length > 12) {
        historyContainer.removeChild(historyContainer.lastChild);
    }
}

function downloadEmoji() {
    const img = document.getElementById('emoji-result');
    if (!img.src) return;
    
    const a = document.createElement('a');
    a.href = img.src;
    a.download = `emoji-${Date.now()}.png`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}