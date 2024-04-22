document.addEventListener('DOMContentLoaded', () => {
    const getGifButton = document.getElementById('get-gif');
    const gifPreview = document.getElementById('gif-preview');
    const gifImg = document.getElementById('gif-img');

    const gifs = ['1IUZ', '6oa', '6vw5', 'AJl', 'DDt', 'JUT', 'PYh', 'XOsX', 'Xysh', 'Z0k', 'xw', 'y5'];

    getGifButton.addEventListener('click', () => {
        const selectedGif = gifs[getRandomInt(0, gifs.length)] + '.gif';
        fetch(`/file?file.File=/tmp/${selectedGif}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.blob();
            })
            .then(blob => {
                const gifUrl = URL.createObjectURL(blob);
                updateGifDisplay(gifUrl);
            })
            .catch(error => {
                alert('Failed to load the GIF.');
            });
    });

    function getRandomInt(min, max) {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random() * (max - min)) + min;
    }

    function updateGifDisplay(gifUrl) {
        gifImg.style.display = 'none';
        URL.revokeObjectURL(gifImg.src);

        gifImg.src = gifUrl;
        gifPreview.style.display = 'block';
        gifImg.style.display = 'block';
    }
});