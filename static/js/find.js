// Функция для получения URL постера по имени фильма с использованием TMDB API
async function getPosterUrl(movieName) {
    const response = await fetch(`https://api.themoviedb.org/3/search/movie?api_key=15d2ea6d0dc1d476efbca3eba2b9bbfb&query=${encodeURIComponent(movieName)}`);
    const data = await response.json();
    if (data.results && data.results.length > 0) {
        const posterPath = data.results[0].poster_path;
        return `https://image.tmdb.org/t/p/w500${posterPath}`;
    } else {
        return "static/img/default.png"; // Замените на URL изображения по умолчанию, если постер не найден
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    // Получаем все контейнеры фильмов
    const containers = document.querySelectorAll('.findcontainer');
    if (containers.length == 0){document.getElementById('main').innerHTML = "<br><center><h1>Nothing found, i guess...</h1></center><br>"}
    l = document.getElementById('foundthings').innerHTML
    document.getElementById('foundthings').innerHTML = `Loaded: 1 to ${containers.length} from ${l}` 
    for (let container of containers) {
        // Извлекаем имя фильма
        const nameElement = container.querySelector('#name');
        const movieName = nameElement.textContent;

        // Получаем URL постера
        const posterUrl = await getPosterUrl(movieName);

        // Вставляем URL постера в img
        const posterElement = container.querySelector('#poster');
        posterElement.src = posterUrl;

        wordsfs = document.getElementById("findsearch").innerHTML
        words = wordsfs.split(" ")

        const content = container.querySelector('#plot');
        const text = content.innerHTML;
    
        const regex = new RegExp(`\\b(${words.join('|')})\\b`, 'gi');
        const highlightedText = text.replace(regex, '<span class="highlight">$1</span>');
    
        content.innerHTML = highlightedText;
    }
});