window.onload = async () => {
  const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
  const data = await res.json();
  const content = document.getElementById('content-area');

  data.forEach(video => {
    const div = document.createElement('div');
    div.className = 'video-item';
    div.innerHTML = `
      <a href="/watch?v=${video.videoId}">
        <img src="${video.thumbnail || ''}" width="320">
      </a>
      <p>${video.title}</p>
    `;
    content.appendChild(div);
  });
};
